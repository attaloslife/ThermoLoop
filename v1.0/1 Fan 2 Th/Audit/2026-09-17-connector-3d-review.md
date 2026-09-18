# Connector orientation review of JLCPCB follow-up images

Reviewed user-supplied Desktop/1.png, 2.png and 3.png for PCBA SMT026091562430_Y3, against current PCB pad coordinates/nets and Molex SD-43045-007 revision G5 (manufacturer drawing reproduced on the final page of the locally cached molex-g5.pdf).

## Conclusion

The visible latch/ramp features in these three views agree with the intended orientation of J1, J3, J7, J8, J4 and J5. Recommend accepting these six connector orientations as shown, without a 180-degree rotation. Their apparent lead and mounting-tab registration also agrees with the footprints at screenshot resolution. No assembly authorization was transmitted.

The previous top-view assessment was conditional on interpreting pink dots as physical component pin 1. These newly visible housing features resolve that ambiguity; do not use the prior conditional 180-degree suggestion as an assembly instruction. Pink overlay markers alone are not reliable evidence of physical terminal numbering.

## Required positions, board top view with text upright

| Ref | Latch/ramp direction | Numbered PCB pads |
| --- | --- | --- |
| J1 | Bottom, toward +VIN/F1 | 1 bottom VIN_RAW; 2 top GND |
| J3 | Top, toward TH1/F1 | 1 top TH1_RAW; 2 bottom GND |
| J7 | Top, toward TH2/J3 | 1 top TH2_RAW; 2 bottom GND |
| J8 | Top, toward VIN/top edge | 1 top VIN_PROTECTED; 2 bottom BUZZER_SW |
| J4 | Right, toward GND/VIN labels | 1 upper-right GND; 2 lower-right VIN_PROTECTED; 3 upper-left FAN1_TACH_RAW; 4 lower-left FAN1_PWM |
| J5 | Top, toward R10/R11/R6/R8 | Upper row left-to-right 1,2,3,4,5; lower row left-to-right 6,7,8,9,10 |

Molex's drawing places circuit 1 on the latch-side row. With latch down it is the rightmost pad of that row; rotating this geometry to the visible latch directions gives the PCB numbering above. J5 uses sequential row numbering, not alternating odd/even numbering.

## Scope

This resolves the six connector-orientation questions in Mia's email. It does not certify soldering, physical production, firmware, or powered operation, and is not a new full-board component-placement signoff. No KiCad design, BOM, CPL or manufacturing files were changed.
