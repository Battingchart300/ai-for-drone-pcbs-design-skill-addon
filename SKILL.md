---
name: ai-fpv-drone-pcbs-design-skill-addon
description: Addon to ai-pcb-design-skill (REQUIRED, v1.2.1+) for civil FPV drone electronics — flight controller, ESC, PDB, BMS, GPS/GNSS, IMU, VTX/VRX, telemetry, AIO PCB, cameras and sensors, firmware (Betaflight/INAV/PX4/ArduPilot), EMI/EMC, thermal, mechanical and safety design. Does NOT work without the base skill. Civil use only, no weaponization. Use when designing FPV drone electronics with an AI.
---

# ai-fpv-drone-pcbs-design-skill-addon

**Version:** 0.0.1 — 2026-11-27

**What it is:** an addon skill for designing civil FPV drone electronics — flight controller, ESCs, power distribution, batteries, video link, GPS and sensors — on top of `ai-pcb-design-skill`. It adds only the drone-specific parts: power domains, component compatibility, thermal budgets, firmware compatibility and civil-operation rules. Everything else (spec, schematic, layout, DRC, BOM, fab) comes from the base skill.

**Who it is for:** the same user as the base skill — a beginner who designs boards and lets the AI do the drafting, while the human stays in charge of every decision that matters — now for a flying machine, where a wrong board can fall out of the sky.

**How to use it:** load the base skill first, then this file. It works with any AI backend, like the base skill. If a step needs a tool that does not exist in your environment (for example `kicad-cli`, `openEMS` or Elmer FEM), the skill says so and tells you the manual alternative — it never pretends a check ran when it did not.

**Civil use only.** This addon covers recreational and industrial drones (freestyle, racing, cinematic, long-range, inspection). It contains no weaponization content of any kind, and must never be used to design one.

---

## 0. Prerequisite — hard stop: this skill does NOT work alone

Read this section first. Nothing below it applies without it.

1. **This addon REQUIRES `ai-pcb-design-skill` v1.2.1 or newer.** Before ANY work, load the base `SKILL.md`, confirm its `name` is `ai-pcb-design-skill` and its version is >= 1.2.1.
2. **If the base skill is not loaded / not found, STOP.** Do not continue, do not guess, do not work from this file alone. Say exactly this and wait for the human:
   > `STOP — missing base skill ai-pcb-design-skill v1.2.1+. This addon does not work without it. Load the base skill first.`
3. **The kit enforces the same stop.** `scripts/run_all.py` and every check script in `scripts/` call `scripts/require_base.py` first. If the base skill is not found, they exit with code `2` (setup missing) and run **no** addon check. A missing base is a setup failure, never a pass.
4. **Nothing in this addon replaces the base skill.** The base spec format, hard rules, gated workflow, routing rules, DRC, BOM, trace-width and fab rules still apply in full. This addon only *extends* them. If the two disagree, the base skill wins on PCB rules, this addon wins only on drone numbers in §4–§15.
5. **A failed base gate stops the addon work too.** If the base spec fails `rules_check.py`, or DRC fails, fix the base first. Do not proceed to an addon stage on top of a failing base stage.

### 0.1 Hard rules inherited from the base skill

All 10 hard rules of the base skill (§0) apply unchanged, in particular:

- Never invent a part number, pin, footprint, datasheet value or fab limit. If a value cannot be verified, write `UNVERIFIED` and cite the file and page where it should be checked. A guessed pinout is the number-one cause of dead boards — and on a drone, of crashes.
- **When you do not know a value, ASK the user.** Never invent a size, a voltage, a pin assignment or a part. A question costs a minute; a wrong guess costs a respin — or a crash.
- Verify on the web, never from memory. Datasheets, component specifications and fab capability limits are checked against live sources. Memory is not a source.
- Never disable, filter or loosen a check. A waiver (knowingly breaking a rule) is a human decision, written down with a reason.
- The model never decides correctness. Small, independently runnable scripts in `scripts/` verify the design (exit 0 = pass, 1 = fail, 2 = setup missing). The model never declares a board correct.
- Never order, upload or publish anything. The order is placed only by the human, manually, with human review.
- Never claim a check ran if it did not run. If a tool is missing, the report says so. A skipped check is a gap in the review, not a silent omission.
- Never destroy the user's work. Checkpoint before the first change.
- A failed gate stops the work. Fix the cause, re-run the *same* check. Do not work around it, do not relax the rule, do not proceed to the next stage. If a stage fails 3 times, stop and ask the human.
- The schematic is the design; the layout is only its physical implementation.

---

## 1. Design maturity — say which one this is

Every design in this addon carries one maturity label, and the label must be written on the design, not implied:

| Level | Meaning | What it proves |
| --- | --- | --- |
| **Conceptual design** | Block diagram, part choices, spec passes the validators | The numbers fit together. Nothing is proven about the real board. |
| **Simulated design** | Conceptual + SI/EM/thermal simulation inputs generated and run in a real tool (openEMS, Elmer FEM, ngspice/LTspice) | The simulation ran and its results are on file. A simulation is still not a flight. |
| **Physically verified design** | Simulated + built, measured in the lab, flown | The only level that may be called flight-ready. |

A conceptual design must never be presented as verified. A simulation result must never be presented as a measurement. See §19 for the simulation policy: a missing tool is reported `BLOCKED` or `NOT_RUN`, never a fake `PASS`.

---

## 2. Quality rules

1. **Automatic ERC, DRC and DFM checks run whenever the tools are available** (KiCad CLI for ERC/DRC, fab rules for DFM). If a tool is missing, the report says `NOT_RUN` and names the missing tool — the gate stays open, it is not passed.
2. **Every error, warning and unverified parameter is recorded** in the review report, with the file and line that produced it. Nothing is silently dropped. `UNVERIFIED` values fail the validators — they are a to-do list, not a pass.
3. **Hardware revisions are supported and backward compatible.** Every board revision gets a revision letter/number, a changelog entry, and a note on what changed vs. the previous revision and whether old firmware, old frames and old batteries still fit. A breaking change is flagged, never hidden.
4. **Safety-critical hardware requires professional verification.** Flight controller, ESC power stage, PDB, BMS and any failsafe hardware must be reviewed by a qualified person and lab-tested (bench power-up, motor test without props, range test, failsafe test) before the first flight. The skill's PASS is not a flight clearance.
5. **No verification claim without evidence.** A claim ("0 DRC errors", "VTX stays under 85 °C") must name the tool, the command and the output file. A claim without evidence is treated as not made.

---

## 3. Gated workflow

| Stage | Do | Gate |
| --- | --- | --- |
| D0. Requirements | Drone class, MTOM, flight time, range, camera, region (EU) | Spec passes all 4 validators, 0 errors. Human approves the spec. |
| D1. Architecture | Block diagram: FC + ESC + PDB + battery + video + GPS + sensors | Every part has MPN + datasheet + footprint. No part without a datasheet. |
| D2. Power | Power domains, energy balance, wire/connector sizing (§6) | `power_check.py`: 0 errors. |
| D3. Compatibility | Part, protocol and firmware matrix (§5, §7, §8) | `compatibility_check.py` + `firmware_check.py`: 0 errors. |
| D4. Schematic | Draw per base §5.2 + module docs in `modules/` | Base ERC: 0 errors. Pin-by-pin check (§3.1): done. |
| D5. Layout | Placement in passes, routing in batches (§3.2) | Continuous DRC, goal 0 errors. |
| D6. Thermal + EMI | Thermal budget (§12), EMI/EMC review (§11) | `thermal_check.py`: 0 errors; EMI checklist signed. |
| D7. Checks | All addon checks + base checks | All checks pass; review report written. |
| D8. Lab + flight | Bench test, motor test without props, failsafe test, first flight | Human sign-off in writing. No flight without it. |

### 3.1 Workflow A — parts → schematic → layout → pin-by-pin check

The standard build procedure (inspired by the tunestechtips workflow):

1. **Select the parts** — FC MCU, IMU, ESC, motors, battery, VTX/VRX, GPS, camera, sensors. Every part from a datasheet, never from memory. If a value is unknown, ASK.
2. **Draw the schematic** — per base §5.2, one sheet per subsystem (power, FC, ESC, video, GPS/sensors). Annotate every net.
3. **Lay out the board in KiCad** — placement first (§3.2), then routing.
4. **Pin-by-pin check — mandatory before handover.** Go through every pin of every part, one by one: pin number, net name, expected connection, actual connection in the schematic AND in the layout. A pin that is not checked is a pin that is wrong. The check is recorded in the review report (part, pin count, result). No handover without it.

### 3.2 Workflow B — one prompt → finished board (multi-pass)

The fast-build procedure (inspired by the protoflow.ai workflow) — a procedure, not a capability claim: the skill does not place or route by itself, it tells the model how to do it in passes:

1. **Placement in passes.** Pass 1: fixed parts (mounting holes, connectors, battery pads). Pass 2: power stage (ESC, PDB, high-current paths). Pass 3: FC + IMU (vibration-isolated, away from power). Pass 4: video + GPS + sensors. Pass 5: passives and cleanup. After every pass, run DRC and fix before the next pass.
2. **Routing in batches.** Batch 1: power (VBAT, high-current). Batch 2: high-speed (gyro SPI, USB, video). Batch 3: the rest. Run DRC after every batch.
3. **Goal: 0 DRC errors.** The loop is place → route → DRC → fix → repeat. A board is handed over only with a clean DRC run on file. If DRC cannot reach 0, the remaining errors are listed with reasons and a human decides — they are never hidden.

---

## 4. Spec-first: the drone spec

The drone spec is a JSON file (schema: `schemas/drone-spec.schema.json`, template: `templates/spec-template.json`). It extends the base spec — a board that uses this addon has both a base spec and a drone spec. Fields:

- `drone`: name, class (freestyle-5inch / racer-5inch / cinematic-7inch / long-range-7inch / inspection-hexacopter), frame size, MTOM in grams, category.
- `battery`: cells (S count), capacity_mah, c_rating, type (LiPo).
- `flight_controller`: mcu, imu, barometer, firmware, firmware_version, gyro_loop_hz, stack (separate / aio).
- `esc`: type (4in1 / single), protocol, firmware, continuous/burst current, voltage_max_v.
- `motors`: list of ref, size, kv, max_current_a.
- `pdb`: max_current_a, integrated (true/false).
- `bms`: present (true/false); when present: cells, cutoff_v_per_cell, balance_current_ma.
- `gps`: module, protocol (UBX / NMEA), baud.
- `camera`: type (analog / digital), sensor.
- `vtx` / `vrx`: type, protocol, band, power_mw (VTX).
- `telemetry`: protocol, link.
- `power_domains`: list of name, voltage_v, max_current_a, consumers (ref + current_a).
- `thermal`: ambient_c, components (ref, power_w, theta_ja_c_per_w, max_temp_c, cooling).
- `sensors`: list of type, part, bus.
- `connectors`: list of name, type, max_current_a, mating.
- `compliance`: region, regulation, class_mark, remote_id, operator_registered, max_altitude_m.

Lint the spec before drawing anything:

```bash
python scripts/run_all.py --spec examples/spec_5inch_freestyle.json
```

**Rule: nothing is drawn until the drone spec has 0 errors AND the base spec has 0 errors.**

---

## 5. Modules

| # | Module | Priority | Doc | What it covers |
| --- | --- | --- | --- | --- |
| 1 | Flight Controller | critical | `modules/flight-controller.md` | FC MCU, IMU placement, gyro loop |
| 2 | ESC | critical | `modules/esc.md` | ESC protocols, current ratings, firmware |
| 3 | PDB | critical | `modules/pdb.md` | Power distribution, high-current paths |
| 4 | BMS | critical | `modules/bms.md` | Cell balancing, cutoff, smart batteries |
| 5 | GPS / GNSS | high | `modules/gps-gnss.md` | u-blox modules, UBX/NMEA, antenna |
| 6 | IMU | high | `modules/imu.md` | Gyro/accel choice, vibration, filtering |
| 7 | VTX / VRX | high | `modules/vtx-vrx.md` | Video link, protocols, RF power |
| 8 | Telemetry | high | `modules/telemetry.md` | CRSF / ELRS / MAVLink / SBUS |
| 9 | AIO PCB | high | `modules/aio-pcb.md` | All-in-one FC+ESC boards |
| 10 | Firmware | high | `modules/firmware.md` | Betaflight / INAV / PX4 / ArduPilot |
| 11 | EMI / EMC | critical | `modules/emi-emc.md` | Noise, grounding, signal integrity |
| 12 | Thermal Design | critical | `modules/thermal-design.md` | PCB copper, vias, heatsinking |
| 13 | Mechanical Design | high | `modules/mechanical.md` | Frame, mounting, vibration |
| 14 | Safety System | critical | `modules/safety-system.md` | Failsafe, arming, lab testing |
| 15 | Camera System | high | `modules/camera-system.md` | Camera interfaces, analog/digital |
| 16 | Sensor System | high | `modules/sensor-system.md` | Barometer, magnetometer, rangefinder |
| 17 | Connector System | high | `modules/connector-system.md` | Connectors, wiring, current ratings |
| 18 | Thermal System | high | `modules/thermal-system.md` | Whole-drone thermal analysis |

Technical knowledge the skill uses: STM32, ESP32, ARM, RISC-V MCUs; UART, SPI, I2C, CAN, USB buses; Betaflight / INAV / PX4 / ArduPilot firmware; multilayer PCB design; EMI/EMC and signal integrity; mechanical durability and vibration; energy balance; fault diagnostics; professional validation before civil operation.

---

## 6. Power domains and energy balance

- **Battery math:** max current = capacity_mah / 1000 × C-rating. Max voltage = cells × 4.2 V. Nominal voltage = cells × 3.7 V. A 6S LiPo is 22.2 V nominal, 25.2 V fully charged.
- **Every consumer belongs to a domain.** VBAT (motors, ESC, VTX), 5 V (FC, GPS, camera, receiver), 9 V / 12 V where used. Each domain has a current budget; the sum of its consumers must fit. `power_check.py` enforces this.
- **ESC voltage rating must cover the fully-charged battery.** A 6S battery needs an ESC rated for at least 25.2 V. An ESC rated for 4S (16.8 V) on a 6S battery is destroyed on plug-in.
- **Motor total vs. battery:** the sum of all motors' max current must fit the battery max current. If it does not, either the battery is too small or the motors are too big.
- **BMS:** FPV freestyle quads normally have no BMS on board — the charger balances the pack. A BMS belongs on smart batteries and industrial packs: cell balancing, per-cell cutoff (2.8–3.6 V), over-current protection. When a BMS is present, its cell count must match the battery.

## 7. Firmware compatibility

| Firmware | MCUs | Notes |
| --- | --- | --- |
| Betaflight | STM32F405, F722, F745, H743 | Freestyle/racing. Gyro loop up to 8 kHz (F4/F7), 16 kHz (H7). |
| INAV | STM32F405, F722, F745, H743 | GPS navigation, fixed-wing + multirotor. |
| ArduPilot | STM32F405, F722, F745, H743 | Full autonomy, MAVLink. |
| PX4 | STM32F745, H743 only | Needs F7/H7-class MCU. Does NOT run on an F405. |

- **DShot limits by MCU:** F405 tops out at DShot600; DShot1200 needs F7/H7 timers. `firmware_check.py` enforces both the firmware matrix and the DShot ceiling.
- **GPS protocols:** Betaflight/INAV/ArduPilot accept UBX and NMEA; PX4 accepts UBX.
- **Telemetry by firmware:** Betaflight — CRSF/SBUS/FPort; INAV — CRSF/SBUS/MAVLink; ArduPilot — MAVLink/CRSF/SBUS; PX4 — MAVLink.

## 8. ESC, motors and protocols

- **ESC protocols:** PWM, OneShot125, Multishot, DShot150/300/600/1200. DShot1200 needs BLHeli_32 or AM32 firmware; BLHeli_S tops out at DShot600.
- **ESC firmware:** BLHeli_S, BLHeli_32, AM32. The protocol must be allowed for the firmware (`compatibility_check.py`).
- **Motor KV sanity:** 5-inch freestyle on 6S is typically 1500–2500 KV; on 4S 2300–2800 KV. An inspection hexacopter on 6S is typically 300–900 KV. A KV far outside the range is an error — check the motor datasheet.
- **ESC continuous current is per channel.** Each motor's max current must fit one channel; the PDB must cover the motor total.

## 9. Video link — camera, VTX, VRX

- **Analog:** camera (e.g. RunCam Phoenix 2, Caddx Ratel 2) → analog VTX on 5.8 GHz → analog VRX/goggles. Simple, low latency, lowest cost.
- **Digital:** DJI O3, HDZero, Walksnail Avatar. VTX and VRX must use the SAME protocol — an analog VRX cannot receive a DJI O3 VTX. `compatibility_check.py` enforces the match.
- **VTX power:** 25 mW–2000 mW in the spec. Above 1 W the validator warns — check the local RF power limit before flying. VTX heat is real: an 800 mW analog VTX dissipates several watts and needs a heatsink and airflow (see §12).
- **Camera interfaces:** analog cameras output CVBS; digital systems use their own link (DJI O3, HDZero, Walksnail). The camera type must match the VTX type.

## 10. Sensors and buses

- **Buses:** UART, SPI, I2C, CAN, USB. Gyro/IMU belongs on SPI (fast, low latency); barometer and magnetometer on I2C; GPS on UART; CAN for industrial payloads and redundant sensors.
- **Known parts (config.json):** IMUs MPU6000 / ICM42688 / BMI270; barometers BMP388 / BMP280 / DPS310; magnetometers QMC5883L / HMC5883L / IST8310; GPS u-blox M10 / M9N / M8N. Any other part must be added to the config with its datasheet source — an unknown part FAILS.
- **MCUs:** STM32F405 (Cortex-M4, 168 MHz), STM32F722 (Cortex-M7, 216 MHz), STM32F745 (Cortex-M7, 216 MHz), STM32H743 (Cortex-M7, 480 MHz). ESP32, ARM and RISC-V MCUs are usable for companion boards (telemetry, payload, companion computer) — the FC itself runs on the STM32 targets above in v0.0.1.

## 11. EMI / EMC and signal integrity

- Keep the gyro SPI traces short and away from the power stage. Route the video signal away from switching regulators.
- One solid GND plane under the FC; no routing over plane splits for high-speed signals.
- Switching regulators need their hot loop kept small; decouple per the regulator datasheet.
- VTX antenna away from GPS antenna (RF desense kills GPS lock). GPS module on a stalk or mast, away from the VTX and the power stage.
- USB and any high-speed lines need controlled impedance per the base skill §7.

## 12. Thermal design and thermal system

- **Budget model (what the validator does):** estimated temperature = ambient + power × theta_ja × cooling factor. Cooling factors: none 1.0, heatsink 0.7, heatsink + airflow 0.5, fan 0.4. The estimate must stay under the component max temperature.
- **This is a budget, not a simulation.** Real thermal proof needs a simulation (Elmer FEM) or a lab measurement with a thermal camera. See §19.
- **Hot parts on an FPV drone:** VTX (watts of RF heat), ESC power stage (I²R losses), voltage regulators. All three need copper area, thermal vias and airflow — a VTX buried inside a closed frame overheats.
- **Thermal System (whole drone):** the same budget applied to the whole aircraft — motors, ESCs, battery and VTX together, with flight airflow as the cooling. A hover test without airflow is the worst case.

## 13. Mechanical design, vibration and durability

- FC mounting: soft-mount (rubber grommets / gel) — hard-mounted gyros pick up motor vibration and the flight controller cannot filter it out.
- IMU placement: at the frame center, away from motors, on the soft mount. Never mount the IMU on the power stage.
- Connectors must be locked or glued — vibration undoes friction-fit connectors in flight.
- Frame: carbon plates, standoffs, motor mounts. A crash bends arms before it breaks the stack — design the stack to survive the arm bending, not the other way round.

## 14. Safety system and civil-operation rules (EU)

- **Failsafe is mandatory:** loss of RC link → disarm or return-to-home (where the firmware supports it), never fly away. Failsafe is tested on the bench before the first flight.
- **Arming:** motors arm only on a deliberate switch, with a pre-arm check (sensors OK, battery OK, GPS lock where required). No arming on the bench with props on.
- **Lab testing before flight:** bench power-up, motor test WITHOUT props, range test, failsafe test. Props go on only at the field.
- **EU open category (EASA, Regulations (EU) 2019/947 and 2019/945):** under 25 kg, VLOS, max 120 m above ground, no flight over assemblies of people. Classes: C0 < 250 g, C1 < 900 g, C2 < 4 kg, C3/C4 < 25 kg. Operator registration at 250 g or more (or with a camera). Direct Remote ID required for C1–C3. A1/A3 online training for C1 and up; A2 certificate for C2 close to people. `compatibility_check.py` enforces the altitude limit, the class-mass limits and the Remote ID rule.

## 15. Failure analysis and diagnostics

- Every design lists its single points of failure: one battery, one PDB, one FC. A hexacopter can lose one motor and land; a quadcopter cannot — say so in the review.
- Diagnostics: blackbox logging (Betaflight/INAV) or dataflash logs (ArduPilot/PX4) are required for any crash investigation. A design without logging cannot be diagnosed.
- Common failure modes to check: brownout on punch-out (BEC too weak), desync on rapid throttle (ESC too slow / DShot too fast for the MCU), GPS loss near the VTX (antenna placement), vibration-induced gyro saturation (hard mount).

## 16. Supported outputs

The addon supports these output formats (produced by the base skill + this addon together):

`.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, `.step`, `.stl`, `.gbr`, `.drl`, `.csv` (BOM), `.json`, `.yaml`, `.md`, `.pdf`, `.spice`, `.zip`

`.step` / `.stl` are mechanical exports (frame, mounts, enclosures). `.spice` is the simulation netlist input for ngspice/LTspice. `.zip` is the fab pack (Gerbers + drill + BOM + CPL).

## 17. Note on "engines"

A proposal for this addon listed 14 engines (Architecture, Component, Schematic, PCB, Routing, Signal Integrity, Power Integrity, Thermal, Simulation, Mechanical, Connector, Compatibility, Firmware, Manufacturing, Security, Validation, Documentation, Cost, Benchmark). **Those engines are NOT built here.** They are functions of the main PCB skill (`ai-pcb-design-skill`), not of this addon. This addon only adds drone-specific checks and guidance on top of it. If an engine is needed, it belongs in the base skill.

## 18. Automatic checks

| Script | What it checks | Exit |
| --- | --- | --- |
| `scripts/require_base.py` | Base skill present, name exact, version >= 1.2.1 | 0 / 2 |
| `scripts/power_check.py` | Battery, ESC voltage, motor/battery/PDB currents, power domains, BMS | 0 / 1 / 2 |
| `scripts/compatibility_check.py` | Known parts, ESC protocol vs firmware, motor KV, VTX == VRX, connectors, EU rules | 0 / 1 / 2 |
| `scripts/thermal_check.py` | Thermal budget per component | 0 / 1 / 2 |
| `scripts/firmware_check.py` | Firmware vs MCU, gyro loop, DShot ceiling, GPS/telemetry support | 0 / 1 / 2 |
| `scripts/run_all.py` | All of the above, base skill first | 0 / 1 / 2 |

All scripts: standard library only, exit 2 on setup problems (missing base skill, missing file, bad JSON root), clean errors, no tracebacks on bad input. A bool is never a number in any check.

## 19. Simulations — what this skill can and cannot do

This skill **cannot simulate**. It can only generate simulation inputs and call the tool:

- Signal integrity / EM: generate inputs for openEMS.
- Thermal: generate inputs for Elmer FEM.
- Circuit: generate `.spice` netlists for ngspice / LTspice.
- If the tool is missing or the simulation was not run, the report says `BLOCKED` or `NOT_RUN` — never a fake `PASS`.
- A simulation result is evidence only when the tool, the command and the output file are named. A simulation is not a flight test (§1).

## 20. Changelog

### v0.0.1 — 2026-11-27 (first release)

- 18 modules: Flight Controller, ESC, PDB, BMS, GPS/GNSS, IMU, VTX/VRX, Telemetry, AIO PCB, Firmware, EMI/EMC, Thermal Design, Mechanical Design, Safety System, Camera System, Sensor System, Connector System, Thermal System.
- 4 validators + require_base (exit 2 without the base skill) + run_all; 2 example specs (5-inch freestyle quad, industrial inspection hexacopter), both PASS.
- Quality rules: maturity levels (conceptual / simulated / physically verified), automatic ERC/DRC/DFM when tools are available, full error/warning/unverified log, hardware revisions with backward compatibility, professional verification for safety-critical hardware.
- Output formats, pin-by-pin check workflow, multi-pass placement + batch routing workflow with continuous DRC.
- pytest suite (unit, integration, regression, negative), CI on Python 3.10–3.13.

---

*Made by PTS6845 — https://battingchart300.github.io*
