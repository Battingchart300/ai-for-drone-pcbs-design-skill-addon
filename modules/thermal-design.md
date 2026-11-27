# Thermal Design (critical)

PCB-level heat: copper, vias, heatsinking.

- **Hot parts:** VTX, ESC FETs, voltage regulators. Give each copper area, thermal vias and airflow.
- **Budget model:** estimated temperature = ambient + power × theta_ja × cooling factor (none 1.0, heatsink 0.7, heatsink + airflow 0.5, fan 0.4). `thermal_check.py` enforces the max temperature per component.
- **This is a budget, not a simulation.** Real proof needs Elmer FEM or a thermal-camera measurement — see SKILL.md §19. A VTX buried in a closed frame overheats no matter what the budget says.
- **Copper:** wide pours for power, thermal vias under FETs and regulators, no thermal relief on high-current pads.
