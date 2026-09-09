# ThermoLoop common 90 x 75 mm layout

## 9 September routing cleanup — current layout

Both actual PCB files now put the 2 mm-wide protected 12 V distribution trunk toward the right outer edge, with the 5 V regulator section inward of it. U3, C14, C15 and R27 moved 8 mm left and 7 mm up in both variants. C14 was rotated 180 degrees to bring its input connection toward the outer 12 V feed; it remains the same non-polar ceramic capacitor. All other footprint locations, the 90 x 75 mm outline and the 78 x 63 mm mounting-hole pitch are unchanged. Every pad retains its original net and all 54 common footprint placements still match.

Total 5 V trace length fell from 62.367 to 44.532 mm on the one-fan board, and from 116.373 to 83.967 mm on the two-fan board. This is a layout measurement, not measured EMC performance. Saved-file DRC reports 0 violations, 0 unconnected items and 0 schematic parity mismatches on both boards. Schematics and BOMs are unchanged. Gerbers, drills, source/fabrication ZIPs and placement exports were refreshed; use the new CPL because C14's orientation and the four relocated components changed. `Audit/rail-cleanup-DRC.json` and `Audit/rail-cleanup-verification.json` supersede earlier coordinate/hash evidence. Pre-cleanup copies are retained at `C:\Users\ersinaytac\Documents\ChatGPT\ThermoLoo[\rail-cleanup\before`.

The initial extension placement described below is historical: the regulator is no longer on the outer side of the 12 V trunk. The physical qualification requirements below remain open.

Published to the actual project files: 9 September 2026. This supersedes the 8 September single-fan-only layout note. Earlier working-copy validation did not mean the files had been published; publication was completed and independently rechecked on 9 September.

## Implemented in both variants

- `1 Fan 2 Th` and `2 Fan 2 Th` now have an identical **90 x 75 mm** outline, extended 10 mm on the right from the original 80 x 75 mm outline.
- M3 mounting-hole centers are 6 mm from their adjacent edges. Hole-center pitch is **78 x 63 mm**. The two right-hand holes moved 10 mm right; left-hand holes and all existing connector positions stayed unchanged. Existing 80 mm enclosure hole patterns are no longer compatible.
- All **54 shared footprints** have identical position, rotation, value and footprint assignment. The one-fan board reserves the same physical area for the omitted second-fan circuitry. Its previous new regulator/driver placement was relocated to this family layout.
- Common U3 TPS7B6950QDBVRQ1, C14/C15 (10 uF / 50 V), and R27 (330 ohms / 125 mW) occupy the right-hand extension. This is a PWM-signal-only 5 V supply; fan motors still use protected 12 V and the MCU remains at 3.3 V.
- Fan 1 uses U4 SN74AHCT1G04DBVR, C16 (100 nF), R26 (33 ohms), and existing R4/R3. Fan 2 uses identical U5/C17/R28 with existing R18/R19. Q2/Q3 are removed. The second-fan tach pull-up's 3.3 V route was rerouted, without changing its electrical connections.
- The logo and affected reference labels were moved to avoid the second fan and its driver. No design-rule relaxations were introduced.
- The two-fan schematic uses an A3 sheet with the new 5 V and two-driver blocks on the right. The one-fan schematic's circuit is unchanged from its preceding 5 V revision.

## Saved-file validation

| Check | 1 fan / 2 thermistors | 2 fans / 2 thermistors |
|---|---|---|
| Native ERC, all severities under existing rules | 0 violations | 0 violations |
| Native DRC, refilled zones and schematic parity | 0 violations | 0 violations |
| Unconnected items / parity mismatches | 0 / 0 | 0 / 0 |
| Electrical parts / BOM / CPL coverage | 50 / exact / exact | 63 / exact / exact |
| Every electrical pad net vs native netlist | Match | Match |
| Gerber ZIP contents vs current exported files | 10 entries match | 10 entries match |
| Source ZIP contents vs current source files | 5 entries match | 5 entries match |

Actual project source text was compared with the checked candidates. Published BOM/CPL rows were compared with generated rows, and every ZIP member was byte-compared with its current file. Audit JSONs beside each project record the saved-file checks; `family-verification.json` contains current source SHA-256 hashes, coordinates and commonality checks.

Fabrication upload is each variant's `Gerbers/<variant>.zip`, not its root source ZIP. BOM is `<variant>.csv`; JLCPCB placement is `Assembly/1_Fan_2_Th_JLCPCB_CPL.csv` or `Assembly/2_Fan_2_Th_JLCPCB_CPL.csv`. Both native placement exports, drill files, Gerbers and ZIPs were refreshed. Source ZIPs include the local `ThermoLoop_PWM.kicad_sym` and `sym-lib-table`.

## Qualification still required

This is a digital design check, not a physical-operation or unconditional production guarantee. The earlier hosted GitHub Action runs do not cover this revision; they were not rerun. Firmware remains to be written and tested for 35–65 C behavior, inverted 25 kHz drive, safe sensor-fault responses, startup and fan-stall handling. With supplies established, an MCU-reset/input-low condition commands full speed; this does not guarantee operation with a failed 5 V rail.

Use an engineering first article to check the actual Noctua fan(s), cable waveforms and overshoot, power sequencing, closed-enclosure temperature, fuse derating and combined two-fan load. The shared rail's 330-ohm load was selected to exceed two fan inputs' combined specified 10 mA maximum pull-up current; worst-case nominal-design resistor dissipation is about 81 mW. Confirm temperature derating in the actual enclosure. Final PSU, JLCPCB stock/substitutions, rotation preview, assembly service for connectors/header, tooling/fiducials, finish and manufacturing revision remain order-time checks. Existing Gerber job metadata does not select a final finish or meaningful revision automatically.

The future 1-fan/1-thermistor variant should derive from this **same outline and component-coordinate baseline**, omitting the unused sensor channel without compacting the PCB. It has not been generated in this change.

Pre-change backups remain at `C:\Users\ersinaytac\Documents\ChatGPT\ThermoLoo[\family-pwm\before`. No purchase, Git commit or push was made. Computer Use was used to reopen and inspect the actual KiCad boards.
