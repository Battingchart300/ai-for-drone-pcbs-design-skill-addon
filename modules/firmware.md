# Firmware (high)

Flight firmware: Betaflight, INAV, PX4, ArduPilot.

| Firmware | MCUs | Best for |
| --- | --- | --- |
| Betaflight | F405, F722, F745, H743 | Freestyle / racing |
| INAV | F405, F722, F745, H743 | GPS navigation, fixed-wing + multirotor |
| ArduPilot | F405, F722, F745, H743 | Full autonomy, MAVLink |
| PX4 | F745, H743 only | Autonomy on F7/H7 hardware |

- PX4 does NOT run on an F405 — `firmware_check.py` fails it.
- Gyro loop: 8 kHz max on F4/F7, 16 kHz on H7. DShot1200 needs F7/H7.
- Firmware version must be a real version string (e.g. `4.5.0`).
- Configuration (PIDs, filters, rates) is firmware work, not board work — but the board decides the noise the firmware has to filter.
