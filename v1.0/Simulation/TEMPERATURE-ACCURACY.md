# Temperature accuracy — first error budget

This is an analytical sensitivity study, not a guaranteed accuracy specification or physical measurement. No manufacturing component values or controller thresholds have been changed.

## Inputs and evidence

Both input channels use 10 kOhm 1% pull-ups, 1 kOhm 1% series resistors and 100 nF 10% filter capacitors. The external Eaton NRMF104F3435B2J is 10 kOhm at 25 C, resistance tolerance 1%, beta 3435 K with 5% tolerance. Eaton lists approximately 0.8 mW/C dissipation coefficient and a thermal time constant up to 10 seconds. [Eaton ELX1109](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-nrm-epoxy-sealed-radial-lead-ntc-thermistor-data-sheet-elx1109-en.pdf)

The ADC study assumes VDD reference, the same supply as the pull-ups. Microchip lists 10-bit resolution and typical (not guaranteed maximum) 2 LSB absolute accuracy with VDD reference. We use +/-2 LSB as a sensitivity case plus a separate conservative half-LSB quantization allowance, which can overlap the absolute-error specification. These are not guaranteed worst-case ADC limits. The datasheet describes ADC sources of about 10 kOhm or less as suitable. [Microchip DS40002204A, sections 30.3.2.4 and 36.16](https://ww1.microchip.com/downloads/en/DeviceDoc/ATtiny1614-16-17-DataSheet-DS40002204A.pdf)

The PDF inspection step identified merged/ambiguous part-number headings in the extracted Eaton R/T table. Visual rendering could not be obtained after download failures, so **the nominal table is NOT incorporated**. No claim is made that the beta approximation exactly reproduces that table. Verification of the correct table and its curve is an open item.

## Executed calculation

`temperature_accuracy.py` evaluates 51 temperatures from 25 to 75 C and 16 sign combinations of R25, beta, pull-up and ADC error. It solves threshold crossings by bisection and checks that inversion reproduces the desired indicated threshold. Full numeric results are in `results/temperature_accuracy.json` and `.csv`; the main runner reproduces this study alongside earlier tests.

| Programmed threshold | Modelled earliest true sensor-bead temperature | Modelled latest |
|---|---:|---:|
| 33 C stop | 31.8 C | 34.3 C |
| 35 C start | 33.7 C | 36.4 C |
| 65 C full speed | 61.8 C | 68.7 C |

These intervals exclude self-heating, thermal lag, mounting error, nominal beta-curve mismatch, resistor temperature coefficients and cable/contact/ground effects. They are not manufacturing pass/fail limits. The corners model constant-beta variation around R25, not a certified full resistance/temperature tolerance envelope.

At true 65 C, positive 5% beta error alone produces about +2.28 C indication error. Positive 1% pull-up error contributes about +0.33 C. Half-LSB quantization contributes about 0.10 C. Thus increasing resolution alone does not address the dominant modeled error. Identical circuitry does not mean the two sensors have identical calibration errors; calibrate each channel separately.

## Heating, filtering and reference

- Estimated nominal self-heating is +0.33 C at 35 C and +0.22 C at 65 C. This is a first-order estimate using the stated dissipation coefficient, not a mounting-independent correction to subtract blindly.
- A hypothetical 10-second sensor time constant at a sustained 0.1 C/s temperature rise gives about 1 C asymptotic lag. Airflow and mounting change this. The bead can lag the protected object even if ADC conversion is accurate.
- Nominal source impedance is about 5.08 kOhm at 35 C and 3.04 kOhm at 65 C. Input-filter time constants are about 0.51 and 0.30 ms. A full-scale electrical step settling to half an LSB takes about 3.9 and 2.3 ms respectively, nominally. This is not a complete ADC sample-and-hold timing model.
- Using VDD as ADC reference ideally cancels steady pull-up supply variation. This does not cancel fast supply changes while the filter capacitor retains its previous voltage, ground noise or reference-path error.
- Separate 1 uA leakage stress cases produce about 0.18–0.19 C error at the endpoints. These are sensitivity assumptions, not guaranteed pin-leakage specifications.

## Recommended next actions

1. Keep the present PCB values for now. Verify the manufacturer's nominal R/T curve before finalizing firmware conversion.
2. Add per-channel two-point calibration near the operating endpoints. A one-point offset does not remove beta/slope error. Calibration residuals and fixture/reference accuracy still need study.
3. Use VDD reference, disable digital input buffers on sensor pins and choose ADC acquisition timing explicitly. Average modestly for noise; avoid filtering that introduces excessive alarm delay.
4. Decide whether 65 C means a normal control endpoint or an absolute maximum protected-object temperature. If it is an absolute ceiling, commanding full speed only at an uncalibrated 65 C indication is insufficient; sensor error, thermal lag and cooling capacity require margin.
5. Verify mounting, thermal response and calibrated accuracy on real assemblies before claiming a product temperature-accuracy specification.

The simulation control model remains unchanged: TH1/FAN1 and TH2/FAN2 are independent, and existing thresholds remain provisional.
