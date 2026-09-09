"""Supply load-envelope experiments, not hardware qualification."""
import csv,json

def run(here, out, sheet, command, vector, save_csv):
    sheet('Startup','spice/startup.inc','.tran 1m 7 0 1m',
          'Simultaneous fan startup load-envelope experiment, NOT vendor model.\nDefault: assumed 1.1A/fan for 0.5s, then 0.55A/fan.\nAssumed 12V source, 0.5 ohm path, 100uF bus, 50mA auxiliary load.\nPlot V(fan_supply) and -I(Vsource). See startup_report.json.')
    rows=[]
    for peak in (.55,1.1,1.65):
        for resistance in (.1,.5,1.):
            for stagger in (0,5):
                deck=out/'startup_case.cir'
                deck.write_text('.title Startup assumed load envelope\n.include "spice/startup.inc"\n'
                    f'.param peak_a={peak} path_r={resistance} stagger_s={stagger}\n'
                    '.tran 1m 7 0 1m\n.end\n')
                command('destroy all');command('source results/startup_case.cir');command('run')
                times=vector('time');volts=vector('fan_supply');amps=[-x for x in vector('vsource#branch')]
                # Sanity-check solved plateau against independent Ohm-law result.
                expected_peak=(2*peak if stagger==0 else peak+.55)+.05
                # 1mA/1mV numerical allowance for transient integration.
                assert abs(max(amps)-expected_peak)<.001,(peak,resistance,stagger,max(amps))
                assert abs(min(volts)-(12-resistance*expected_peak))<.001
                assert abs(volts[-1]-(12-resistance*1.15))<1e-5
                rows.append({'assumed_peak_A_per_fan':peak,'assumed_path_ohm':resistance,
                    'stagger_s':stagger,'peak_source_A':max(amps),'minimum_bus_V':min(volts),
                    'final_bus_V':volts[-1]})
                if peak==1.1 and resistance==.5:
                    save_csv(f'startup_{stagger}s.csv',{'time_s':times,'fan_supply_V':volts,'source_A':amps})
    for index in range(0,len(rows),2):
        assert rows[index+1]['peak_source_A']<=rows[index]['peak_source_A']+.001
    with (out/'startup_matrix.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    report={'status':'18 exploratory cases solved; model sanity checks passed; NO hardware pass/fail',
      'published_max_fan_input_A':.55,'startup_current_measured':False,
      'assumptions':{'supply_V':12,'peak_duration_s':.5,'effective_bus_capacitance_uF':100,'auxiliary_load_A':.05,
                     'current_limit':'none','rail_startup':'supply already established before fan load steps'},
      'limits':['No real PSU selected','No measured fan inrush waveform','No fuse/PTC dynamics or MOSFET switching',
                'No rail ramp, brownout or firmware boot simulation','Stagger is scheduled stimulus, not implemented controller scheduler',
                'Peaks above 0.55A are hypothetical stress assumptions, not manufacturer ratings'],
      'cases':rows}
    (out/'startup_report.json').write_text(json.dumps(report,indent=2))
    return report
