# JLCPCB production-file review — 2026-09-16

## Scope and disposition

PCB order Y3-13393445A, batch W2026091520532581; 5 PCBs and 2 assemblies. Reviewed downloaded `1 Fan 2 Th_Y3.zip`, internal job `13393445a_y3`, against the submitted Gerber ZIP. Browser approval was NOT submitted.

No blocking PCB fabrication-file discrepancy was found in the checks below. This is a CAM comparison, not a guarantee of electrical operation or approval of component assembly placement.

## Evidence

- All 10 original Gerber, drill and job files supplied in JLCPCB's `yg` directory match the submitted manufacturing ZIP byte-for-byte.
- Submitted ZIP SHA256: ED7FFE0186CCF07D85CE17DAEB5E828E99F3FD0624826CA531708933A746F389.
- All 60 original hole centers retained; maximum coordinate difference after translation is 0.0000322 mm. Six additional handling holes are outside the finished PCB.
- ODB++ `steps/edit/layers/drl/tools` explicitly specifies finished sizes of 0.3, 0.4, 1.0 and 3.2 mm. The 1.15 mm and 3.25 mm dimensions in the production drill plot are drill-tool sizes, not changed finished-size requirements. The separate NPTH tool table also specifies 3.2 mm.
- The processed `ko` contour retains the nominal 90 x 75 mm finished board with 3 mm rounded corners. Added approximately 5 mm rails above and below give an approximately 90 x 85 mm manufacturing panel; these do not enlarge the finished PCB.
- Geometry comparison of top and bottom copper inside x=0.3..89.7, y=5.3..79.7 mm in panel coordinates found no missing copper beyond a 0.015 mm comparison tolerance. Added top-copper area beyond this tolerance was 0.01604 mm² in small corner slivers; bottom was zero.
- Copper connected-island counts stayed 72 top and 18 bottom, with no detected merging of original islands in this comparison region.
- All original soldermask openings were retained within the same tolerance. Extra mask clearances were concentrated around mounting holes and rounded board corners, not removed component-pad openings.
- No original top silkscreen was missing beyond the comparison tolerance. Added area was predominantly thickening of the Attalos artwork.
- Red soldermask / white silkscreen were verified in the live order review. The order lists `1 Fan 2 Th.csv` and `1_Fan_2_Th_JLCPCB_CPL_review.csv` for assembly.

## Limits and remaining assembly review

The comparison uses polygon approximation (0.001 mm arc approximation) and 0.015 mm shape tolerance, with a clipped interior region. It is not a formal netlist-aware electrical test, fabrication-tolerance certification, stencil review, or exhaustive panel-depanelization analysis. Board-edge geometry was checked separately from the copper comparison.

Component placement is a separate approval: the previously observed Q1 model/body offset and keyed-connector orientation ambiguity still require the engineer-adjusted assembly preview. Support's statement that engineers will adjust placement is not evidence that those corrections have already been made. Firmware and physical bring-up remain necessary; production-file approval cannot establish that an unprogrammed assembled board will perform temperature control.

Local comparison artifacts and script: `C:/Users/ersinaytac/Documents/ChatGPT/ThermoLoo[/production-review-20260916/` (`comparison.json`, `compare.py`, layer-diff PNGs and extracted production files). No schematic, PCB, BOM or CPL changes were made during this review.
