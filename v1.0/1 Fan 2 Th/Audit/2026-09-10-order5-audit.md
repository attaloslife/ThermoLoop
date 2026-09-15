# 1 fan / 2 thermistors: five-board assembly audit

> Update, 10 September 2026, 09:32: F1 is resolved. At the user's request, both the fabrication ZIP and source ZIP were refreshed. All ten fabrication members match fresh exports of the audited current board, ignoring generation timestamps; archive integrity and exact member contents were verified. The corrected front silkscreen is included. New fabrication SHA-256: `ed7ffe0186ccf07d85ce17daeb5e828e99f3fd0624826ca531708933a746f389`. New source ZIP SHA-256: `92a93a1fe78fcef564229994da386eb90f2ea4daa0f06cd4503d0863c005f5ab`. Previous ZIPs and loose Gerbers are backed up at `C:\Users\ersinaytac\Documents\ChatGPT\ThermoLoo[\zip-refresh\backup-20260910-093209`. No schematic or PCB changes were made. The historical hold and hashes below describe the pre-refresh package; the other firmware, assembly and thermal qualification conditions remain open.

Date: 10 September 2026. Scope: saved 90 x 75 mm design, current BOM/CPL and existing fabrication ZIP. No circuit, layout or manufacturing files were changed by this audit. Simulation result logs were regenerated.

## Decision

**HOLD the current manufacturing package for a front-silkscreen refresh. No confirmed electrical connectivity or critical pin-assignment defect was found in the checks below. This is a candidate for five engineering prototypes, not an unconditional guarantee of operation or production qualification.**

There is no compiled firmware in the repository. Assembled boards will not perform the requested temperature control until programmed and tested. The simulation controller is not firmware.

## Findings and required actions

### F1 - Existing fabrication ZIP contains an older front silkscreen

Confidence: high; fresh native exports and independent Gerber rendering.

`Gerbers/1 Fan 2 Th.zip` contains a front silkscreen dated 9 September, 09:01. It lacks the current Cyprus graphic and `Designed in Cyprus`, keeps the ThermoLoop title at the upper left instead of below the lower-right logo, and has previous reference/connector-label positions. Both the ZIP and loose Gerber directory contain that older version.

Fresh copper, solder masks, edge cuts, both drills, back silkscreen and job file match the ZIP after removing creation timestamps. Only front silkscreen differs. Thus this finding does **not** indicate stale copper or missing 5 V routing. It does prevent saying the package represents the current saved PCB in full.

Action before ordering: regenerate the complete fabrication package from the saved board using the stored plot settings, independently recheck the layers, then replace the upload ZIP. Do not upload the root source archive by mistake. The audit generated comparison exports only, without replacing the user's manufacturing package.

### F2 - Firmware and programming plan are still missing

Confidence: high; repository search and current simulation scope.

Required before a working temperature controller can be delivered:

- Implement the 1F/2TH sensor-selection policy. The simulation uses the hotter sensor; that remains a provisional choice to confirm.
- Implement 35 C start and 65 C full-command endpoints, hysteresis, startup/restart boost, open/short sensor handling, tach/stall supervision, LEDs and active buzzer.
- Use approximately 25 kHz PWM with inverted polarity for U4. With established rails, MCU reset/high impedance lets R3 pull U4 input low, commanding fan PWM high/full speed. This does not protect against every 5 V rail or power-sequencing failure.
- PB0 is the fan PWM output, PC0 tach, PA6/PA7 the two ADC inputs, PA0 UPDI and PC3 buzzer. Native netlist pin assignments were checked. Avoid alternate peripheral mappings that conflict with the LED GPIOs.
- Choose a clock supported at 3.3 V: a conservative 10 MHz operating clock is appropriate for the reviewed datasheet; do not assume the advertised 20 MHz maximum is valid at this supply voltage. Configure ADC acquisition time/reference, watchdog and brownout behaviour deliberately.
- Plan 3.3 V-compatible UPDI programming through J2. Pin 1 is 3V3, pin 2 UPDI, pin 3 GND. Do not inject 5 V onto 3V3 or back-power the unpowered regulator from a programmer without a verified power arrangement. Preserve UPDI fuse access.

JLCPCB soldering the MCU is not evidence that application firmware will be loaded. Arrange programming explicitly or program the prototypes after delivery.

### F3 - Sealed-enclosure thermal limits remain unqualified

Confidence: high for dissipation calculations; actual temperatures unknown.

- R27 is the **330 ohm rail-bleed resistor**, not one of the 150 ohm LED resistors. Worst-case dissipation at 5.15 V and -1% resistance is `5.15^2 / 326.7 = 81.2 mW`, 65% of its 125 mW nominal rating. This is not a demonstrated failure, but needs temperature derating. For family robustness, consider a verified higher-power 330 ohm part, preferably in the same 0805 footprint if its manufacturer's thermal rating supports the actual mounting conditions. Do not change resistance or substitute a part without rechecking minimum load and procurement data.
- U3 dissipates about 0.164 W at an illustrative 13.2 V input and 20 mA rail load. TI's package thermal resistance is board-condition-dependent; it cannot certify the temperature of this two-layer board in a sealed box.
- U1's dissipation at 13.2 V is about 0.248 W at 25 mA output, or 0.396 W at 40 mA. Four illuminated indicators plus MCU load make this worth measuring. Its 300 mA headline does not imply that 300 mA is thermally usable from 12 V. Reviewed CJ7533S limits are 85 C ambient and 125 C junction.
- The selected APEM QS63YYRG02 lists an operating-temperature maximum of **65 C at the indicator**. Keep the panel indicator within its rating. A remote thermistor reaching 65 C is not the same as the indicator or PCB reaching 65 C.
- Confirm fuse hold-current derating, electrolytic life and enclosure temperature with actual hardware. The control endpoint of 65 C is not a safety ceiling and was not treated as one.

### F4 - JLCPCB assembly review and harnesses remain release gates

Confidence: high that these checks are outstanding; no supplier-order preview was submitted or approved.

- BOM has 50 components; CPL has the same 50. There are 49 SMD components and one THT programming header, J2. Confirm whether JLCPCB will assemble J2 or whether it will be hand-soldered.
- Verify exact MPN/C-code matches, availability for the order and substitutions in JLCPCB's component-selection page. The lifecycle analyzer returned unknown statuses, not supply-chain clearance. Distributor inventory is not a guarantee of JLCPCB assembly stock.
- Check their placement preview against pin 1 and polarity for U1/U2/U3/U4, Q1/Q4, C1 and D1, and every keyed connector. CPL angles match KiCad but that does not prove JLCPCB's library rotation convention matches.
- No dedicated fiducials are present. Agree on supplier-added tooling rails, fiducials and tooling holes for the selected assembly service, without changing the common finished 90 x 75 mm outline.
- Confirm copper weight, board thickness, finish and soldering/stencil treatment, including Q1's exposed-drain land. Job metadata still has an unspecified finish/revision; explicitly identify the approved order revision.
- Noctua's PC fan connector does not directly mate with the Micro-Fit board connector. Prepare and continuity-test the adapter harness. External fan, thermistors, panel indicators and buzzer are not included simply because their board connectors are in the BOM.
- Check the actual enclosure, screws, washers, connector housings and cable bend/strain relief. The top render lacks some connector 3D models and cannot prove housing clearance. Keep metalwork away from live copper; do not assume non-plated mounting holes bond the aluminium enclosure to GND.

### F5 - Documentation and robustness improvements

U1's schematic datasheet field still refers to an MCP1703-family document although the BOM selects CJ7533S. Manual review used the actual CJ7533S pinout: 1 GND, 2 IN, 3 OUT. Correct the metadata to avoid a future mistaken substitution; no replacement regulator was assumed.

There are no dedicated test points and little external-port ESD protection. Existing pads/header permit engineering bring-up, but long exposed cables, hot-plugging and industrial noise need a defined environment and additional qualification. A sealed metal box alone is not EMC qualification. Optional stitching-via/test-point improvements should be propagated deliberately across the family, not applied automatically during this audit.

## Checks completed

| Check | Result and limitation |
|---|---|
| Native KiCad 10.0.5 ERC, all severities | 0 violations |
| Native DRC, refilled zones, all track errors, schematic parity | 0 violations, 0 unconnected items, 0 parity issues; board not saved by DRC |
| Electrical footprint pads vs native XML nets | All checked numbered electrical pads match; mechanical and paste-only pads are handled separately |
| Schematic vs footprint identifiers | No mismatches |
| Native vs open-source analyzer net partitions | No missing native connected-net groups |
| BOM refs/quantity/value/package/C-code/MPN | 50 components, no mismatches |
| CPL refs/coordinates/rotation/layer | Same 50 components, no mismatches against PCB; supplier orientation still pending |
| Existing ZIP vs loose Gerbers | All members match, but both share the stale front silk |
| Fresh exports vs ZIP | 9/10 members match ignoring timestamp; front silk differs |
| Independent Gerber rendering | Confirms front-silk content/position differences, not merely byte ordering |
| Geometry | Edge-cut centreline extents 90 x 75 mm; mounting pitch 78 x 63 mm. Job bounding box adds stroke width |
| Simulation rerun | Limited model checks pass; not hardware or compiled firmware |

Existing rule exclusions were not changed: DRC ignores symbol footprint-filter compatibility; ERC also ignores four-way junction, single-global-label and simulation-model categories. There are no individual DRC exclusions. Global minimum clearance is zero but all configured netclasses require 0.2 mm; minimum track width is 0.2 mm and copper-to-edge clearance 0.5 mm. Passing these rules does not replace JLCPCB DFM.

## Circuit review summary

**Power:** J1 pin 1 supplies VIN_RAW, then F1, then Q1's drain side; Q1 source feeds VIN_PROTECTED. D1 clamps source-to-gate voltage with correct polarity. Q1's shared drain pad geometry is consistent with its package. At an illustrative 0.6 A and 45 milliohms, Q1 loss is about 16 mW; generic demands for five thermal vias are not evidence of overheating here. D2 is a 15 V-standoff TVS, not a precise 13.2 V overvoltage limiter. Use a suitable regulated 12 V supply; the fan remains directly supplied and is not made safe for higher voltages by PWM. A 12 V/3 A supply remains a provisional family target, not a measured startup guarantee.

**5 V PWM:** U3 pin 1 receives protected input, pins 3/4 GND, pin 5 the 5 V rail, pin 2 NC. U4 pins 2/3/4/5 are input/GND/output/5 V, pin 1 NC. Its TTL-compatible input accepts 3.3 V logic. R26 is 33 ohms in series with the fan signal, with local C16 decoupling. TI's 0.44 V low-level bound at 8 mA plus a 5 mA fan pull-up through 33 ohms gives an illustrative conservative low below about 0.61 V, within Noctua's 0.8 V limit. Scope the actual cable to check overshoot and edge timing; do not treat this DC calculation as a waveform measurement. U3's specified output range is 4.85-5.15 V under its specified conditions, below the fan's 5.25 V input maximum before considering overshoot. C15 must retain at least 2.2 uF effective capacitance and meet TI's ESR range; nominal 10 uF/50 V is not a substituted-part guarantee. R27's minimum load is about 14.55 mA, providing steady-state bleed margin for up to two 5 mA fan pull-ups; this is not a proof for arbitrary power sequencing.

**Sensors/tach:** Each 10 kohm NTC forms a divider with a 10 kohm pull-up, followed by a 1 kohm/100 nF ADC filter. Both channels reach the intended ADC pins. Nominal beta-model voltages are 1.65 V at 25 C, 1.345 V at 35 C and 0.672 V at 65 C. Open circuit reads high and short reads low; firmware must diagnose both. Use a supply-referenced/ratiometric ADC conversion. Tach has a 3.3 V pull-up and series/filter network, and reaches PC0. Noctua specifies two tach pulses per revolution.

**Indicators/buzzer:** All eight LED resistors are 150 ohms. Each two-wire bicolour indicator sees two in series, so total resistance is 300 ohms. Current is roughly 4 mA for a 2.1 V LED at ideal 3.3 V GPIO drive, less after GPIO drop; brightness is not guaranteed at the manufacturer's 20 mA characterization level. Drive opposite GPIO states to select colour, equal states for off. The lack of a common ground at J5 is intentional. J8 pin 1 is protected supply, pin 2 the Q4 drain-switched return. AO3400A gate/source/drain assignment is correct for this active piezo indicator; use DC enable rather than assuming it requires an audio-frequency drive. Manufacturer search data identifies CPE-270 as 12 V, 6 mA; full current-page/PDF retrieval was blocked, so its complete environmental specification was not freshly validated.

## Open-source tools and honest coverage

Used local `kicad-happy` commit `3cf837b2d6577d1369a45a36d5e9bac0e06ff5b6`: schematic, PCB, Gerber, cross-analysis, EMC, thermal and lifecycle analyzers. Its review skill led to checking raw findings, datasheet gaps and export evidence rather than accepting aggregate readiness labels. Also used Gerbonara for independent Gerber parsing/rendering. KiBot was researched as an additional reproducible ERC/DRC/export automation option, but was not installed or run.

- Schematic warnings about missing declared VIN sources reflect passive fuse/MOSFET paths; native connectivity was checked. J5 no-ground warning reflects intentional differential bicolour wiring. R27 derating warning is retained above.
- PCB warnings include fiducials, test points, a J1/MH1 bounding-box courtyard contact, J4 silk, and generic Q1 thermal-via guidance. Native DRC does not show a physical courtyard violation; verify real screws/connectors anyway. Silk is mask-clipped during export.
- EMC reports an error-level heuristic for 62.5% ground coverage along the 7.2 mm UPDI route, plus missing stitching at several transitions including PWM. These are improvement/test concerns, not proof of a nonfunctional board, and not EMC certification.
- The thermal analyzer assessed **zero components** because it had no populated extraction cache. Its zero findings are **not** a thermal pass. Manual calculations above are estimates; enclosure ambient remains unspecified. The analyzer's entered 65 C ambient is a scenario, not a user-confirmed operating condition.
- The lifecycle analyzer could not determine lifecycle status. Its result does not approve sourcing.
- The toolkit SPICE runner could not find a standalone simulator executable. The existing project simulation was rerun using KiCad's ngspice DLL instead. It passed 28 provisional supervisor assertion groups, 18 startup envelope scenarios and the existing supply/temperature studies. Fan/inverter models are simplified, supplies idealized, and firmware/peripheral timing is not simulated.
- Earlier hosted GitHub Action run `34126426159` applies to a previous hardware revision. No new workflow was pushed or dispatched in this audit; local checks must not be presented as a fresh hosted run.

## Harness map for continuity testing

| Connector | Wiring |
|---|---|
| J1 | 1: +12 V input; 2: GND |
| J4 | 1: fan GND; 2: fan +12 V; 3: tach; 4: PWM |
| J3 / J7 | 1: thermistor signal; 2: GND; NTC itself is non-polar |
| J8 | 1: buzzer positive; 2: switched negative |
| J2 | 1: 3V3; 2: UPDI; 3: GND |
| J5 | SYS 1/6; FAN1 2/7; TH1 3/8; TH2 5/10; 4/9 unused |

Pin numbers refer to the PCB footprint, not a guessed cable-view orientation. Verify mating-connector drawings and continuity before connecting power.

## First-article acceptance plan

1. Inspect soldering, exact parts, polarity and keyed connector orientations. Check rail-to-ground resistance before applying power.
2. With external loads disconnected, power at 12 V with a conservative bench current limit. Measure protected 12 V, 3.3 V and 5 V, idle current and regulator heating. A blank MCU is not a functional controller test.
3. Program via compatible UPDI; verify firmware/fuses/readback and reset/watchdog/brownout recovery.
4. Use precision resistor substitutes near 10 kohms, 6.88 kohms and 2.56 kohms to check nominal 25/35/65 C readings and control decisions; this is verification, not per-sensor calibration. Then test both actual NTCs, open/short faults and the selected two-sensor policy.
5. Connect the real Noctua fan through the checked harness. Scope PWM at the fan connector: target 25 kHz, 21-28 kHz range, low <=0.8 V, high/overshoot within Noctua's limits and never above 5.25 V. Test reset, ramping, zero/full command, stall, reconnection and power cycling.
6. Confirm each indicator's colour/off state and usable brightness, buzzer operation and fault indication.
7. Test with the intended PSU/cables and in the closed enclosure at the worst expected ambient and supply voltage. Log rail dips, startup behaviour and temperatures of U1, U3, R27, F1 and C1. Verify indicator temperature too. Do not infer a universal supply requirement solely from the assumed startup-current model.
8. Repeat essential electrical/programming/functional checks on all five boards. Only expand production after first-article evidence closes the open risks.

## Evidence and provenance

Detailed local evidence: `C:\Users\ersinaytac\Documents\ChatGPT\ThermoLoo[\order5-audit` (ERC/DRC JSON, native XML, analyzers, verification.json, export-comparison.json, fresh exports, silk render pairs and board top render). Simulation evidence: `v1.0/Simulation/results`. Manufacturing hashes were unchanged after checks:

| File | SHA-256 |
|---|---|
| 1 Fan 2 Th.kicad_sch | f465de423ad463fdd50da84313405ec68badc5d6bfd035d8283f12bd3d6897bc |
| 1 Fan 2 Th.kicad_pcb | da7c263515e071cfce6b557b5736f583ac11e6a4439dbc39ccd447f2426b4af5 |
| 1 Fan 2 Th.csv | 2d11bb84a72268692cbd33a79bbf8b96fb452a39f62154f196e5747e0a46dfc7 |
| JLCPCB CPL | 01f25d1b7bdec7c69919d6aa7aab5d43e4edcc28b4446f1c6f3db37e90def154 |
| Existing Gerber ZIP, pending refresh | 0ecfd179189903ad2c17672571582cf5c59d423598f1cc5aee6f9e9c6d8d9904 |

Sources: [TI inverter](https://www.ti.com/lit/ds/symlink/sn74ahct1g04.pdf), [TI regulator](https://www.ti.com/lit/ds/symlink/tps7b69-q1.pdf), [Noctua PWM](https://cdn.noctua.at/media/Noctua_PWM_specifications_white_paper.pdf), [Noctua fan](https://www.noctua.at/en/products/nf-a14-industrialppc-3000-pwm/specifications), [APEM exact indicator](https://www.apem.com/led-indicators/snap-in-plastic-led-indicators/qs/qs63yyrg02), [Microchip device](https://www.microchip.com/en-us/product/attiny1616), [R27 assembly listing](https://jlcpcb.com/partdetail/18318-0805W8F3300T5E/C17630), [JLCPCB rails/fiducials](https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order), [JLCPCB placement orientation](https://github.com/JLCPCB/JLCPCB-SMT-Assembly-Components-orientation-fix), [kicad-happy](https://github.com/aklofas/kicad-happy), [KiBot](https://github.com/INTI-CMNB/KiBot).

Package-review sources also include the local manufacturer PDFs in `final-audit-evidence/datasheets`: CJ7533S, DMPH4029LFGQ, AO3400A, ATtiny1616, Eaton-NRM and Noctua-PWM. CJ7533S and Q1 pinout pages were rendered and visually inspected; the ATtiny pinout and multiplex table were checked in extracted text. No claim is made that every component has a newly fetched, fully validated datasheet model.
