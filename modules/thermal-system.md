# Thermal System (high)

Whole-drone thermal analysis: motors, ESCs, battery and VTX together, with flight airflow as the cooling.

- **Same budget as the PCB level, wider scope:** every heat source in the aircraft gets a power, a theta and a cooling type; the estimate must stay under its max temperature. `thermal_check.py` runs it.
- **Worst case is hover without airflow.** A bench test with no prop wash is hotter than flight — if it passes on the bench, it passes in the air.
- **Battery heat:** high-C discharge warms the pack; a hot pack sags and ages fast. Keep the pack in airflow, never buried under insulation.
- **This is a budget, not a simulation.** Real proof needs Elmer FEM or a thermal-camera measurement (SKILL.md §19).
