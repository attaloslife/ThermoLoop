# ThermoLoop simulation project — initial model

Latest logic extension: [fault and recovery study](FAULT-BEHAVIOUR.md). User decisions: no calibration; 65 C is not a safety ceiling. The new supervisor tests missing tach and sensor recovery using injected inputs; it is not deployed firmware.

Temperature study: [first accuracy budget](TEMPERATURE-ACCURACY.md), including tolerance corners, threshold spread, self-heating and filtering. This is a beta-model sensitivity study, not a guaranteed accuracy bound; manufacturer table verification remains open.

Latest: [Supply requirements study](SUPPLY-REQUIREMENTS.md) — 1,440 analytical operating-envelope cases, with 18 unlimited-source cases cross-checked against ngspice. The 12 V / 3 A requirement remains provisional; current-limit dynamics and real startup currents are unverified.

Separate from the manufacturing designs. No PCB, Gerber, BOM or assembly file is edited by this project. This is not a manufacturing approval.

## Start here

Open `Thermistors.kicad_pro` or `Fan_PWM.kicad_pro` in KiCad 10, then open its schematic and choose **Inspect > Simulator**. Load the schematic directives into a new analysis and run. If necessary, enable full paths for include directives. The sheets are annotated simulation launchers: the reduced electrical circuits are in `spice/*.inc`, not drawn as production symbols. The CLI successfully parsed both sheets; interactive Simulator UI operation has not been verified.

- Thermistors: DC sweep `Vtemperature`, 0 to 90, increment 1. One volt on this artificial source represents one degree Celsius. Plot `V(th1_adc)`, `V(th2_adc)`, `V(open_adc)`, `V(short_adc)`.
- Fan_PWM: transient `.tran 50n 200u`. Plot `V(gpio)`, `V(fan_pwm)`, `V(reset_pwm)`.

Reproduce the batch simulation and control checks on this machine:

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' 'C:\Users\ersinaytac\Documents\GitHub\ThermoLoop\v1.0\Simulation\run_simulation.py'
```

The runner regenerates the two annotated sheets and results; edit the generator to change their text. It uses KiCad's installed ngspice DLL and has no additional Python dependency. Set `KICAD_BIN` for another installation. The CLI SPICE exporter omits simulation-only text directives, so the batch runner generates matching `.cir` wrappers from the same include paths and analysis definitions. These wrappers were actually simulated; this is not a full-board netlist simulation.

## Verified inputs and important correction

The Eaton **NRMF104F3435B2J is 10 kOhm at 25 C, not 100 kOhm**. Earlier references to 100 kOhm were incorrect and must not be used for firmware calibration. Nominal beta is 3435 K. This first version uses a beta equation, not Eaton's complete tabulated resistance curve or tolerance corners.

The board's R2/R22 pull-ups are 10 kOhm; R13/R23 are 1 kOhm series resistors; C6/C13 are 100 nF filters. TH2 is held at 45 C while TH1 sweeps. Open/short channels represent steady-state faults; fault detection latency and ADC acquisition are not simulated.

The Noctua fan is 12 V, up to 3000 rpm, with a 25 kHz target PWM interface. This first version models its PWM input only, NOT motor startup, current, rpm response, airflow or tachometer output. It uses an assumed 1 kOhm pull-up to 5 V and 1 nF lumped cable/input capacitance. The inverter is behavioral with assumed 25 Ohm output resistance and the board's 33 Ohm output resistor. Neither is a manufacturer-validated electrical model. The 5 V source is ideal; the 330 Ohm bleed is included but regulator stability/backfeed are not tested. Powered reset means GPIO low with the 5 V rail already valid; it does not represent a brownout or failed regulator.

Sources:

- [Eaton NRM datasheet, ELX1109](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-nrm-epoxy-sealed-radial-lead-ntc-thermistor-data-sheet-elx1109-en.pdf)
- [Noctua exact fan specifications](https://www.noctua.at/en/products/nf-a14-industrialppc-3000-pwm/specifications)
- [Noctua PWM interface specification](https://cdn.noctua.at/media/Noctua_PWM_specifications_white_paper.pdf)
- [KiCad Simulator documentation](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#simulator)

## Draft controller assumptions — user decisions still required

`control_model.py` is a Python specification model, NOT compiled ATtiny firmware. It assumes a ratiometric 10-bit ADC and supports 1F/1TH, 1F/2TH and 2F/2TH. It does not execute inside the SPICE simulation; the electrical and logic checks run separately.

- Primary test variant is **2F/2TH**: TH1 controls FAN1 and TH2 controls FAN2, with separate startup timers and hysteresis. This mapping is user-confirmed.
- 1F/2TH provisionally uses the hotter sensor; 1F/1TH uses its only sensor. Retain both as regression cases.
- Start at measured 35 C, stop at or below 33 C; hold running between these thresholds.
- One-second full-speed startup boost; then 20% command at 35 C, increasing linearly to 100% at 65 C. This is PWM command, not a percentage of fan power or rpm.
- Near-rail ADC codes (<=5 or >=1018) provisionally command **all** fans full speed and alarm, overriding independent normal operation. This fault policy still needs confirmation. Thresholds are provisional; this does not detect every possible sensor fault.
- No fault latching, fan-stall detection, watchdog, brownout behavior or automatic retries yet.

## First executed results

`results/report.json` contains numeric checks and hashes of the manufacturing files, verified unchanged during the run. `results/ngspice.log` contains the engine output; the CSV files contain full traces. The engine identifies itself as ngspice-46.

| Check | Nominal model result |
|---|---:|
| ADC node at 25 C | 1.650 V |
| ADC node at 35 C | 1.345 V |
| ADC node at 65 C | 0.672 V |
| PWM low / high | 0.274 V / 5.000 V |
| PWM period | 40 us (25 kHz) |
| Powered reset PWM | 5.000 V |

Control assertions cover off, startup boost, midpoint ramp, full command, cooling hysteresis, open and short inputs, independent two-fan mapping, separate channel timers, and the provisional hotter-sensor rule for 1F/2TH. These tests check the provisional model against its own requirements, not a physical fan or deployed firmware.

The two-fan model is the primary aggregate-load case for upcoming electrical tests: both fans running, simultaneous starts, asymmetric operation and stall/restart. The existing PWM bench is still a single switching channel plus a powered-reset channel, with ideal supplies: it does not yet establish two-fan supply performance. Lower-load variants still need regression tests, especially for minimum-load and startup behavior.

## Next work

### Simultaneous versus staggered startup: initial load-envelope study

Open `Startup.kicad_pro` for the default simultaneous case. The batch runner also evaluates a five-second stagger. `results/startup_report.json` and `startup_matrix.csv` contain 18 combinations:

- Assumed per-fan startup plateau: 0.55, 1.10 or 1.65 A, lasting 0.5 seconds.
- Assumed combined source/cable/protection/PCB resistance: 0.1, 0.5 or 1 ohm.
- Starts separated by zero or five seconds.

Noctua publishes maximum input current of 0.55 A, but the referenced product page does not provide a startup-current waveform. The 1.10/1.65 A cases are hypothetical 2x/3x stress envelopes, NOT manufacturer specifications or established worst-case bounds. Every case uses an assumed 50 mA auxiliary load, 100 uF effective bus capacitance, and a 12 V Thevenin source with NO current limiting/foldback. These are not extracted component/PSU models. The rail is already established before the first load step; cold power-up sequencing is not simulated. Constant-current loads do not reproduce motor dynamics at low voltage.

For the assumed 1.10 A peak and 0.5 ohm path:

| Scenario | Total peak demand | Minimum modelled bus voltage |
|---|---:|---:|
| Simultaneous | about 2.25 A | about 10.875 V |
| Five-second stagger | about 1.70 A | about 11.150 V |
| Both settled at 0.55 A each | 1.15 A | 11.425 V |

All 18 cases solved and passed consistency checks against their assumed circuit equations; this is NOT a supply or board pass/fail. Traces for the example are in `startup_0s.csv` and `startup_5s.csv`. The stagger is a scheduled load stimulus, not a newly implemented firmware scheduling rule. Sensor-to-fan independence is unchanged.

Needed next: exact supply model, cable length/gauge, measured or manufacturer-provided startup waveform, realistic protection-path parameters and auxiliary-load budget. Then add current limiting, rail ramps and MCU reset/boot behavior before judging startup robustness.

1. Confirm remaining minimum duty, hysteresis, startup boost and fault policy; two-fan normal mapping is settled.
2. Add the manufacturer's thermistor R/T table, resistor/sensor tolerance corners and ADC settling/error analysis.
3. Add tachometer/stall scenarios, then implement and test the real portable firmware control core.
4. Obtain compatible vendor models for power rails and logic; test startup, shutdown, rail failures and parameter corners.
5. Add LED/buzzer loads and power dissipation estimates. No enclosure thermal model is present.
6. Validate PWM, thermistors, fan startup, brightness and enclosed temperatures on a prototype.
