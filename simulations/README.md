# Simulations

## Policy

This skill **cannot simulate**. It generates simulation inputs and calls the tool. That is the whole job here:

| Domain | Tool | Input this addon generates |
| --- | --- | --- |
| Signal integrity / EM | openEMS | Geometry + material + port definition (`.xml` / Octave script) |
| Thermal | Elmer FEM | Mesh + material + boundary conditions |
| Circuit | ngspice / LTspice | `.spice` netlist |

## Status reporting

`sim_status.py` checks which tools are installed (`shutil.which`) and reports one status per tool:

- `OK` — the tool is installed and can be called.
- `NOT_RUN` — the tool is installed but no simulation was run in this session.
- `BLOCKED` — the tool is missing; the simulation cannot run.

A missing tool is **never** a fake `PASS`. A gate that needs a simulation stays open until the tool runs and its output file exists.

## What a simulation proves

A simulation result is evidence only when it names the tool, the exact command and the output file. A simulation is not a flight test — see SKILL.md §1 (maturity levels: conceptual / simulated / physically verified).

```bash
python simulations/sim_status.py
```
