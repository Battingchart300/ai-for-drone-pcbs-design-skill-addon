#!/usr/bin/env python3
"""sim_status.py — report simulation tool availability.

Statuses: OK (installed), NOT_RUN (installed, no simulation run),
BLOCKED (missing — the simulation cannot run). A missing tool is
never a fake PASS. Standard library only.
"""
import shutil
import sys

TOOLS = {
    "openEMS": "Signal integrity / EM simulation",
    "elmerfem": "Thermal simulation (Elmer FEM)",
    "ngspice": "Circuit simulation",
    "ltspice": "Circuit simulation (LTspice)",
    "kicad-cli": "ERC / DRC / export (KiCad CLI)",
}


def main():
    print("Simulation tool status (FPV drone addon v0.0.1):")
    blocked = []
    for tool, what in TOOLS.items():
        found = shutil.which(tool) is not None
        status = "OK — installed (NOT_RUN: no simulation run yet)" \
            if found else "BLOCKED — not installed"
        if not found:
            blocked.append(tool)
        print(f"  {tool}: {status} — {what}")
    if blocked:
        print(f"Result: {len(blocked)} tool(s) BLOCKED: "
              f"{', '.join(blocked)} — simulations needing them cannot run.")
    else:
        print("Result: all tools installed (status NOT_RUN until a "
              "simulation actually runs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
