# Supply requirements study — provisional, not hardware qualification

## Outcome

Keep **regulated 12 V DC, 3 A continuous** as a candidate specification for the specified one/two Noctua NF-A14 industrialPPC-3000 PWM configurations. It is NOT yet a validated universal requirement. A 4 A supply offers more margin against the hypothetical high-startup-current case, but does not eliminate cable voltage drop or validate the board's protection path. Do not increase board fuse ratings based on this study.

## What was tested

The reproducible runner evaluates 1,440 analytical combinations of source voltage (11.4/12/12.6/13.2/13.8 V), total effective path resistance (0.1/0.25/0.5/1 ohm), assumed current-capacity threshold (2/3/4 A), per-fan startup demand (0.55/1.1/1.65 A), auxiliary load (50/100 mA), one/two fans, and simultaneous/five-second-staggered starts. One-fan stagger cases are intentionally equivalent regression cases, not distinct electrical conditions.

18 voltage-droop calculations were cross-checked against the existing ngspice startup simulations within 1 mV. The current-capacity comparisons are analytical checks, NOT simulated PSU current-limit dynamics. Exceeded limits are flagged without inventing a stable output voltage. The study does not model foldback, hiccup, shutdown/retry or motor response to undervoltage. A current-limit threshold is not necessarily equal to the adapter's nameplate rating.

Files: `results/supply_report.json`, `results/supply_matrix.csv`. Run `run_simulation.py` to reproduce all checks. No manufacturing files are modified.

## Known versus assumed inputs

The [Noctua product specifications](https://www.noctua.at/en/products/nf-a14-industrialppc-3000-pwm/specifications) publish 12 V rated supply, 0.55 A maximum input current per fan, 7 V starting voltage, and 13.2 V maximum operating voltage. They do not supply the startup waveform used here. 1.1/1.65 A are hypothetical stress values, not measured currents, manufacturer specifications or proven bounds.

The 10.8 V bus floor is our provisional design target, NOT a manufacturer minimum and NOT proof of rated speed, regulator regulation or MCU stability. Startup pulses last an assumed 0.5 seconds. The auxiliary-current budget is not a completed MCU/LED/buzzer worst-case calculation. Capacitance is an illustrative 100 uF effective bus value; actual distributed capacitance, bias, tolerance, ESR and location are not extracted.

## Key two-fan results

Using 100 mA auxiliary load:

| Condition | Demand | Interpretation |
|---|---:|---|
| Both at published maximum running current | 1.20 A | Below the 3 A capacity target |
| Both start at assumed 1.10 A each | 2.30 A | Below the 3 A capacity target |
| Five-second stagger, assumed 1.10 A startup | 1.75 A | Lower peak, provided pulses do not overlap |
| Both start at assumed 1.65 A each | 3.40 A | Exceeds a 3 A capacity threshold |
| Five-second stagger, assumed 1.65 A startup | 2.30 A | Does not cover simultaneous reset/power-on |

At 11.4 V source voltage and 0.25 ohm effective path resistance, 2.30 A leaves **10.825 V** at the modelled bus. The maximum path budget to maintain 10.8 V is approximately **0.261 ohm**. This includes effective source impedance and both supply/return paths, connectors, protection and PCB resistance; it is not a cable-only allowance.

At 3.40 A the same path would leave **10.55 V**, even with a 4 A supply. Maintaining the same target requires a path budget below approximately **0.176 ohm**. No recommended cable gauge can be assigned until cable length and the non-cable resistance budget are established.

100 uF cannot compensate for a long overload. With a hypothetical 3.4 A demand, 3 A hard limit and an initially charged 11.4 V bus, the optimistic hold-up time to 10.8 V is only **0.15 ms**, compared with the assumed 500 ms startup plateau. This bound ignores path resistance/ESR and assumes the load continues demanding the same current. It is not a simulated brownout waveform.

## Candidate procurement/installation requirements

- Regulated 12 V DC, candidate tolerance +/-5% at the source under rated conditions (11.4 to 12.6 V).
- Candidate 3 A continuous capacity **at the actual installed ambient temperature**, dedicated to this controller and its supported loads. Shared project loads require additional budget.
- Validate simultaneous startup without current limiting, hiccup or restart; firmware staggering must not be the only protection.
- Keep ripple/overshoot at the fan below its 13.2 V maximum. This is only the fan's limit; the whole board still needs a transient review.
- Verify at least the provisional 10.8 V bus target during selected load tests, without MCU resets or regulator dropout.
- Correct polarity, adequate connectors and short/appropriately sized supply/return wiring. Do not interpret a higher-current supply as permission to install higher-current fans.

These remain draft acceptance criteria, not released product specifications. Different fan models need separate current/startup limits.

## Remaining gates before release

1. Measure startup of both real fans together at cold power-on and fault/reset conditions. Repeat at the supply tolerance extremes.
2. Validate representative compliant adapters, including current limiting/recovery and startup overshoot. The requirement may ultimately remain 3 A or increase based on this evidence.
3. Establish maximum auxiliary load, including buzzer and all indicators.
4. Extract protection/cable/PCB resistance and check the existing F1 2920L260/24DR and Q1 DMPH4029LFGQ at enclosure temperature. Current/time and thermal behavior are absent here.
5. Confirm MCU brownout/reset and 3.3/5 V rail sequencing during load steps; no thermal or cold-start rail model is present.

Increasing the supply to 4 A alone does not close these gates. Manufacturing files and existing protection components remain unchanged.
