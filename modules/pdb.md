# PDB (critical)

Power distribution board: battery in, motors/ESCs and BEC rails out.

- **Sizing:** the PDB max current must cover the total motor max current. Size the copper with the base skill's `trace_width.py` — a 100 A path is not a 0.5 mm trace.
- **Current sensing:** a shunt or Hall sensor on the battery input feeds the FC (mAh consumed, voltage sag alarms).
- **BEC rails:** 5 V for FC/GPS/camera/receiver, 9 V / 12 V where used. A BEC that browns out on punch-out crashes the drone — size it with margin and check it in `power_check.py`.
- **Integrated vs separate:** a 4-in-1 ESC often integrates the PDB. The same current rules apply; `pdb.integrated: true` says so in the spec.
