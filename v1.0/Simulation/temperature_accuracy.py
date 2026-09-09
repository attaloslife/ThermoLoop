"""Beta-model error budget. Not a manufacturer-guaranteed accuracy bound."""
import csv,json,math
from itertools import product
from control_model import resistance

def indicated(actual,r25_error=0,beta_error=0,pull_error=0,code_error=0):
    r=resistance(actual,10000*(1+r25_error),3435*(1+beta_error))
    code=1023*r/(10000*(1+pull_error)+r)+code_error
    ratio=code/(1023-code)
    return 1/(1/298.15+math.log(ratio)/3435)-273.15

def crossing(target,corner):
    lo,hi=0.,100.
    for _ in range(60):
        mid=(lo+hi)/2
        if indicated(mid,*corner)<target:lo=mid
        else:hi=mid
    return (lo+hi)/2

def run(out):
    corners=list(product((-.01,.01),(-.05,.05),(-.01,.01),(-2.5,2.5)))
    rows=[]
    for t in range(25,76):
        errors=[indicated(t,*corner)-t for corner in corners]
        r=resistance(t);rth=1000+10000*r/(10000+r)
        power=3.3**2*r/(10000+r)**2
        quant=[indicated(t,code_error=q)-t for q in (-.5,.5)]
        row={'true_bead_C':t,'modeled_error_min_C':min(errors),'modeled_error_max_C':max(errors),
             'half_LSB_error_max_C':max(map(abs,quant)),
             'self_heating_estimate_C':power/.0008,'source_impedance_ohm':rth,
             'filter_tau_ms':rth*100e-9*1000,'filter_settle_half_LSB_ms':rth*100e-9*math.log(2046)*1000}
        for name,kwargs in [('R25',{'r25_error':.01}),('beta',{'beta_error':.05}),('pullup',{'pull_error':.01}),('ADC_2LSB',{'code_error':2})]:
            row[name+'_positive_parameter_error_C']=indicated(t,**kwargs)-t
        assert abs(indicated(t)-t)<1e-9
        assert min(errors)<0<max(errors)
        rows.append(row)
    switches={}
    for target in (33,35,65):
        values=[crossing(target,c) for c in corners]
        switches[str(target)]={'earliest_true_bead_C':min(values),'latest_true_bead_C':max(values)}
        for c in corners:assert abs(indicated(crossing(target,c),*c)-target)<1e-8
    # Ratiometric DC supply cancellation, ideal circuit only.
    for v in (3.0,3.3,3.6):
        r=resistance(50);assert abs((v*r/(10000+r))/v-r/(10000+r))<1e-12
    assert max(r['source_impedance_ohm'] for r in rows)<10000
    # ADC pin leakage sensitivity is separate, not added to the corner bound.
    leakage=[]
    for t in (35,65):
        r=resistance(t);rth=1000+10000*r/(10000+r)
        for amp in (50e-9,1e-6):
            delta=amp*rth/3.3*1023
            leakage.append({'temperature_C':t,'assumed_leakage_A':amp,
                'worst_magnitude_C':max(abs(indicated(t,code_error=s*delta)-t) for s in (-1,1))})
    with (out/'temperature_accuracy.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    result={'method':'51 temperatures x 16 corners; analytical beta-model sensitivity',
       'R25_tolerance_percent':1,'beta_tolerance_percent':5,'pullup_tolerance_percent':1,
       'ADC_error_assumption_LSB':2,'additional_quantization_allowance_LSB':.5,
       'ADC_2LSB_is_typical_not_guaranteed_maximum':True,
       'threshold_crossings_without_self_heating_or_lag':switches,
       'key_points':[r for r in rows if r['true_bead_C'] in (25,35,50,65)],
       'pin_leakage_separate_sensitivity':leakage,
       'thermal_lag_example':{'assumed_tau_s':10,'ramp_C_per_s':.1,'asymptotic_lag_C':1},
       'limits':['Nominal manufacturer table not incorporated: merged heading requires verification',
         'Beta tolerance represented as constant-beta variation; not full curve envelope',
         'ADC allowance is illustrative and may overlap quantization in typical EABS spec',
         'No resistor temperature coefficient, cable resistance or contact/ground errors in combined bound',
         'Self-heating and thermal lag reported separately; mounting affects both',
         'RC settling is input-filter estimate, not complete ADC acquisition validation']}
    (out/'temperature_accuracy.json').write_text(json.dumps(result,indent=2))
    return result
