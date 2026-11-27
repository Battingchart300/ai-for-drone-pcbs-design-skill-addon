#!/usr/bin/env python3
"""firmware_check.py — flight-controller firmware compatibility.

Checks:
  1. The firmware is known and supports the FC MCU
     (PX4 needs an F7/H7-class MCU — it does NOT run on an F405).
  2. The gyro loop rate fits the MCU (F4/F7: 8 kHz, H7: 16 kHz).
  3. The ESC protocol fits the MCU (DShot1200 needs F7/H7 timers;
     an F405 tops out at DShot600).
  4. The firmware version is a real version string, not empty.
  5. The GPS protocol and the telemetry protocol are supported
     by the chosen firmware.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (incl. base
skill missing — the hard dependency). Standard library only.
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common
from common import (Report, check_base_or_exit, is_int, is_nonempty_str,
                    is_unverified, load_config, load_spec)

NAME = "firmware_check"
DSHOT_ORDER = ["PWM", "OneShot125", "Multishot", "DShot150", "DShot300",
               "DShot600", "DShot1200"]
VERSION_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")


def main():
    ap = argparse.ArgumentParser(
        description="Validate FPV firmware compatibility.")
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

    fc = spec.get("flight_controller")
    if not isinstance(fc, dict):
        rep.error("flight_controller section missing or not an object")
        return rep.finish()
    fw = fc.get("firmware")
    mcu = fc.get("mcu")
    if is_unverified(fw):
        rep.error("flight_controller.firmware is UNVERIFIED")
        return rep.finish()
    if not is_nonempty_str(fw) or fw not in cfg["firmware_mcus"]:
        rep.error(f"flight_controller.firmware {fw!r} is unknown "
                  f"(known: {', '.join(cfg['firmware_mcus'])})")
        return rep.finish()
    if is_nonempty_str(mcu):
        supported = cfg["firmware_mcus"][fw]
        if mcu not in supported:
            rep.error(f"firmware {fw} does not support MCU {mcu} "
                      f"(supported: {', '.join(supported)}) — "
                      f"PX4, for example, needs an F7/H7-class MCU "
                      f"and does not run on an F405")
    mcu_info = cfg["mcus"].get(mcu) if is_nonempty_str(mcu) else None
    if mcu_info is None:
        rep.error(f"flight_controller.mcu {mcu!r} is unknown "
                  f"(known: {', '.join(cfg['mcus'])})")
        return rep.finish()

    version = fc.get("firmware_version")
    if not is_nonempty_str(version) or not VERSION_RE.match(version):
        rep.error(f"flight_controller.firmware_version must look like "
                  f"'4.5.0', got {version!r}")

    loop = fc.get("gyro_loop_hz")
    if not is_int(loop) or loop <= 0:
        rep.error(f"flight_controller.gyro_loop_hz must be a positive "
                  f"integer, got {loop!r}")
    elif loop > mcu_info["max_gyro_loop_hz"]:
        rep.error(f"gyro_loop_hz {loop} exceeds the {mcu} maximum of "
                  f"{mcu_info['max_gyro_loop_hz']} Hz")

    esc = spec.get("esc")
    if isinstance(esc, dict):
        proto = esc.get("protocol")
        if proto in DSHOT_ORDER:
            max_proto = mcu_info["max_dshot"]
            if DSHOT_ORDER.index(proto) > DSHOT_ORDER.index(max_proto):
                rep.error(f"ESC protocol {proto} exceeds the {mcu} "
                          f"maximum of {max_proto} (DShot1200 needs "
                          f"F7/H7 timers)")

    gps = spec.get("gps")
    if isinstance(gps, dict):
        gproto = gps.get("protocol")
        allowed = cfg["firmware_gps_protocols"].get(fw, [])
        if gproto not in allowed:
            rep.error(f"GPS protocol {gproto!r} is not supported by "
                      f"firmware {fw} (supported: {', '.join(allowed)})")

    telemetry = spec.get("telemetry")
    if isinstance(telemetry, dict):
        tproto = telemetry.get("protocol")
        allowed = cfg["firmware_telemetry"].get(fw, [])
        if tproto not in allowed:
            rep.error(f"telemetry protocol {tproto!r} is not supported "
                      f"by firmware {fw} (supported: "
                      f"{', '.join(allowed)})")

    return rep.finish()


if __name__ == "__main__":
    sys.exit(main())
