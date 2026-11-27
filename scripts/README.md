# scripts/

Python validators for the FPV drone addon. Standard library only.

| Script | Checks | Exit |
| --- | --- | --- |
| `require_base.py` | Base skill `ai-pcb-design-skill` present, exact name, version >= 1.2.1 | 0 / 2 |
| `power_check.py` | Battery, ESC voltage, motor/battery/PDB currents, power domains, BMS | 0 / 1 / 2 |
| `compatibility_check.py` | Known parts, ESC protocol vs firmware, motor KV, VTX == VRX, connectors, EU rules | 0 / 1 / 2 |
| `thermal_check.py` | Thermal budget per component (ambient + power × theta × cooling factor) | 0 / 1 / 2 |
| `firmware_check.py` | Firmware vs MCU, gyro loop, DShot ceiling, GPS/telemetry support | 0 / 1 / 2 |
| `run_all.py` | All of the above, base skill first | 0 / 1 / 2 |
| `common.py` | Shared helpers (spec/config loading, bool-safe number checks, report) | — |

Usage:

```bash
python scripts/run_all.py --spec examples/spec_5inch_freestyle.json
python scripts/run_all.py --spec examples/spec_hexacopter_inspection.json
python scripts/power_check.py --spec <spec.json> [--base-skill <path>]
```

The base skill is found automatically (sibling `../ai-pcb-design-skill`, `AI_PCB_SKILL_PATH`, or `--base-skill`). Without it every script exits `2` and runs no check.

Known parts live in `config.json` — MCUs, IMUs, barometers, magnetometers, GPS modules, cameras, firmware matrices, ESC protocols, KV ranges, connector ratings, cooling factors, EU limits. A part that is not in the config is an error; add it only with its datasheet source. A bool is never a number in any check.
