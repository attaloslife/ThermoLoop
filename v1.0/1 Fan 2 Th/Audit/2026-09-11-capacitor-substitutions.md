# Capacitor sourcing substitutions - 1 Fan 2 Thermistor

User authorized footprint-compatible equivalents on 2026-09-11.

| Reference | Previous MPN / JLCPCB | Replacement MPN / JLCPCB |
|---|---|---|
| C7 | Yageo AC0805KPX7R9BB102 / C5576121 | Samsung CL21B102KBCNNNC / C46653 |
| C8, C14, C15 | Samsung CL32B106KBVZNWE / C5596896 | Samsung CL32B106KBJNNNE / C138687 |

C7 remains 1 nF, 50 V, X7R, +/-10%, 0805. Replacement dimensions are 2.00 +/-0.10 x 1.25 +/-0.10 x 0.85 +/-0.10 mm. The original automotive-grade Yageo part is replaced by a general-purpose Samsung part; this project is not an automotive-qualified assembly.

C8/C14/C15 remain 10 uF, 50 V, X7R, +/-10%, 1210. Replacement dimensions are 3.20 +/-0.30 x 2.50 +/-0.20 x 2.50 +/-0.20 mm. Same land pattern; maximum component height 2.70 mm.

Manufacturer typical DC-bias plot for CL32B106KBJNNNE was visually inspected. Capacitance is approximately 9-10 uF at 5 V and approximately 7 uF at 13.2 V. C15 therefore retains substantial margin above the TPS7B6950 output-capacitance minimum of 2.2 uF, including ordinary tolerance/temperature allowance. Typical curves are not guaranteed worst-case production limits; bench validation remains required.

Sources:
- https://product.samsungsem.com/mlcc/CL21B102KBCNNN.do
- https://product.samsungsem.com/mlcc/CL32B106KBJNNN.do

Live JLCPCB draft showed 1,798,792 C46653 and 179,439 C138687 in public stock when selected; stock is not reserved until ordering. After substitution, 28/28 BOM lines were confirmed, no shortage listed, and the four repeated two-pin connector rows remained selected. Required replacement quantities: 5 C7 and 15 C8/C14/C15 for five boards. Draft URL:
https://cart.jlcpcb.com/smt-order/?pcbFileNo=47d2f9c87e164a3ba99630d288484f80

Schematic, PCB and BOM metadata updated for this 1F/2TH variant only. A normalized before/after comparison verified that native schematic and PCB differ only in MPN, JLCPCB and Manufacturer strings. No footprint, track, pad, net, position, outline, or component value changes. Gerbers and CPL remain unchanged. Source archive updated. Prior files backed up in the task workspace capacitor-backup-20260911 directory.

This resolves component sourcing shortages, not final assembly approval. Placement/orientation review, firmware, and physical bring-up remain separate gates. No order submitted or paid.
