# Sensor faults, missing tach and recovery — provisional simulation policy

No calibration is required by the user. 65 C is a full-speed control endpoint, not an absolute safety ceiling. Normal 2F/2TH operation remains independent: TH1 controls FAN1, TH2 controls FAN2. Manufacturing files are unchanged.

`fault_model.Supervisor` wraps the existing control model. The primary case is 2F/2TH, with 1F/2TH and 1F/1TH regression cases. Timings below are proposed simulation settings, not user-approved production firmware.

| Condition | Model response |
|---|---|
| Any sensor code <=5 or >=1018 | On next sample, all installed fans commanded full speed and alarm set |
| Sensor returns to valid range | Require 5 seconds continuously valid before clearing sensor alarm |
| Fan commanded on but no tach edge for 2 seconds | Set channel tach fault; all fans commanded full speed and alarm set |
| Fan deliberately commanded off | No missing-tach alarm |
| Tach resumes after a fault | Require 5 seconds of healthy activity before clearing that channel fault |
| Fault persists | Full command and alarm persist; do not assume physical recovery |

Recovery activity means no edge gap longer than 0.2 seconds. Edge counts are supplied at intervals no longer than 100 ms. Pulse timing is quantized to the update boundary, so physical detection timing includes that granularity. The wrapper enforces increasing time and rejects update gaps outside its assumptions; it is not a watchdog implementation. Full-speed fault override bypasses any normal startup staggering. The five-second start scheduler itself is not implemented here.

Sensor and tach faults are tracked separately; clearing one does not clear another. A newly forced-on fan receives its own two-second tach grace interval. After recovery, the normal temperature controller resumes, including its independent channel hysteresis. Repeated bad readings or interrupted tach recovery restart recovery timing.

## Executed checks

`results/fault_report.json` lists 28 scenario groups; `results/fault_trace.json` records representative two-fan traces. Run `run_simulation.py` to reproduce them alongside all existing studies. Checks include each sensor open/short, each fan missing tach at startup, mid-run loss of both tach signals, persistent failures, recovery delays, interrupted recovery, intentionally stopped fans, short pulse interruptions and invalid test inputs.

These are Python behavioral assertions using injected ADC values and edge counts. They do not execute compiled ATtiny firmware or a physical motor model. The existing `Controller` remains the nominal control core; these fault tests exercise the added supervisor rather than silently changing the old test interpretation.

## Limitations and remaining decisions

- A disconnected tach wire and a stopped rotor are indistinguishable here; report missing tach, not a proven mechanical stall.
- Plausible but incorrect thermistor readings cannot be caught by near-rail detection alone. No mismatch alarm is assumed: sensors may intentionally measure different zones.
- Spurious tach pulses can defeat missing-edge detection. RPM plausibility, pulse filtering and actual timer capture remain to implement.
- There is no fan power switch for firmware-controlled supply cycling. Full PWM is a request, not evidence of a successful restart.
- There is no watchdog/reset, brownout, boot sequencing, MCU timing or alarm LED/buzzer electrical simulation.
- All-fans-full fault policy, two-second detection, five-second recovery and automatic clearing remain provisional. They may be revised without changing normal TH1/FAN1 and TH2/FAN2 mapping.
