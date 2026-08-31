# ThermoLoop 5V / 1 Fan — JLCPCB assembly notes

## Upload files

- PCB fabrication: `5V_1Fan_JLCPCB_Gerbers.zip`
- Assembly BOM: `5V_1Fan_JLCPCB_BOM.csv`
- Component placement: `5V_1Fan_JLCPCB_CPL.csv`
- Combined convenience archive: `5V_1Fan_JLCPCB_Assembly_Package.zip`

The BOM and CPL each cover the same 19 populated references. H1 and H2 are mechanical mounting holes and are intentionally absent from both files.

## Assembly selections

| References | Manufacturer part | JLCPCB/LCSC |
|---|---|---|
| C1, C2 | Murata GRM21BR71H104KA01L | C77082 |
| C3, C4 | CCTC TCC1206X7R106K160HT | C380363 |
| F1 | Littelfuse 1206L025/24YR | C3762322 |
| J1 | ZHOURI 2.54-1*3 | C5116482 |
| J2 | JST B2B-PH-K-S | C20504437 |
| J3 | Molex 470531000 | C240840 |
| J4 | JST B2B-XH-A(LF)(SN) | C158012 |
| J5 | JST B3B-PH-K-S(LF)(SN) | C131339 |
| Q1 | Yangzhou Yangjie 2N7002 | C389059 |
| Q2 | Alpha & Omega AO3401A | C15127 |
| R1, R4 | Yageo RC0805FR-0710KL | C84376 |
| R2, R5, R6 | Yageo RC0805FR-071KL | C95781 |
| R3 | Yageo RC0805FR-07100KL | C96346 |
| U1 | Microchip ATTINY402-SSF | C1338236 |

## Required order review

- Select top-side PCBA and enable through-hole/wave-solder assembly. J1–J5 are through-hole parts; J3 is an extended wave-soldered part and may require a fixture or extra fee.
- In JLCPCB's parts-matching screen, confirm every C-code and live stock. Supplier stock and basic/extended classifications can change.
- In the placement preview, confirm pin 1 and orientation for U1, Q1, Q2, J1–J5, and F1. The exported CPL uses KiCad's native coordinate system and matches the established ThermoLoop v0.2 JLC format.
- The Eaton NRMF104F3435B2J thermistor is an external 10 kΩ, B25/85 3435 K sensor connected to J2; it is not part of the PCB assembly BOM.
- U1 will arrive blank unless JLCPCB programming is separately arranged. Program it through J1 (UPDI) before functional testing.

## Verification snapshot

- KiCad ERC: 0 errors, 0 warnings
- KiCad DRC: 0 violations
- Unconnected pads: 0
- Schematic/PCB parity issues: 0
- Routing: 14/14 nets complete
- Minimum track width: 0.20 mm
- Power/GND routing used up to 0.80 mm
- Minimum spacing: approximately 0.249 mm
- Vias: five at 0.80/0.30 mm, 0.25 mm annular ring
- Board: 40 × 35 mm, two copper layers

The kicad-happy Gerber gate reports an alignment failure because it compares each layer's drawn-feature bounding box with the full 40 × 35 mm board outline. Copper, mask, and silkscreen do not naturally occupy the full outline. KiCad generated all Gerbers and drill files together from one board/origin, and its DRC/parity checks are clean; do not add duplicate Edge.Cuts graphics to copper layers merely to satisfy this heuristic.
