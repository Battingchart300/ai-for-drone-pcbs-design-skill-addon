# Validator catalog

Every validator in `scripts/` and what it enforces. All validators exit 0 (pass), 1 (fail) or 2 (setup missing — including a missing base skill).

| Validator | File | Enforces |
| --- | --- | --- |
| require_base | `scripts/require_base.py` | Base skill present, frontmatter `name:` exactly `ai-pcb-design-skill`, version >= 1.2.1 |
| power_check | `scripts/power_check.py` | Battery max current/voltage; ESC voltage rating covers the charged battery; motor max <= ESC continuous per channel; motor total <= battery max; PDB covers motor total; every power domain budget holds; VBAT matches battery nominal; BMS cell count/cutoff/balance when present |
| compatibility_check | `scripts/compatibility_check.py` | Every part is a known verified part (unknown or UNVERIFIED = error); ESC protocol allowed for ESC firmware; motor KV in range for class + cells; GPS/camera/VTX/VRX known; VTX protocol == VRX protocol; telemetry known; sensor parts + buses known; connector declared current <= connector rating; EU: altitude <= 120 m, class-mass limits, Remote ID for C1–C3 |
| thermal_check | `scripts/thermal_check.py` | Per component: ambient + power × theta_ja × cooling factor <= max temp; cooling type known; numbers real and finite |
| firmware_check | `scripts/firmware_check.py` | Firmware known and supports the MCU (PX4 needs F7/H7, never F405); gyro loop <= MCU max; ESC protocol <= MCU DShot ceiling; firmware version looks like x.y.z; GPS + telemetry protocols supported by the firmware |
| run_all | `scripts/run_all.py` | require_base first, then the four checks in order; stops at the first failure |

## Regression fixtures

Negative specs used by the pytest suite live in `tests/fixtures/` (see `tests/README.md`): invented MCU, ESC voltage too low, motor total over battery max, PX4 on F405, DShot1200 on F405, VTX/VRX protocol mismatch, thermal overload, UNVERIFIED IMU, bool where a number belongs, KV out of range. Every one of them must FAIL the matching validator.
