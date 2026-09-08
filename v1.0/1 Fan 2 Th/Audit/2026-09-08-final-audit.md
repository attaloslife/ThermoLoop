# ThermoLoop 1 Fan / 2 Thermistors — final design audit

> Revision notice: this report describes the pre-change circuit. A subsequent 5 V push-pull PWM revision replaces Q2 and increases the electrical component count to 50. See [the revision and validation note](2026-09-08-5V-PWM-revision.md) for current files and checks. The hosted Action run below does not cover the subsequent revision. Firmware and enclosure qualification remain open.

Date: 8 September 2026. Status: HOLD unconditional production release.

The saved design has no confirmed electrical connectivity or pin-assignment defect from this audit. Native checks and manufacturing-file consistency checks pass. This is not proof of reliable operation with the final fan, harness, enclosure and firmware. A small engineering first-article build is the next validation stage; do not treat this report as approval for a production batch.

No schematic, PCB, BOM, CPL or Gerber changes were made by this audit. This report is an added audit artifact. The requested hosted action was run on a separate `codex/final-1f2th-audit-20260907` branch, not merged into main.

## Scope and reproducibility

- Design: `v1.0/1 Fan 2 Th`, repository commit `5f539bf42e2ca10e53855e7c8b6fc5d4256c298c`.
- Noctua NF-A14 industrialPPC-3000 PWM, 12 V version; Eaton NRMF104F3435B2J.
- User intends an airtight, probably aluminium enclosure; no firmware exists yet.
- Requested control: begin running at sensed 35 °C, reach full fan command at 65 °C.
- Power-supply model, maximum internal PCB ambient, final LED panel and buzzer remain unspecified.
- KiCad 10.0.5 native checks, exported native netlist, manual component/datasheet review, board render and raw pad/net checks.
- Requested kicad-happy KiCad, LCSC and EMC workflows used; action pinned to `3cf837b2d6577d1369a45a36d5e9bac0e06ff5b6`.
- Actual [hosted run 34126426159](https://github.com/attaloslife/ThermoLoop/actions/runs/34126426159) succeeded; raw artifacts, not only its headline, were inspected.
- Audit applies to saved files. Unsaved changes in an open KiCad window are not covered.

## Verification results

| Check | Result / limitation |
|---|---|
| Native schematic ERC | 0 reported violations under project settings |
| Native PCB DRC, refilled zones, schematic parity | 0 violations, 0 unconnected items, 0 parity mismatches |
| Every electrical pad net against native schematic netlist | Match |
| Independent analyzer net partitions against native netlist | Match |
| BOM and CPL reference coverage | 44 electrical components in each; no missing or extra references |
| BOM values, footprints and C-codes against design | Match; this does not validate supplier substitutions |
| CPL raw coordinates, side and rotations against saved footprints | Match; JLC machine-library orientation still needs preview approval |
| Existing ZIP versus fresh manufacturing exports | All 10 files match after removing timestamp lines only |
| Hosted extended SPICE | 9 pass; generic models and extracted subcircuits, not a complete working controller simulation |
| Hosted thermal analysis | Skipped: 0 components assessed; no thermal clearance can be claimed |
| LCSC lifecycle-only audit | 18 unique parts returned unknown; not a stock/lifecycle approval |
| Deep-review evidence gate | 4 findings accepted, 0 quarantined; 1 partial automated source check |

Native DRC ignores the footprint-filter mismatch category; native ERC also ignores single-global-label, four-way-junction, simulation-model and footprint-filter categories. Actual electrical pads and assigned footprints were independently compared. There are no excluded PCB DRC violations in the output. Passing checks remain conditional on the configured design rules.

Board: 80 × 75 mm outline, two copper layers, 1.6 mm thickness, nominal 1 oz copper, 44 electrical footprints plus four mounting holes. Electrical parts are 43 SMD and one THT. Six Micro-Fit connectors are SMD; only J2 is a through-hole header. Any earlier statement that all seven connectors were THT was incorrect.

## Release findings

### 1. PWM interface requires qualification — high priority

U2 PB0 drives Q2 through R4; R3 pulls the gate down. Q2's source is grounded and its drain goes to J4 pin 4. This is an open-drain, inverting PWM interface. The AO3400A is suitably enhanced at a 3.3 V gate voltage and can pull the fan input low. However, there is no active rising-edge drive: the fan's internal source must charge the line and transistor capacitance.

[Noctua's PWM whitepaper](https://cdn.noctua.at/media/Noctua_PWM_specifications_white_paper.pdf), page 8, recommends a CMOS drive arrangement and cautions against pull-down-only open-collector designs. Q2 is an NMOS, not the pictured bipolar transistor; that distinction prevents declaring definite failure, but does not establish the rising waveform. Internal pull-up strength and harness capacitance have not been measured.

Before a production batch, either qualify this exact circuit with the actual fan and intended cable, or revise to a suitable actively driven interface and re-audit it. Do not add an arbitrary pull-up voltage or connect the fan PWM input to 12 V. Test 25 kHz PWM at the fan connector, especially low commands, restart, 100% command and power cycling. Noctua specifies a target of 25 kHz with a 21–28 kHz range and a maximum low input level of 0.8 V; use the complete manufacturer limits during the test.

The transistor inverts the command: MCU high pulls fan PWM low; MCU low releases it high. With MCU pins high-impedance during reset, the gate pulldown releases PWM, providing the full-speed hardware default with a powered compatible fan. This is not a complete safety mechanism against arbitrary MCU/output faults.

### 2. Firmware is required before this is a temperature controller

JLC assembly of a blank MCU will not implement the requested curve. Programme and verify U2 through UPDI, using 3.3 V-compatible programming equipment and a defined power arrangement that avoids backfeeding.

Recommended firmware requirements, not implemented by this audit:

- Configure a clock valid at 3.3 V; 10 MHz is a conservative supported choice. Do not assume the 20 MHz maximum is valid at this supply.
- Use PB0/TCA WO0 for 25 kHz PWM, accounting for Q2 inversion. Leave unrelated TCA outputs disabled.
- Read TH1 on PA6 and TH2 on PA7; use a VDD-referenced ADC for ratiometric divider readings.
- Recommend controlling from the hotter valid sensor; confirm this policy before implementation.
- Below the start threshold, stop if intended; at 35 °C command at least a tested reliable starting duty, not an infinitesimal duty.
- Ramp from that minimum running command to 100% at 65 °C. Add hysteresis, filtering and a startup kick verified on the real fan.
- Treat an open or shorted sensor as a fault, command full cooling and indicate an alarm. Do not silently discard the hotter sensor when it faults.
- Monitor PC0 tachometer input; Noctua's two pulses per revolution imply RPM = 30 × frequency in Hz. At 3000 RPM, expect about 100 Hz.
- Include startup grace time, stopped-fan detection, watchdog and deliberate brownout behaviour.

Full fan command at 65 °C is not a guarantee that the controlled object cannot exceed 65 °C. Actual heat load, airflow, sensor mounting, delay and control behaviour determine the temperature. If 65 °C is a hard safety ceiling, an earlier full-speed threshold and independent protection may be necessary.

### 3. Airtight enclosure thermal performance remains unverified

The fan's main current flows on VIN_PROTECTED, not through the 3.3 V regulator. This is correct. Q1's conduction loss is small at the stated fan load: using 0.6 A board current and 45 mΩ gives approximately 16 mW at the stated resistance condition. The automated request for five thermal vias beneath Q1 is not a load-specific requirement.

U1 is the more relevant local heat source. At 13.2 V input its approximate dissipation is 0.158 W at 16 mA, 0.248 W at 25 mA and 0.396 W at 40 mA, excluding small quiescent-current loss. These are scenarios, not measured or guaranteed load bounds. LED selection and firmware affect the actual load.

The CJ7533S datasheet gives a maximum junction temperature of 125 °C and ambient operating range ending at 85 °C. Its nominal package power rating is not a promise that the installed board stays cool in a sealed box. For example, at 65 °C local ambient and 0.248 W, remaining below 125 °C would require effective junction-to-ambient thermal resistance below about 242 K/W, with no design margin.

Heat-soak a first article in the actual closed enclosure at the worst external temperature and heat load, with all relevant LEDs and buzzer operating. Measure local PCB air and regulator temperature; estimate junction temperature with an appropriate package/board model. Verify fan starts, ADC readings and resets throughout. Aluminium material alone does not establish the thermal path.

### 4. JLC assembly approval and harnesses are still required

There are no dedicated board fiducials. Arrange supplier-added process rails/fiducials or add suitable ones to the layout. [JLCPCB's assembly guidance](https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order) requires these for standard assembly. Confirm the selected assembly service handles J2's THT insertion, or explicitly leave J2 for hand soldering.

Before payment, approve each actual manufacturer part/C-code and live availability, grouped-reference import, polarity and pin-1 orientation in JLC's placement preview. Pay particular attention to U1, U2, Q1, D1, C1 and all connectors. A raw CPL match does not prove JLC's package origin/rotation convention matches KiCad's. OEM mechanical drawings and the final mating enclosure/harness assembly are not fully dimensionally signed off here.

The Noctua fan's normal PC connector does not directly mate with the board's Micro-Fit connector. Make and continuity-test a correctly keyed adapter. The Eaton thermistor also requires appropriate lead termination; its fine enamelled leads are not a ready-made Micro-Fit cable. Secure and insulate the leads and provide strain relief.

| Board connection | Pin mapping from saved design |
|---|---|
| J1 power input | 1 = positive 12 V; 2 = GND |
| J4 fan | 1 = GND; 2 = protected 12 V; 3 = tach; 4 = PWM |
| J3 TH1, J7 TH2 | 1 = thermistor signal; 2 = GND; NTC itself is nonpolar |
| J2 programmer | 1 = 3.3 V; 2 = UPDI; 3 = GND |
| J8 buzzer | 1 = protected supply; 2 = switched low side |
| J5 LED pairs | System 1/6; fan 2/7; TH1 3/8; TH2 5/10; 4/9 unused |

Read physical connector pin numbers from the part drawing; do not infer left/right from cable colour or a mirrored mating view. Use insulated spacers and verify screw/washer clearances in the aluminium case. Do not allow its metalwork to contact live copper or connector solder joints.

## Electrical review details

Power path: J1 → F1 → Q1 reverse-polarity stage → direct fan supply and U1. Q1's drain/source orientation supports reverse-polarity protection; D1 limits source-to-gate voltage. The DMPH4029LFGQ power pad is drain, and the saved mapping is consistent with that package. U1 CJ7533S is pin 1 GND, pin 2 input including tab, pin 3 output. Its input/output ceramic capacitors are present. U1's schematic datasheet property incorrectly points to an MCP1703 document; correct that metadata before future maintenance, but it is not the part actually in the BOM.

The [selected Noctua](https://www.noctua.at/en/products/nf-a14-industrialppc-3000-pwm/specifications) is rated 12 V, maximum 0.55 A / 6.6 W, maximum operating voltage 13.2 V. Supply it from regulated 12 V with verified tolerance, startup/transient behaviour and current capacity. A 12 V-labelled unregulated adapter is not enough evidence. The exact supply remains a release input.

F1 is a 2.6 A hold PPTC at its reference temperature, with substantial derating at high ambient; published reference values still exceed this fan's 0.55 A rating at 70–85 °C. It is not a precision 0.55 A motor-current limiter. Its trip response and actual fan startup must be considered with the supply. [Littelfuse 2920L datasheet](https://www.littelfuse.com/assetdocs/2920l_datasheet_update.pdf?assetguid=f237e8c2-1ed9-4c13-a738-dbe0738b3d2c).

D2 SMBJ15CA is transient suppression, not a 13.2 V fan overvoltage regulator. Its 15 V stand-off and 24.4 V specified clamp mean it does not guarantee protection of this fan against an excessive DC supply or every surge. Preserve the intentionally simple matched-voltage architecture, but state the regulated 12 V requirement clearly. [Littelfuse SMBJ datasheet](https://www.littelfuse.com/~/media/electronics/datasheets/tvs_diodes/littelfuse_tvs_diode_smbj_datasheet.pdf.pdf).

Tachometer: R5 pulls the open-collector signal to 3.3 V; R12/C7 provide series filtering. A 100 Hz tach signal is far below that filter's bandwidth. The MCU is not directly pulled to 12 V. Noctua's specified signal interface is compatible with this arrangement.

Sensors: NRMF104F3435B2J is 10 kΩ at 25 °C, not 100 kΩ; Eaton's code uses 1.0 × 10^4. Its nominal beta is 3435 K for 25/85 °C, resistance tolerance ±1%, beta tolerance ±5%. The 10 kΩ pull-ups are appropriate. Each ADC has a 1 kΩ series resistor and 100 nF capacitor. Constant-beta illustrative readings are about 417/1023 at 35 °C and 208/1023 at 65 °C with VDD reference. Use the manufacturer's R/T curve for final conversion, not these rounded counts as calibrated trip points.

Divider self-heating peaks around 0.272 mW; the published 0.8 mW/°C dissipation constant suggests roughly 0.34 °C under its specified conditions. Beta tolerance alone can create errors of a few degrees near the upper threshold, before mounting effects and thermal lag. Calibrate the assembled sensing system if temperature accuracy matters. The effective ADC RC time constant includes the divider resistance and is about 0.51 ms at 35 °C and 0.30 ms at 65 °C. [Eaton NRM datasheet](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-nrm-epoxy-sealed-radial-lead-ntc-thermistor-data-sheet-elx1109-en.pdf); manufacturer PDF was obtained through an LCSC mirror because the original download timed out.

LED panel: each used pair has two 220 Ω resistors in series through the LED, 440 Ω total. It is suitable for four two-lead antiparallel/bicolour LEDs, not an arbitrary common-anode/common-cathode panel. For a 2 V LED, current is about 3 mA. The absence of ground on J5 is intentional for that topology. The final LED assembly must match it; unused 4/9 positions are intentional standardization, not missing connections.

Buzzer: Q4 is a low-side switch, default off. J8 expects a supply-compatible device. A suitable active piezo can work; an inductive magnetic buzzer would require appropriate flyback handling, not established by the present circuit. No unconditional buzzer compatibility claim is possible without its final part number.

## Automated-warning triage

The action's short summary reported no warnings, but raw outputs did. The full EMC analysis returned one error, nine warnings and twelve informational findings, score 85/100; the default lightweight score was 100/100. Neither score is an EMC compliance measurement.

- Schematic: external power/fuse source-inference warnings on VIN_RAW/VIN_FUSED do not contradict native net connectivity; J5 no-ground warning is explained by differential LED pairs.
- PCB: no fiducials needs an assembly plan; J4 silk/pad overlap needs JLC legend clipping/DFM review. Native silk clearance minimum is zero, so clean DRC does not independently clear that legend warning.
- J1/MH1 courtyard overlap was reported with 0.0 mm² area, consistent with a boundary touch; actual case screw/washer clearance remains a mechanical check.
- No dedicated test points: not a functional defect, but prepare accessible probing/programming for the first article and production test.
- Q1 thermal-via warning is a generic footprint heuristic; the actual conduction estimate is small at the intended load, as above.
- Full EMC flags a partial ground reference beneath the short, approximately 7.2 mm UPDI route, and missing nearby return vias for several LED/buzzer/control transitions. These are engineering layout-improvement candidates, not demonstrated runtime failure. Ground stitching near layer changes is recommended for a revision; long external harnesses need practical immunity testing.
- The cross-domain stitching warning assumes a 100 MHz analysis frequency; it is not evidence that this controller operates at that frequency.
- Analyzer graph summaries report extra power-net islands; native refilled-zone DRC reports no unconnected items and pad/net maps match. Do not equate those graph counts with confirmed unrouted connections; the parser-level discrepancy is not independently resolved into a physical open circuit.
- Nine SPICE passes cover three RC filters, Q2/Q4 generic NMOS models, D2 generic diode behaviour, two decoupling networks and one inrush network. The output explicitly warns that real TVS clamping and transistor behaviour need actual models. It does not simulate the full fan or firmware.
- Automated datasheet extraction failed, so thermal and lifecycle outputs do not establish component qualification. Critical datasheets were reviewed manually; live JLC stock and complete OEM dimensional verification remain pending.

## First-article acceptance checklist

1. Inspect population, soldering, polarities and pin 1; check no shorts between input, 3.3 V and ground before applying power.
2. Use a current-limited regulated supply; verify input polarity, 3.3 V rail, MCU programming and idle current. Verify fan connector voltage before plugging the fan in.
3. Confirm full-speed reset/default behaviour, then scope 25 kHz PWM at the actual fan through the final harness across the command range.
4. Verify startup/restart and tach RPM; stall/disconnect the fan safely and confirm the intended alarm response.
5. Substitute known resistances, then use real sensors alongside a reference thermometer at points below, around and above 35/65 °C. Test both sensors and open/short faults separately.
6. Verify all four LED pairs and the selected buzzer, including worst-case current draw.
7. Heat-soak the closed final enclosure under maximum intended conditions; record regulator/PCB temperatures, supply rail, resets, fan speed and sensor error.
8. Test repeated power cycles, brownout recovery and realistic cable handling/ESD conditions. Formal EMC or safety certification requires its own applicable test plan.
9. Approve final JLC BOM, substitutions, rotations, rails/fiducials, THT handling and DFM preview before a production batch.

## Evidence locations and frozen hashes

Full local evidence: `C:\Users\ersinaytac\Documents\ChatGPT\ThermoLoo[\final-audit-evidence`.

Useful files: `erc.json`, `drc.json`, `netlist.xml`, `verification.json`, `final_calculations.py`, `final_calculations.json`, `deep_review.json`, `board-top.png`, downloaded `datasheets`, and `hosted` raw action artifacts. The calculations are transparent approximations, not measurements. The deep-review gate's partial finding reflects unavailable automatic PDF text validation; the Noctua page was read separately.

| File | SHA-256 |
|---|---|
| Schematic | `556ed193fd9474da492f6623ae6ef92b0243fe95273d3b7971d09ab17d144613` |
| PCB | `bcf84b1efc44bbb05f6d3558122c626b6bb957025db62a1c9bf40f01ce7d8a67` |
| BOM | `631d70437e054c6411634c88690d22e4666a40c6e1904e288d4a5a6e093fb1f8` |
| CPL | `fca1d64259dc2235a1a1d5feb73688da2bcf58f51435146f319cfc5c76dad8d4` |
| Gerber ZIP | `06132ef9f8864d08852f4a9985a016fdef38fa1ad2bc4ad96a1bfa7ddde63435` |

Bottom line: the design is electrically plausible and manufacturing files are consistent, but an unconditional statement that it will work is not justified. Close the PWM, firmware, supply/peripheral and assembly decisions, then validate a first article in the real enclosure before releasing a production batch.
