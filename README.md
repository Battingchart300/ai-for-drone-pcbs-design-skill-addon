# ai-fpv-drone-pcbs-design-skill-addon

**Version:** 0.0.1 — 2026-11-27

An addon to `ai-pcb-design-skill` (required, v1.2.1+) for designing civil FPV drone electronics: flight controller, ESC, PDB, BMS, GPS/GNSS, IMU, VTX/VRX, telemetry, AIO PCB, camera and sensor systems, firmware (Betaflight / INAV / PX4 / ArduPilot), EMI/EMC, thermal, mechanical and safety design.

**Civil use only** — recreational and industrial drones. No weaponization content anywhere.

## What it does

- 18 modules, from Flight Controller (critical) to Safety System (critical), Camera System, Sensor System, Connector System and Thermal System.
- 4 automatic validators + a hard base-skill check: power domains and energy balance, component/interface compatibility, thermal budgets, firmware compatibility.
- 2 complete example specs that PASS all validators: a 5-inch freestyle quad and an industrial inspection hexacopter.
- Quality rules: conceptual / simulated / physically verified maturity levels, automatic ERC/DRC/DFM when tools exist, full error/warning/unverified log, hardware revisions with backward compatibility, professional verification for safety-critical hardware.
- Workflows: pin-by-pin check before handover; multi-pass placement and batch routing with continuous DRC (goal: 0 DRC errors).

## Requirements

- `ai-pcb-design-skill` v1.2.1 or newer — this addon does NOT work without it. Every script exits with code `2` and runs no check if the base skill is missing.
- Python 3.10–3.13, standard library only (no third-party packages needed for the validators; pytest only for the test suite).

## Quick start

```bash
# run every check on the freestyle example (base skill is found automatically
# as a sibling directory, or pass --base-skill / -- AI_PCB_SKILL_PATH)
python scripts/run_all.py --spec examples/spec_5inch_freestyle.json

# inspection hexacopter
python scripts/run_all.py --spec examples/spec_hexacopter_inspection.json

# run the test suite
PYTHONPATH=$HOME/.local/lib/python3.12/site-packages python3 -m pytest
```

## Layout

| Path | Contents |
| --- | --- |
| `SKILL.md` | The skill: rules, workflow, modules, checks |
| `README.md` | This file |
| `CHANGELOG.md` | Version history |
| `manifest.json` | Addon metadata |
| `compatibility.json` | Hard dependency declaration |
| `references/` | Architecture, components, interfaces, design rules, safety, standards |
| `modules/` | One doc per module (18) |
| `scripts/` | Python validators (stdlib only) + config |
| `schemas/` | JSON Schema for the drone spec |
| `templates/` | Spec + BOM templates |
| `examples/` | 2 complete example specs (both PASS) |
| `validators/` | Validator catalog |
| `simulations/` | Simulation policy + tool-status script |
| `benchmarks/` | Validator runtime benchmarks |
| `tests/` | pytest suite (unit, integration, regression, negative) |
| `.github/workflows/` | CI: Python 3.10–3.13, pytest + validators on both examples |

## Simulations

This skill cannot simulate. It generates inputs (openEMS, Elmer FEM, ngspice/LTspice) and calls the tool. A missing tool is reported `BLOCKED` or `NOT_RUN`, never a fake `PASS`. See `simulations/README.md`.

## Changelog

See `CHANGELOG.md`. v0.0.1 is the first release.

## License

MIT — see `LICENSE`.

---

*Made by PTS6845 — https://battingchart300.github.io*
