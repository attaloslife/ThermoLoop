"""Analytical operating-envelope study. Not a PSU or motor transient model."""
import csv, json, math
from itertools import product

def evaluate(voltage, path, limit, fan_peak, auxiliary, fans, stagger):
    demand = (fan_peak*fans if not stagger else fan_peak+.55*(fans-1))+auxiliary
    running = .55*fans+auxiliary
    limited = demand > limit
    # Do not report a fictitious stable bus voltage when demand exceeds limit.
    bus = None if limited else voltage-demand*path
    flags=[]
    if voltage>13.2: flags.append('overvoltage')
    if limited: flags.append('current_capacity_exceeded')
    if bus is not None and bus<10.8: flags.append('below_provisional_10.8V_target')
    # Optimistic upper bound for hold-up after hard current limiting starts.
    # Assumes capacitor starts at full source voltage, ignores path losses/ESR.
    hold = (100e-6*max(0,voltage-10.8)/(demand-limit)) if limited else None
    return {'source_V':voltage,'lumped_path_ohm':path,'assumed_limit_A':limit,
            'assumed_fan_start_A':fan_peak,'assumed_aux_A':auxiliary,'fans':fans,
            'stagger_s':stagger,'peak_demand_A':demand,'running_A':running,
            'peak_bus_V_if_not_limited':bus,'steady_bus_V':voltage-running*path,
            'optimistic_100uF_hold_up_to_10_8V_s':hold,
            'classification':';'.join(flags) or 'within_provisional_envelope'}

def run(out):
    rows=[evaluate(*args) for args in product((11.4,12.,12.6,13.2,13.8),(.1,.25,.5,1.),
          (2.,3.,4.),(.55,1.1,1.65),(.05,.1),(1,2),(0,5))]
    assert len(rows)==1440
    a=evaluate(11.4,.25,3,1.1,.1,2,0)
    assert math.isclose(a['peak_demand_A'],2.3) and math.isclose(a['peak_bus_V_if_not_limited'],10.825)
    b=evaluate(11.4,.25,3,1.65,.1,2,0)
    assert b['peak_bus_V_if_not_limited'] is None and b['classification']=='current_capacity_exceeded'
    c=evaluate(11.4,.25,4,1.65,.1,2,0)
    assert c['classification']=='below_provisional_10.8V_target'
    assert evaluate(13.8,.1,4,.55,.1,1,0)['classification']=='overvoltage'
    # Cross-check analytical source droop against all previous SPICE cases.
    spice=json.loads((out/'startup_report.json').read_text())
    for case in spice['cases']:
        expected=evaluate(12,case['assumed_path_ohm'],99,case['assumed_peak_A_per_fan'],.05,2,case['stagger_s'])
        assert abs(expected['peak_bus_V_if_not_limited']-case['minimum_bus_V'])<.001
    with (out/'supply_matrix.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    # Resistance budget uses chosen target, NOT Noctua's minimum operating spec.
    report={'method':'1440 analytical envelope cases; 18 unlimited cases cross-checked against ngspice',
       'hardware_qualified':False,'voltage_floor_is_design_target_not_vendor_limit':10.8,
       'auxiliary_current_is_assumed_A':.1,'peak_duration_assumed_s':.5,
       'candidate_3A_2x_start':a,'hypothetical_3x_start_3A':b,'hypothetical_3x_start_4A':c,
       'maximum_path_ohm_at_11_4V':{'2x_start':(11.4-10.8)/2.3,'3x_start':(11.4-10.8)/3.4},
       'classification_counts':{label:sum(r['classification']==label for r in rows) for label in sorted({r['classification'] for r in rows})},
       'limits':['Current-limit threshold is assumed, not inferred from adapter nameplate',
                 'No dynamic constant-current, foldback or hiccup waveform simulated',
                 'No fan startup waveform known; 2x/3x peaks are hypothetical',
                 'No PSU regulation/overshoot model or real PCB protection/thermal model',
                 '10.8V target does not guarantee rated fan rpm or MCU/regulator stability']}
    (out/'supply_report.json').write_text(json.dumps(report,indent=2))
    return report
