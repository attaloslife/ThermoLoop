* EXPLORATORY load envelope, NOT a Noctua motor or PSU vendor model.
* 0.55A is published maximum input current, not measured startup current.
* Default 1.10A startup plateau is an assumed 2x stress case, not a claim.
.param supply_v=12 path_r=0.5 run_a=0.55 peak_a=1.10 aux_a=0.05
.param stagger_s=0 peak_s=0.5
.options method=gear reltol=1e-7 abstol=1e-12 vntol=1e-9
Vsource source 0 {supply_v}
* Lumped assumed PSU/cable/protection/PCB resistance. No current limit/foldback.
Rpath source fan_supply {path_r}
* 100uF is an illustrative effective bus capacitance, NOT extracted board C.
Cbus fan_supply 0 100u
Iaux fan_supply 0 {aux_a}
* First starts at 0.1s; second starts simultaneously or stagger_s later.
* Both remain at maximum running current after their startup plateaus.
Ifan1 fan_supply 0 PWL(0 0 0.1 0 0.101 {peak_a}
+ {0.101+peak_s} {peak_a} {0.102+peak_s} {run_a} 7 {run_a})
Ifan2 fan_supply 0 PWL(0 0 {0.1+stagger_s} 0 {0.101+stagger_s} {peak_a}
+ {0.101+stagger_s+peak_s} {peak_a} {0.102+stagger_s+peak_s} {run_a} 7 {run_a})
