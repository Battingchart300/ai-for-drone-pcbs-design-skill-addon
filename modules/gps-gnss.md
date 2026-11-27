# GPS / GNSS (high)

Position hold, return-to-home, navigation (INAV / ArduPilot / PX4).

- **Modules:** u-blox M10, M9N, M8N. Protocols UBX (preferred) or NMEA, over UART.
- **Placement:** on a mast/stalk, away from the VTX antenna and the power stage — RF desense kills GPS lock. Keep the antenna facing up with a clear sky view.
- **Fix before arming:** navigation modes arm only with a GPS fix; the pre-arm check enforces it.
- **Checks:** `compatibility_check.py` (known module, UBX/NMEA), `firmware_check.py` (GPS protocol supported by the firmware).
