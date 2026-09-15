# JLCPCB placement review - 2026-09-14

Status: NOT RELEASED for manufacture. No order placed or paid.

## Follow-up - 2026-09-15

Regenerated preview recovered. Rechecked C1 positive-left/negative-right; D1 cathode bottom; Q4 gate lower-left and single drain top; U1 pin 1 lower-right; U2/U3/U4 pin 1 upper-left. J2 is vertical and centered over its three holes. J1/J3/J7/J8/J4/J5 models mechanically align, but colored pin markers on the keyed connector models remain ambiguous: final numbered-pin/latch correspondence requires engineering confirmation. No additional rotations or coordinates changed in this follow-up.

Sent Q1 draft reference and screenshot to JLCPCB support with the user's approval. Leo replied that the automated preview is only a reference and engineers adjust placement after ordering. This is not Q1-specific placement signoff or confirmation of a production hold. Require customer approval of final placement before assembly.

Green Economic quote loaded at USD 88.04 excluding shipping/tax, including production-file and placement-confirmation charges. User subsequently requested RED solder mask. Selected Red and continued the settings draft: the site automatically changed to Standard assembly, disabled Economic, and added two 5 mm rails (90 x 85 mm panel around the unchanged 90 x 75 mm PCB). Five PCBs and two assemblies retained in the settings. Depanel-before-delivery remained No; confirm this choice and revised total before purchase. BOM remained 28/28 confirmed, but Standard changes attrition quantities. Red/Standard full quote and regenerated placement review remain pending. No order placed or paid.

Draft: PCB file number 47d2f9c87e164a3ba99630d288484f80, 1 Fan 2 Th.

Red/Standard quote subsequently loaded: PCB USD 6.34 + PCBA USD 104.62 = USD 110.96 before shipping/tax (USD 22.92 above green/Economic). Confirmation charges remain included. Standard assembly build-time choice shows 4-5 days. Saved draft remains at Quote & Order; SAVE TO CART was not clicked. Preview regenerated after color change, but final numbered connector and engineering placement approval are still outstanding.

## Corrections investigated

The initial JLCPCB 2D model preview showed reversed C1 polarity and mismatched IC rotations. Corrections were applied interactively and visually inspected against PCB pads and pin-one markers. They were then encoded in `Assembly/1_Fan_2_Th_JLCPCB_CPL_review.csv`, which was uploaded and processed. The original CPL is preserved unchanged. The review file is provisional until its regenerated preview is checked.

| Reference | Original CPL rotation | Review-file rotation | Reason |
| --- | ---: | ---: | --- |
| C1 | 0 | 180 | Positive terminal must be left, on VIN_PROTECTED; negative terminal right, on GND |
| J2 | 0 | 270 | Header must run vertically along the three holes |
| Q1 | 180 | 90 | Pin 1 must be lower right; model offset still unresolved |
| Q4 | 90 | 270 | Single drain lead top; gate lower left; source lower right |
| U1 | 180 | 90 | Three leads on right; pin 1 lower right |
| U2 | 0 | 270 | Pin 1 upper left; ten leads on each left/right edge |
| U3 | 0 | 270 | Pin 1 upper left; three leads left and two right |
| U4 | 0 | 180 | Pin 1 upper left; three leads left and two right |

J2 midpoint additionally changes from (76.050, -62.455) to (76.050, -64.995) mm. The old point was pin 1, not the centroid. Native PCB hole coordinates in KiCad are (76.050,62.455), (76.050,64.995), (76.050,67.535). No PCB holes or traces were moved.

The review file has the same 50 references as the original. Only the eight rotations above and J2 midpoint differ. Physical PCB, schematic, Gerber ZIP and original CPL were not edited in this review.

## BOM recovery after reprocessing

Reprocessing the CPL initially reloaded the older server-side BOM and reverted capacitor substitutions. Uploaded the current local `1 Fan 2 Th.csv` as well, then processed both files together. Restored assembly selection of J1, J3, J7 and J8, which the site had deselected during reprocessing.

After a page reload, verified 28/28 BOM rows confirmed, all row checkboxes selected, C7=C46653, C8/C14/C15=C138687, and eight C476811 connectors total across the two assembled boards. No shortage was displayed. A transient 32/28 confirmation counter during checkbox changes disappeared on reload.

## Remaining release gates

- Verify regenerated preview uses the review CPL, especially the sign of the 90-degree rotation corrections and J2's exact midpoint. The site stalled at Processing files after upload; recovery reload attempted.
- Q1: after the interactive 90-degree clockwise correction its pin-one marker is on the correct side, but the model body appears offset relative to the PCB outline. Do not adjust its centroid by eye. Resolve the JLC model/footprint registration against the actual PowerDI3333-8 drawing or obtain JLC engineering confirmation.
- Keyed Molex connector body/lead positions appeared aligned, but complete pin-number/latch correspondence is not yet signed off. The two-pin model has potentially confusing colored markers; do not flip it solely because of those markers.
- Finish all component alignment checks and final quote/settings verification (five PCBs, two assembled, three bare; tooling/rails; confirm production and placement files; do not auto-confirm).
- Firmware programming and powered first-article testing remain necessary. Assembly-preview acceptance is not proof of electrical operation.

Manufacturer references inspected: Diodes DMPH4029LFGQ DS41959 Rev. 4-2, December 2025, pages 1 and 6 (local cached PDF); Molex SD-43045-007 G5 public PDF text. Molex drawing raster could not be retrieved for visual pin-number verification in this pass.
