# Camera System (high)

Camera interfaces: what the camera outputs and what the VTX accepts.

- **Analog:** camera outputs CVBS (75 Ω) to an analog VTX. Known sensors: RunCam Phoenix 2, Caddx Ratel 2. Keep the video trace away from switching noise — noise lines in the picture are a layout problem.
- **Digital:** DJI O3 Air Unit, Walksnail Avatar HD Pro, HDZero Lux — the camera is part of the digital link; the camera type must match the VTX type.
- **Power:** analog cameras usually run on 5 V; digital air units run on VBAT (3S–6S). The camera belongs to the right power domain in the spec.
- **Checks:** `compatibility_check.py` (known sensor for the camera type), `power_check.py` (camera current in its domain).
