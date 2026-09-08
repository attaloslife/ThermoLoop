# 5 V PWM revision — 1 fan / 2 thermistors

Date: 8 September 2026. Status: implemented and digitally checked; engineering first-article validation still required. This is not unconditional production approval.

## Implemented circuit

- Added U3 TPS7B6950QDBVRQ1 (C132202), a dedicated 5 V / 150 mA regulator supplied from VIN_PROTECTED. Its rail is for PWM signal drivers only, not fan motors, LEDs or buzzer.
- Replaced Q2 with U4 SN74AHCT1G04DBVR (C30326), a 5 V push-pull inverter accepting the MCU's 3.3 V logic. R4 remains 100 ohms and R3 remains 100 kilohms on its input. Added R26, 33 ohms (C23140), in series with the fan PWM output.
- Added C14/C15, 10 uF / 50 V / 1210 (C5596896, same part as C8), and C16, 100 nF / 50 V / 0805 (C49678, existing family part).
- Added R27, 330 ohms / 1% / 125 mW / 0805 (C17630), as a common rail bleed/minimum load. It draws at least 14.55 mA at 4.85 V, exceeding the combined maximum 10 mA pull-up current of two fan inputs. Its calculated worst-case dissipation is 81.2 mW at 5.15 V and -1% resistance; confirm enclosure-temperature derating during qualification.
- U3 output tolerance is 4.85–5.15 V under its specified operating conditions. Its output capacitor must retain at least 2.2 uF effective capacitance; the selected 10 uF, 50 V part provides nominal margin at 5 V. At 13.2 V input and an illustrative 20 mA rail load, regulator dissipation is approximately 0.164 W, not a measured thermal result.
- MCU supply remains 3.3 V. Fan motor remains directly on protected 12 V. Tachometer, thermistor, LED and buzzer circuits are unchanged.
- KiCad corrected the project sheet display name from the inherited '2 Fan 2 Th' to '1 Fan 2 Th'. No design-rule relaxation was introduced.

Input low gives fan PWM high. Thus the existing input pulldown commands full speed during MCU reset **once the rails are established**. This is not a guarantee against a failed 5 V rail, fan disconnection or all power-sequencing faults. Firmware must use inverted output polarity at approximately 25 kHz. Requested behavior remains start at 35 C and reach full command at 65 C, with sensor-fault handling and startup/restart logic still to be implemented.

## Family standardization

Only the 1F/2TH variant was changed. Board outline, mounting holes, connector positions, MCU allocation, and all 47 retained footprints' position/rotation/value/footprint assignments are unchanged.

| Variant | Shared 5 V section | PWM channels | Status |
|---|---|---|---|
| 1 fan / 2 thermistors | U3, C14, C15, R27 | U4, C16, R26; existing R4/R3 | Implemented |
| 2 fans / 2 thermistors | Reuse identical U3, C14, C15, R27 | Reuse fan 1 section; proposed fan 2 U5/C17/R28 with existing R18/R19 | Not modified; placement/routing and full checks required |
| 1 fan / 1 thermistor | Reuse identical section | Same fan 1 section | Future variant; no board generated |

The second fan's power-path current, fuse derating and connector loading still require separate validation; sizing the PWM rail for two channels does not qualify the two-fan power path. Keep the common local symbol library and stable reference designators when porting this change.

## Verification and evidence

- KiCad 10.0.5 schematic ERC: 0 violations.
- PCB DRC with refilled zones, all severities, all track errors and schematic parity: 0 violations, 0 unconnected items, 0 parity mismatches, under the existing project rules.
- Every electrical footprint pad net compared with the native schematic XML netlist: match. Explicit U3/U4 pin maps checked. All retained original pad nets unchanged except the intended R3/R4 gate-net rename.
- BOM and CPL each cover all 50 electrical components (49 SMD, one THT programming header). Values, footprints and part fields were generated from the revised netlist; raw placement coordinates and rotations match the saved PCB. This does not certify JLCPCB's machine-library rotation convention or current assembly stock.
- Saved schematic reopened and drawing inspected using the Computer Use skill; final PCB top render inspected.
- Evidence is in `5V-PWM-ERC.json`, `5V-PWM-DRC.json`, and `5V-PWM-verification.json` alongside this note. Native checks retain the category exclusions described in the earlier audit; none were relaxed for this change.
- The earlier hosted GitHub Action run 34126426159 applies to the **pre-change** design. It was not rerun for this revision; do not present its thermal/SPICE results as validation of the added circuitry.

## Updated outputs and remaining release gates

- Fabrication ZIP: `../Gerbers/1 Fan 2 Th.zip` (seven Gerber layers, two drill files, job file). Silk export subtracts solder-mask openings. This is the fabrication upload, not the root source ZIP.
- BOM: `../1 Fan 2 Th.csv`. Placement: `../Assembly/1_Fan_2_Th_JLCPCB_CPL.csv`. Native placement export also refreshed.
- Root `../1 Fan 2 Th.zip` refreshed as a source-only archive, including the new local symbol library and table. Previous manufacturing ZIPs are retained in the local staging backup `C:\Users\ersinaytac\Documents\ChatGPT\ThermoLoo[\pwm5v-revision\before-manufacturing`.
- Confirm exact 12 V PSU, JLCPCB component availability/substitutions, pin-1 orientation/rotation in their assembly preview, connector/header assembly service, tooling rails/fiducials, finish and job revision. Gerber job metadata still says `rev?` / finish `None`; select the real manufacturing finish and revision explicitly in the order.
- Before production quantities, scope PWM at the actual Noctua fan connector and cable: low <=0.8 V, high within manufacturer limits, maximum 5.25 V including overshoot, frequency 21–28 kHz (target 25 kHz). Check startup, power cycling, reset, very low duty and full command, including supplies ramping at different rates. Check 5 V rail behavior with one fan and, when ported, both fan inputs.
- Program and validate firmware; check sensor disconnect/short handling, 35–65 C control behavior, stall handling, indicators and active buzzer. No firmware was created by this hardware change.
- Measure temperatures in the closed aluminium enclosure at worst supply voltage and expected ambient; sensed 65 C is not a known PCB ambient. Qualify the original 3.3 V regulator, fuse, new 5 V regulator and bleed resistor as well as the selected panel indicator's temperature rating.

## Component references

- [TI TPS7B69-Q1 datasheet](https://www.ti.com/lit/ds/symlink/tps7b69-q1.pdf)
- [TI SN74AHCT1G04 datasheet](https://www.ti.com/lit/ds/symlink/sn74ahct1g04.pdf)
- [Noctua PWM specification](https://cdn.noctua.at/media/Noctua_PWM_specifications_white_paper.pdf)

