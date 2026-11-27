# Safety

- **Failsafe is mandatory.** Loss of RC link → disarm or return-to-home (where the firmware supports it). Never fly away. Tested on the bench before the first flight.
- **Arming:** deliberate switch only, with a pre-arm check (sensors OK, battery OK, GPS lock where required). Never arm on the bench with props on.
- **Lab testing before flight:** bench power-up → motor test WITHOUT props → range test → failsafe test. Props go on only at the field.
- **Battery:** LiPo charging only on a balance charger, never unattended; damaged packs are discharged and disposed of, never flown. Storage at ~3.8 V/cell.
- **Safety-critical hardware** (FC, ESC power stage, PDB, BMS, failsafe) requires professional verification and lab testing — the skill's PASS is not a flight clearance (SKILL.md §2, rule 4).
- **LiPo cutoff:** never fly a cell below ~3.2 V under load; the BMS cutoff range in this addon is 2.8–3.6 V per cell.
