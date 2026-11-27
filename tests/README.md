# Tests

pytest suite for the FPV drone addon. Run from the repo root with:

```bash
PYTHONPATH=$HOME/.local/lib/python3.12/site-packages python3 -m pytest
```

## Files

| File | Covers |
| --- | --- |
| `conftest.py` | Helpers: spec loading/mutation, validator runner, paths |
| `test_require_base.py` | Hard dependency: base found / missing / misnamed / too old / exact minimum |
| `test_power_check.py` | Battery, ESC voltage, motor/battery/PDB currents, domains, BMS, bool/NaN guards, array root |
| `test_compatibility_check.py` | Known parts, invented/UNVERIFIED parts, VTX==VRX, KV range, connectors, EU rules |
| `test_thermal_check.py` | Thermal budget, overload, bool power, unknown cooling |
| `test_firmware_check.py` | Firmware vs MCU (PX4 never on F405), gyro loop, DShot ceiling, versions |
| `test_run_all.py` | End-to-end: both examples PASS, invented part FAILs, missing base exits 2, credit present |
| `test_negative.py` | Regression fixtures in `fixtures/` — each must FAIL its validator cleanly (no traceback) |

## Fixtures

`fixtures/` holds 8 negative specs derived from the 5-inch freestyle example, each broken in exactly one way: invented MCU, ESC voltage too low, PX4 on F405, VTX/VRX protocol mismatch, thermal overload, bool where a current belongs, KV out of range, UNVERIFIED IMU.

## Integration

Tests run the validators as subprocesses against the real base skill at `../ai-pcb-design-skill` (sibling of this repo). If the base skill is missing, `require_base` tests fail — that is the point.
