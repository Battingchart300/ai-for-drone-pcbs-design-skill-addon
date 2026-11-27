# VTX / VRX (high)

Video transmitter on the drone, video receiver in the goggles.

- **Analog:** 5.8 GHz, camera CVBS in, RF out. Simple, lowest latency.
- **Digital:** DJI O3, HDZero, Walksnail Avatar. VTX and VRX must use the SAME protocol — an analog VRX cannot receive a DJI O3 VTX.
- **Power:** 25–2000 mW in the spec; above 1 W the validator warns (check the local RF limit). An 800 mW VTX dissipates several watts — heatsink + airflow, or it overheats.
- **Placement:** VTX antenna away from the GPS antenna.
- **Checks:** `compatibility_check.py` (known protocols, VTX == VRX, power range), `thermal_check.py` (VTX heat).
