#!/usr/bin/env python3
"""power_check.py — power-domain and energy-balance validation.

Checks:
  1. Battery: cells / capacity / C-rating are real numbers; max
     battery current = capacity_mah / 1000 * c_rating.
  2. ESC: max battery voltage (cells * 4.2 V) must not exceed the
     ESC voltage rating; each motor's max current must fit the
     ESC continuous current (per channel).
  3. Motors: total max current must fit the battery max current.
  4. PDB: max current must cover the motor total.
  5. Power domains: every domain has a voltage and a current
     budget; the sum of its consumers must fit; a VBAT domain
     must match the battery nominal voltage; low-voltage domains
     (5 V / 9 V / 12 V) must not exceed the battery max voltage.
  6. BMS (when present): cell count must match the battery, cutoff
     voltage per cell must be 2.8-3.6 V, balance current positive.
  7. UNVERIFIED anywhere in the checked values is an error —
     an unverified number is not a checked number.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (incl. base
skill missing — the hard dependency). Standard library only.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common
from common import (CREDIT, Report, check_base_or_exit, is_int, is_num,
                    is_nonempty_str, is_unverified, load_config, load_spec)

NAME = "power_check"


def main():
    ap = argparse.ArgumentParser(description="Validate FPV power domains.")
    ap.add_argument("--spec", default=None, help="Drone spec JSON")
    ap.add_argument("--base-skill", default=None,
                    help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()
    check_base_or_exit(args.base_skill)

    spec_path = args.spec or str(HERE.parent / "examples"
                                  / "spec_5inch_freestyle.json")
    spec, code = load_spec(spec_path)
    if spec is None:
        return code
    cfg = load_config()
    if cfg is None:
        return 2
    rep = Report(NAME)
    cell = cfg["lipo_cell_v"]

    battery = spec.get("battery")
    if not isinstance(battery, dict):
        rep.error("battery section missing or not an object")
        return rep.finish()
    cells = battery.get("cells")
    capacity = battery.get("capacity_mah")
    c_rating = battery.get("c_rating")
    if not is_int(cells) or not 1 <= cells <= 12:
        rep.error(f"battery.cells must be an integer 1-12, got {cells!r}")
        return rep.finish()
    if not is_num(capacity) or capacity <= 0:
        rep.error(f"battery.capacity_mah must be a positive number, "
                  f"got {capacity!r}")
    if not is_num(c_rating) or c_rating <= 0:
        rep.error(f"battery.c_rating must be a positive number, "
                  f"got {c_rating!r}")
    if rep.errors:
        return rep.finish()
    if is_unverified(battery.get("type")):
        rep.error("battery.type is UNVERIFIED — verify the cell chemistry")
    bat_max_a = capacity / 1000.0 * c_rating
    # Round: 6 * 4.2 is 25.200000000000003 in float — a 25.2 V ESC
    # must not fail on that.
    bat_max_v = round(cells * cell["max"], 3)
    bat_nom_v = round(cells * cell["nominal"], 3)

    esc = spec.get("esc")
    if not isinstance(esc, dict):
        rep.error("esc section missing or not an object")
        return rep.finish()
    esc_vmax = esc.get("voltage_max_v")
    if not is_num(esc_vmax) or esc_vmax <= 0:
        rep.error(f"esc.voltage_max_v must be a positive number, "
                  f"got {esc_vmax!r}")
    elif esc_vmax < bat_max_v:
        rep.error(f"esc.voltage_max_v {esc_vmax} V is below the battery "
                  f"max voltage {bat_max_v} V ({cells}S LiPo) — "
                  f"the ESC would be destroyed")
    esc_cont = esc.get("continuous_current_a")
    if not is_num(esc_cont) or esc_cont <= 0:
        rep.error(f"esc.continuous_current_a must be a positive number, "
                  f"got {esc_cont!r}")
    if is_unverified(esc.get("firmware")):
        rep.error("esc.firmware is UNVERIFIED — verify the ESC firmware")

    motors = spec.get("motors")
    if not isinstance(motors, list) or not motors:
        rep.error("motors must be a non-empty list")
        return rep.finish()
    motor_total = 0.0
    for m in motors:
        if not isinstance(m, dict):
            rep.error(f"motor entry is not an object: {m!r}")
            continue
        ref = m.get("ref", "?")
        mc = m.get("max_current_a")
        if not is_num(mc) or mc <= 0:
            rep.error(f"motor {ref}: max_current_a must be a positive "
                      f"number, got {mc!r}")
            continue
        motor_total += mc
        if is_num(esc_cont) and mc > esc_cont:
            rep.error(f"motor {ref}: max current {mc} A exceeds the ESC "
                      f"continuous current {esc_cont} A per channel")
    if motor_total > bat_max_a:
        rep.error(f"motors total max current {motor_total:.1f} A exceeds "
                  f"the battery max current {bat_max_a:.1f} A "
                  f"({capacity} mAh x {c_rating}C)")

    pdb = spec.get("pdb")
    if pdb is not None:
        if not isinstance(pdb, dict):
            rep.error("pdb section is not an object")
        else:
            pdb_max = pdb.get("max_current_a")
            if not is_num(pdb_max) or pdb_max <= 0:
                rep.error(f"pdb.max_current_a must be a positive number, "
                          f"got {pdb_max!r}")
            elif motor_total > pdb_max:
                rep.error(f"motors total {motor_total:.1f} A exceeds the "
                          f"PDB max current {pdb_max} A")

    domains = spec.get("power_domains")
    if not isinstance(domains, list) or not domains:
        rep.error("power_domains must be a non-empty list")
    else:
        for d in domains:
            if not isinstance(d, dict):
                rep.error(f"power domain entry is not an object: {d!r}")
                continue
            name = d.get("name", "?")
            volt = d.get("voltage_v")
            budget = d.get("max_current_a")
            if not is_num(volt) or volt <= 0:
                rep.error(f"domain {name}: voltage_v must be a positive "
                          f"number, got {volt!r}")
                continue
            if not is_num(budget) or budget <= 0:
                rep.error(f"domain {name}: max_current_a must be a positive "
                          f"number, got {budget!r}")
                continue
            if name.upper() == "VBAT" and abs(volt - bat_nom_v) > 0.5:
                rep.error(f"domain VBAT voltage {volt} V does not match "
                          f"the battery nominal voltage {bat_nom_v} V")
            if volt > bat_max_v:
                rep.error(f"domain {name} voltage {volt} V exceeds the "
                          f"battery max voltage {bat_max_v} V")
            consumers = d.get("consumers")
            if not isinstance(consumers, list):
                rep.error(f"domain {name}: consumers must be a list")
                continue
            total = 0.0
            for c in consumers:
                if not isinstance(c, dict):
                    rep.error(f"domain {name}: consumer is not an object: "
                              f"{c!r}")
                    continue
                ca = c.get("current_a")
                if not is_num(ca) or ca < 0:
                    rep.error(f"domain {name}: consumer {c.get('ref', '?')} "
                              f"current_a must be a non-negative number, "
                              f"got {ca!r}")
                    continue
                total += ca
            if total > budget:
                rep.error(f"domain {name}: consumers draw {total:.2f} A, "
                          f"over the {budget} A budget")

    bms = spec.get("bms")
    if isinstance(bms, dict) and bms.get("present") is True:
        if bms.get("cells") != cells:
            rep.error(f"bms.cells {bms.get('cells')} does not match "
                      f"battery.cells {cells}")
        cutoff = bms.get("cutoff_v_per_cell")
        if not is_num(cutoff) or not (cell["cutoff_min"]
                                      <= cutoff <= cell["cutoff_max"]):
            rep.error(f"bms.cutoff_v_per_cell must be "
                      f"{cell['cutoff_min']}-{cell['cutoff_max']} V, "
                      f"got {cutoff!r}")
        bal = bms.get("balance_current_ma")
        if not is_num(bal) or bal <= 0:
            rep.error(f"bms.balance_current_ma must be a positive number, "
                      f"got {bal!r}")

    return rep.finish()


if __name__ == "__main__":
    sys.exit(main())
