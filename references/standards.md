# Standards

Civil-operation rules enforced or referenced by this addon:

- **EASA open category** — Regulations (EU) 2019/947 (operations) and (EU) 2019/945 (class marks). Open category: under 25 kg, VLOS, max 120 m above ground, no flight over assemblies of people. Classes C0 < 250 g, C1 < 900 g, C2 < 4 kg, C3/C4 < 25 kg. Operator registration at 250 g or more (or with a camera). Direct Remote ID required for C1–C3. A1/A3 training for C1+, A2 certificate for C2 close to people.
- **RF:** VTX power limits are national — the validator warns above 1 W; the pilot checks the local limit before flying.
- **LiPo transport and storage:** follow the cell manufacturer's datasheet and local transport rules; never ship a damaged pack.
- **What this addon does NOT cover:** specific-category authorisation (SORA), certified category, BVLOS rules, national additions to EASA rules. Those need the national aviation authority, not a skill file.

All values in this file were checked against EASA sources (2026-11-27). If a regulation changes, the config table in `scripts/config.json` is the single place to update.
