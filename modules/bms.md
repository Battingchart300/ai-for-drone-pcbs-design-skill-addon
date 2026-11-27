# BMS (critical)

Battery management system: cell balancing, per-cell cutoff, over-current protection.

- **Where it belongs:** smart batteries and industrial packs. FPV freestyle quads normally have NO BMS on board — the charger balances the pack. `bms.present: false` is normal there.
- **When present:** cell count must match the battery; cutoff 2.8–3.6 V per cell (fly above ~3.2 V under load); balance current positive and sized to the pack.
- **Safety:** a BMS is safety-critical hardware — it needs professional verification and lab testing before flight (SKILL.md §2, rule 4).
- **Checks:** `power_check.py` (cell count, cutoff, balance current).
