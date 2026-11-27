# Changelog

## v0.0.1 — 2026-11-27 (first release)

- 18 modules: Flight Controller, ESC, PDB, BMS, GPS/GNSS, IMU, VTX/VRX, Telemetry, AIO PCB, Firmware, EMI/EMC, Thermal Design, Mechanical Design, Safety System, Camera System, Sensor System, Connector System, Thermal System.
- 4 validators + require_base (exit 2 without the base skill) + run_all; 2 example specs (5-inch freestyle quad, industrial inspection hexacopter), both PASS.
- Quality rules: maturity levels (conceptual / simulated / physically verified), automatic ERC/DRC/DFM when tools are available, full error/warning/unverified log, hardware revisions with backward compatibility, professional verification for safety-critical hardware.
- Output formats: .kicad_pcb, .kicad_sch, .kicad_pro, .step, .stl, .gbr, .drl, .csv (BOM), .json, .yaml, .md, .pdf, .spice, .zip.
- Workflows: pin-by-pin check before handover; multi-pass placement + batch routing with continuous DRC, goal 0 DRC errors.
- pytest suite (unit, integration, regression, negative), CI on Python 3.10–3.13 (no 3.9 — EOL, no setup-python on ubuntu 26.04).
- Simulation policy: the skill generates inputs and calls the tool; a missing tool is BLOCKED / NOT_RUN, never a fake PASS.
