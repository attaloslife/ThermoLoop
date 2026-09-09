"""Build KiCad testbench sheets and run their exported netlists with ngspice."""
from pathlib import Path
import ctypes as C
import csv, hashlib, json, os, subprocess, uuid
from control_model import Controller, adc_code, resistance, temperature
from startup_checks import run as run_startup_checks
from supply_study import run as run_supply_study
from temperature_accuracy import run as run_temperature_accuracy
from fault_tests import run as run_fault_tests

HERE = Path(__file__).resolve().parent
BIN = Path(os.environ.get('KICAD_BIN', r'C:\Program Files\KiCad\10.0\bin'))
OUT = HERE / 'results'
OUT.mkdir(exist_ok=True)
os.chdir(HERE)
sources = [p for n in ('1 Fan 2 Th','2 Fan 2 Th') for p in (HERE.parent/n).rglob('*') if p.is_file() and p.suffix in ('.kicad_sch','.kicad_pcb','.csv','.zip')]
before = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}

def sheet(name, include, analysis, explanation):
    # Deterministic generated testbench sheets, not manufacturing schematics.
    uid = lambda text: str(uuid.uuid5(uuid.NAMESPACE_URL, 'ThermoLoop-Simulation/'+text))
    texts = [('ThermoLoop simulation only - '+name,25,25), (explanation,25,40),
             ('.include "'+include+'"',25,75), (analysis,25,85),
             ('Open Inspect > Simulator. Run the analysis and select node voltages.\nModels live in spice/. See README.md for assumptions.\nThis is a reduced behavioral bench, not the production schematic.',25,105)]
    content='(kicad_sch (version 20250114) (generator "eeschema")\n(uuid "'+uid(name)+'") (paper "A4") (lib_symbols)\n'
    for i,(text,x,y) in enumerate(texts):
        content += '(text '+json.dumps(text)+' (at '+str(x)+' '+str(y)+' 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "'+uid(name+str(i))+'"))\n'
    content+='(sheet_instances (path "/" (page "1"))))\n'
    path=HERE/(name+'.kicad_sch');path.write_text(content,encoding='utf-8')
    net=OUT/(name+'.cir')
    subprocess.run([str(BIN/'kicad-cli.exe'),'sch','export','netlist','--format','spice','-o',str(net),str(path)],check=True)
    assert '.title' in net.read_text(),net
    # CLI export omits simulation-only sheet text. Build the batch wrapper
    # from the same include and analysis used by the GUI Simulator.
    net.write_text('.title ThermoLoop '+name+'\n.include "'+include+'"\n'+analysis+'\n.end\n')
    return net

benches = [sheet('Thermistors','spice/thermistors.inc','.dc Vtemperature 0 90 1',
    'Eaton NRMF104F3435B2J: 10k at 25 C, beta 3435 K (nominal approximation).\nTH1 sweeps 0 to 90 C; TH2 stays at 45 C. Open and short channels included.\nPlot V(th1_adc), V(th2_adc), V(open_adc), V(short_adc).'),
    sheet('Fan_PWM','spice/pwm.inc','.tran 50n 200u',
    '25 kHz GPIO stimulus -> behavioral inverter -> 33 ohm -> fan input.\nAssumed 25 ohm driver resistance, 1nF cable, 1k fan pull-up.\nPlot V(gpio), V(fan_pwm), V(reset_pwm). Ideal 5V supply.')]

logs=[]
SEND=C.CFUNCTYPE(C.c_int,C.c_char_p,C.c_int,C.c_void_p)
EXIT=C.CFUNCTYPE(C.c_int,C.c_int,C.c_bool,C.c_bool,C.c_int,C.c_void_p)
@SEND
def send(s, ident, userdata):
    logs.append(s.decode(errors='replace'));return 0
@EXIT
def quit_callback(status, immediate, exit_upon, ident, userdata):
    logs.append('CONTROLLED_EXIT '+str(status));return 0
class Vector(C.Structure):
    _fields_=[('name',C.c_char_p),('type',C.c_int),('flags',C.c_short),('real',C.POINTER(C.c_double)),('complex',C.c_void_p),('length',C.c_int)]
dll=C.CDLL(str(BIN/'ngspice.dll'))
dll.ngSpice_Init.argtypes=[SEND,C.c_void_p,EXIT,C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p]
dll.ngSpice_Init(send,None,quit_callback,None,None,None,None)
dll.ngSpice_Command.argtypes=[C.c_char_p]
dll.ngGet_Vec_Info.argtypes=[C.c_char_p];dll.ngGet_Vec_Info.restype=C.POINTER(Vector)
def command(s):
    result=dll.ngSpice_Command(s.encode());assert result==0,(s,result,logs[-10:])
def vector(s):
    ptr=dll.ngGet_Vec_Info(s.encode());assert ptr, (s,logs[-10:])
    v=ptr.contents;assert v.length>0 and v.real,s
    return [v.real[i] for i in range(v.length)]
def save_csv(name, columns):
    with (OUT/name).open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(columns);writer.writerows(zip(*columns.values()))

command('source results/Thermistors.cir');command('run')
adc=vector('th1_adc');opens=vector('open_adc');shorts=vector('short_adc')
assert len(adc)==91,len(adc)
assert all(a>b for a,b in zip(adc,adc[1:]))
assert abs(adc[25]-1.65)<1e-6,(adc[25],logs[-20:])
assert min(opens)>3.29 and max(shorts)<.001
assert all(abs(v-3.3*resistance(t)/(10000+resistance(t)))<1e-6 for t,v in enumerate(adc))
save_csv('thermistors.csv',{'temperature_C':range(91),'th1_adc_V':adc,'th2_adc_V':vector('th2_adc'),'open_V':opens,'short_V':shorts})
command('destroy all');command('source results/Fan_PWM.cir');command('run')
times=vector('time');pwm=vector('fan_pwm');reset=vector('reset_pwm')
assert min(pwm)<.8 and max(pwm)>4.5 and min(reset)>4.5
cross=[times[i] for i in range(1,len(times)) if pwm[i-1]<2.5<=pwm[i]]
assert len(cross)>=3 and abs((cross[-1]-cross[-2])-40e-6)<.2e-6,cross
save_csv('pwm.csv',{'time_s':times,'gpio_V':vector('gpio'),'fan_pwm_V':pwm,'reset_pwm_V':reset})

checks=[]
for sensors,fans in ((2,2),(2,1),(1,1)):
    c=Controller(sensors,fans)
    codes=lambda t:[adc_code(t)]*sensors
    assert c.update(0,codes(25))['duty']==[0.]*fans
    assert c.update(1,codes(36))['duty']==[1.]*fans
    mid=c.update(3,codes(50));assert all(.59<x<.61 for x in mid['duty'])
    assert c.update(4,codes(66))['duty']==[1.]*fans
    assert c.update(5,codes(34))['duty']==[.2]*fans
    assert c.update(6,codes(32))['duty']==[0.]*fans
    for fault in (0,1023):
        inp=codes(25);inp[-1]=fault;r=c.update(7,inp)
        assert r['alarm'] and r['duty']==[1.]*fans
    if sensors==2:
        expected=[0.,1.] if fans==2 else [1.]
        assert c.update(8,[adc_code(25),adc_code(70)])['duty']==expected
    checks.append(f'{fans}F/{sensors}TH: off, boost, ramp, full, hysteresis, open, short'+(', independent mapping' if fans==2 else ', hotter sensor (provisional)' if sensors==2 else ''))

# Primary model: independent startup timers and hysteresis in both directions.
for hot in (0,1):
    c=Controller(2,2)
    inp=[adc_code(25),adc_code(25)];inp[hot]=adc_code(50)
    r=c.update(0,inp);assert r['duty'][hot]==1 and r['duty'][1-hot]==0
    r=c.update(2,inp);assert .59<r['duty'][hot]<.61 and r['duty'][1-hot]==0
    inp[1-hot]=adc_code(40)
    r=c.update(3,inp);assert .59<r['duty'][hot]<.61 and r['duty'][1-hot]==1
    r=c.update(5,inp);assert .59<r['duty'][hot]<.61 and .32<r['duty'][1-hot]<.35
    inp[hot]=adc_code(32)
    r=c.update(6,inp);assert r['duty'][hot]==0 and .32<r['duty'][1-hot]<.35
    for fault in (0,1023):
        fault_input=inp.copy();fault_input[hot]=fault
        r=c.update(7,fault_input);assert r['alarm'] and r['duty']==[1.,1.]
checks.append('2F/2TH: asymmetric temperatures, separate boost timers and hysteresis, faults on either sensor')

startup_report=run_startup_checks(HERE,OUT,sheet,command,vector,save_csv)
supply_report=run_supply_study(OUT)
temperature_report=run_temperature_accuracy(OUT)
fault_report=run_fault_tests(OUT)
assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'Manufacturing files changed during run'
report={'status':'PASS - limited model checks only','thermistor_R25_ohm':10000,'thermistor_beta_K':3435,
        'primary_variant':'2F/2TH', 'normal_mapping':'TH1 -> FAN1; TH2 -> FAN2',
        'startup_load_envelope':startup_report['status'],
        'supply_requirements_study':supply_report['method'],
        'temperature_accuracy_study':temperature_report['method'],
        'fault_supervisor_tests':{'status':fault_report['status'],'checks':len(fault_report['checks'])},
        'provisional_fault_policy':'Any sensor fault commands all fans full speed plus alarm',
        'adc_voltage_at_C':{str(t):adc[t] for t in (25,35,50,65)},
        'pwm_min_V':min(pwm),'pwm_max_V':max(pwm),'pwm_period_s':cross[-1]-cross[-2],
        'reset_pwm_min_V':min(reset),'control_checks':checks,
        'manufacturing_file_hashes':before,'limits':['Not compiled ATtiny firmware','Not validated vendor inverter or fan model','Ideal supplies; no enclosure thermal model','Beta approximation; ADC acquisition/leakage omitted','Tach supervisor uses injected counts; no watchdog, brownout, LED or buzzer hardware simulation']}
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(OUT/'ngspice.log').write_text('\n'.join(logs),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='manufacturing_file_hashes'},indent=2))
