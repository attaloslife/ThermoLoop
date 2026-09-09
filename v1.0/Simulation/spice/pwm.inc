* Behavioral inverter, NOT a manufacturer SN74AHCT1G04 model.
* Ideal powered 5 V rail: cannot validate dropout, backfeed or power sequencing.
* Output resistance 25 ohm and cable capacitance 1nF are assumptions.
V5 rail5 0 5
Vgpio gpio 0 PULSE(0 3.3 10u 10n 10n 20u 40u)
R4 gpio input1 100
R3 input1 0 100k
Bdrive drive 0 V=5*(1-tanh((V(input1)-1.5)/0.1))/2
Rdriver drive output1 25
R26 output1 fan_pwm 33
Cwire fan_pwm 0 1n
* 5 V / 1k approximates the documented maximum 5 mA pull-up current.
Rfanpull rail5 fan_pwm 1k
R27 rail5 0 330
* Reset scenario: GPIO held low, powered inverter commands full speed.
Vreset reset_gpio 0 0
Breset reset_drive 0 V=5*(1-tanh((V(reset_gpio)-1.5)/0.1))/2
Rresetdriver reset_drive reset_out 25
R28 reset_out reset_pwm 33
Rresetpull rail5 reset_pwm 1k
Creset reset_pwm 0 1n
