* Simulation-only reduced circuit. Nominal beta approximation, not Eaton R/T table.
* R2/R22 = 10k pull-up; R13/R23 = 1k; C6/C13 = 100n.
Vrail rail 0 3.3
.options reltol=1e-7 abstol=1e-12 vntol=1e-9
* Temperature stimulus: 1 V represents 1 degree C. DC analysis sweeps this.
Vtemperature temperature 0 25
R2 rail th1_raw 10k
Bntc1 th1_raw 0 I=V(th1_raw)/(10000*exp(3435*(1/(V(temperature)+273.15)-1/298.15)))
R13 th1_raw th1_adc 1k
C6 th1_adc 0 100n
* Second sensor fixed at 45 C for comparison.
R22 rail th2_raw 10k
Rntc2 th2_raw 0 {10000*exp(3435*(1/318.15-1/298.15))}
R23 th2_raw th2_adc 1k
C13 th2_adc 0 100n
* Duplicate channels demonstrate steady-state open/short faults.
Ropen rail open_adc 10k
Rleak open_adc 0 1e12
Rshortpull rail short_adc 10k
Rshort short_adc 0 0.01
