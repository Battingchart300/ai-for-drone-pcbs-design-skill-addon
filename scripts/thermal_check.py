#!/usr/bin/env python3
"""thermal_check.py — thermal limits for FPV components.

Model: estimated temperature = ambient + power_w * theta_ja * cooling
factor. Theta_ja (deg C per W) and the cooling factor come from the
spec and config.json; the skill does NOT simulate heat flow — this
is a first-order budget check, and a real thermal simulation
(openEMS / Elmer FEM) or a lab measurement is still required for
safety-critical hardware (see SKILL.md §12 and simulations/).

Rules: every thermal component needs power, theta, a max temperature
and a known cooling type; the estimate must stay under the max.
A missing thermal section, a bool where a number belongs, or a
non-finite value is an error.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (incl. base
skill missing — the hard dependency). Standard library only.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common
from common import (Report, check_base_or_exit, is_num, load_config,
                    load_spec)

NAME = "thermal_check"


def main():
    ap = argparse.ArgumentParser(
        description="Validate FPV thermal limits.")
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

    thermal = spec.get("thermal")
    if not isinstance(thermal, dict):
        rep.error("thermal section missing or not an object")
        return rep.finish()
    ambient = thermal.get("ambient_c", 25)
    if not is_num(ambient):
        rep.error(f"thermal.ambient_c must be a number, got {ambient!r}")
        return rep.finish()
    if thermal.get("ambient_c") is None:
        rep.warning("thermal.ambient_c not given, assuming 25 C")

    components = thermal.get("components")
    if not isinstance(components, list) or not components:
        rep.error("thermal.components must be a non-empty list")
        return rep.finish()
    factors = cfg["cooling_factors"]
    for c in components:
        if not isinstance(c, dict):
            rep.error(f"thermal component is not an object: {c!r}")
            continue
        ref = c.get("ref", "?")
        power = c.get("power_w")
        theta = c.get("theta_ja_c_per_w")
        tmax = c.get("max_temp_c")
        cooling = c.get("cooling")
        if not is_num(power) or power < 0:
            rep.error(f"thermal {ref}: power_w must be a non-negative "
                      f"number, got {power!r}")
            continue
        if not is_num(theta) or theta <= 0:
            rep.error(f"thermal {ref}: theta_ja_c_per_w must be a positive "
                      f"number, got {theta!r}")
            continue
        if not is_num(tmax) or tmax <= 0:
            rep.error(f"thermal {ref}: max_temp_c must be a positive "
                      f"number, got {tmax!r}")
            continue
        if cooling not in factors:
            rep.error(f"thermal {ref}: cooling must be one of "
                      f"{list(factors)}, got {cooling!r}")
            continue
        est = ambient + power * theta * factors[cooling]
        if est > tmax:
            rep.error(f"thermal {ref}: estimated {est:.1f} C exceeds the "
                      f"max {tmax} C (power {power} W, theta {theta} "
                      f"C/W, cooling {cooling}) — add a heatsink, "
                      f"airflow, or reduce the power")
        elif est > tmax - 10:
            rep.warning(f"thermal {ref}: estimated {est:.1f} C is within "
                        f"10 C of the max {tmax} C — thin margin")

    return rep.finish()


if __name__ == "__main__":
    sys.exit(main())
