# Interfaces

| Interface | Used for | Notes |
| --- | --- | --- |
| UART | GPS, receiver, telemetry, VTX control (SmartAudio / Tramp) | One peripheral per UART; check the MCU UART count |
| SPI | Gyro/IMU, flash, barometer (fast) | Gyro belongs on SPI — I2C is too slow for 8 kHz loops |
| I2C | Barometer, magnetometer, rangefinder | Pull-ups required; keep traces short |
| CAN | Industrial payloads, redundant sensors | Needs a CAN transceiver; 120 Ω termination at both ends |
| USB | FC configuration, blackbox download, firmware flashing | USB-C preferred; protect with ESD diodes |
| CVBS | Analog camera → VTX | 75 Ω, keep away from switching noise |
| DShot | FC → ESC | Digital, no calibration; DShot1200 needs F7/H7 timers |
| CRSF / SBUS / MAVLink | RC link / telemetry | See `modules/telemetry.md` |

Rule: every interface in the spec must name its bus, its pins and its protocol. An interface with a missing pin is caught by the pin-by-pin check (SKILL.md §3.1), not by luck.
