# Telemetry (high)

RC link and telemetry between the drone and the pilot/ground station.

- **Protocols:** CRSF, ELRS, MAVLink, SBUS, FPort.
- **By firmware:** Betaflight — CRSF/SBUS/FPort; INAV — CRSF/SBUS/MAVLink; ArduPilot — MAVLink/CRSF/SBUS; PX4 — MAVLink.
- **Failsafe rides on this link:** loss of link must disarm or trigger return-to-home. Test it on the bench before the first flight.
- **Checks:** `compatibility_check.py` (known protocol), `firmware_check.py` (protocol supported by the firmware).
