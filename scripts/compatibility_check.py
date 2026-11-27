#!/usr/bin/env python3
"""compatibility_check.py — component / interface compatibility.

Checks that every named part is a real, known part from the tables
in config.json, that interfaces match (VTX protocol == VRX protocol,
ESC protocol allowed for the ESC firmware, motor KV in range for the
drone class and cell count), that connectors are rated for their
current, and that the EU civil-operation rules fit the drone
(EASA open category: 120 m max altitude, class-mark mass limits,
Remote ID where required, registration at >= 250 g).

An unknown part name is an ERROR, not a warning: an invented part
must FAIL. A value of UNVERIFIED is also an error — it means the
part was never verified against a datasheet.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (incl. base
skill missing — the hard dependency). Standard library only.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common
from common import (Report, check_base_or_exit, is_int, is_num,
                    is_nonempty_str, is_unverified, load_config, load_spec)

NAME = "compatibility_check"


def known(rep, value, table, what):
    """Error unless value is a known, verified entry of the table."""
    if is_unverified(value):
        rep.error(f"{what} is UNVERIFIED — verify the part against its "
                  f"datasheet before the design can pass")
        return False
    if not is_nonempty_str(value):
        rep.error(f"{what} must be a non-empty string, got {value!r}")
        return False
    if value not in table:
        rep.error(f"{what} {value!r} is not a known verified part "
                  f"(known: {', '.join(table)}) — if this is a real "
                  f"part, add it to config.json with its datasheet "
                  f"source; an invented part must FAIL")
        return False
    return True


def main():
    ap = argparse.ArgumentParser(
        description="Validate FPV component compatibility.")
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

    drone = spec.get("drone")
    if not isinstance(drone, dict):
        rep.error("drone section missing or not an object")
        return rep.finish()
    dclass = drone.get("class")
    if not is_nonempty_str(dclass) or dclass not in cfg["drone_classes"]:
        rep.error(f"drone.class must be one of {cfg['drone_classes']}, "
                  f"got {dclass!r}")
        dclass = None
    mtom = drone.get("mtom_g")
    if not is_num(mtom) or mtom <= 0:
        rep.error(f"drone.mtom_g must be a positive number, got {mtom!r}")
        mtom = None

    battery = spec.get("battery")
    cells = battery.get("cells") if isinstance(battery, dict) else None

    fc = spec.get("flight_controller")
    if not isinstance(fc, dict):
        rep.error("flight_controller section missing or not an object")
        return rep.finish()
    known(rep, fc.get("mcu"), list(cfg["mcus"]), "flight_controller.mcu")
    known(rep, fc.get("imu"), cfg["imus"], "flight_controller.imu")
    if fc.get("barometer") is not None:
        known(rep, fc.get("barometer"), cfg["barometers"],
              "flight_controller.barometer")
    fw = fc.get("firmware")
    if is_nonempty_str(fw) and fw not in cfg["firmware_mcus"]:
        rep.error(f"flight_controller.firmware {fw!r} is unknown "
                  f"(known: {', '.join(cfg['firmware_mcus'])})")
    if is_unverified(fw):
        rep.error("flight_controller.firmware is UNVERIFIED")

    esc = spec.get("esc")
    if not isinstance(esc, dict):
        rep.error("esc section missing or not an object")
        return rep.finish()
    proto = esc.get("protocol")
    allowed_fw = cfg["esc_protocol_min_firmware"].get(proto)
    if allowed_fw is None:
        rep.error(f"esc.protocol {proto!r} is unknown "
                  f"(known: {', '.join(cfg['esc_protocol_min_firmware'])})")
    else:
        efw = esc.get("firmware")
        if is_unverified(efw):
            rep.error("esc.firmware is UNVERIFIED")
        elif efw not in allowed_fw:
            rep.error(f"esc.protocol {proto} is not supported by ESC "
                      f"firmware {efw!r} (needs one of: "
                      f"{', '.join(allowed_fw)})")

    motors = spec.get("motors")
    if isinstance(motors, list):
        for m in motors:
            if not isinstance(m, dict):
                continue
            ref = m.get("ref", "?")
            kv = m.get("kv")
            if not is_int(kv) or kv <= 0:
                rep.error(f"motor {ref}: kv must be a positive integer, "
                          f"got {kv!r}")
                continue
            if dclass and is_int(cells):
                ranges = cfg["kv_ranges"].get(dclass, {})
                lo_hi = ranges.get(str(cells))
                if lo_hi and not (lo_hi[0] <= kv <= lo_hi[1]):
                    rep.error(f"motor {ref}: kv {kv} is outside the "
                              f"typical range {lo_hi[0]}-{lo_hi[1]} for "
                              f"{dclass} on {cells}S — check the motor "
                              f"datasheet (wrong KV burns motors or "
                              f"gives no thrust)")

    gps = spec.get("gps")
    if gps is not None:
        if not isinstance(gps, dict):
            rep.error("gps section is not an object")
        else:
            known(rep, gps.get("module"), cfg["gps_modules"], "gps.module")
            if gps.get("protocol") not in ("UBX", "NMEA"):
                rep.error(f"gps.protocol must be UBX or NMEA, "
                          f"got {gps.get('protocol')!r}")

    camera = spec.get("camera")
    if camera is not None:
        if not isinstance(camera, dict):
            rep.error("camera section is not an object")
        else:
            ctype = camera.get("type")
            if ctype not in cfg["cameras"]:
                rep.error(f"camera.type must be analog or digital, "
                          f"got {ctype!r}")
            else:
                known(rep, camera.get("sensor"), cfg["cameras"][ctype],
                      "camera.sensor")

    vtx = spec.get("vtx")
    vrx = spec.get("vrx")
    vtx_proto = vtx.get("protocol") if isinstance(vtx, dict) else None
    if isinstance(vtx, dict):
        if vtx_proto not in cfg["vtx_protocols"]:
            rep.error(f"vtx.protocol {vtx_proto!r} is unknown "
                      f"(known: {', '.join(cfg['vtx_protocols'])})")
        pmw = vtx.get("power_mw")
        if not is_num(pmw) or not 25 <= pmw <= 2000:
            rep.error(f"vtx.power_mw must be 25-2000 mW, got {pmw!r}")
        elif pmw > 1000:
            rep.warning(f"vtx.power_mw {pmw} mW is above 1 W — check the "
                        f"local RF power limit before flying")
    if isinstance(vrx, dict):
        vrx_proto = vrx.get("protocol")
        if vrx_proto not in cfg["vtx_protocols"]:
            rep.error(f"vrx.protocol {vrx_proto!r} is unknown")
        elif (vtx_proto in cfg["vtx_protocols"]
              and vrx_proto != vtx_proto):
            rep.error(f"VRX protocol {vrx_proto!r} does not match VTX "
                      f"protocol {vtx_proto!r} — the video link cannot work")

    telemetry = spec.get("telemetry")
    if telemetry is not None:
        if not isinstance(telemetry, dict):
            rep.error("telemetry section is not an object")
        else:
            known(rep, telemetry.get("protocol"),
                  cfg["telemetry_protocols"], "telemetry.protocol")

    sensors = spec.get("sensors")
    if sensors is not None:
        if not isinstance(sensors, list):
            rep.error("sensors must be a list")
        else:
            known_parts = {"barometer": cfg["barometers"],
                           "magnetometer": cfg["magnetometers"]}
            for s in sensors:
                if not isinstance(s, dict):
                    rep.error(f"sensor entry is not an object: {s!r}")
                    continue
                stype = s.get("type")
                table = known_parts.get(stype)
                if table is None:
                    rep.error(f"sensor type {stype!r} is unknown "
                              f"(known: barometer, magnetometer)")
                    continue
                known(rep, s.get("part"), table, f"sensor {stype} part")
                if s.get("bus") not in cfg["buses"]:
                    rep.error(f"sensor {stype}: bus must be one of "
                              f"{cfg['buses']}, got {s.get('bus')!r}")

    connectors = spec.get("connectors")
    if connectors is not None:
        if not isinstance(connectors, list):
            rep.error("connectors must be a list")
        else:
            for c in connectors:
                if not isinstance(c, dict):
                    rep.error(f"connector entry is not an object: {c!r}")
                    continue
                ctype = c.get("type")
                if ctype not in cfg["connector_max_a"]:
                    rep.error(f"connector type {ctype!r} is unknown "
                              f"(known: "
                              f"{', '.join(cfg['connector_max_a'])})")
                    continue
                cmax = c.get("max_current_a")
                if not is_num(cmax) or cmax <= 0:
                    rep.error(f"connector {c.get('name', '?')}: "
                              f"max_current_a must be a positive number, "
                              f"got {cmax!r}")
                    continue
                rated = cfg["connector_max_a"][ctype]
                if rated > 0 and cmax > rated:
                    rep.error(f"connector {c.get('name', '?')}: "
                              f"{cmax} A exceeds the {ctype} rating "
                              f"of {rated} A")

    comp = spec.get("compliance")
    if comp is not None:
        if not isinstance(comp, dict):
            rep.error("compliance section is not an object")
        else:
            if comp.get("region") == "EU":
                eu = cfg["eu"]
                alt = comp.get("max_altitude_m")
                if is_num(alt) and alt > eu["max_altitude_m"]:
                    rep.error(f"compliance.max_altitude_m {alt} m exceeds "
                              f"the EU open-category limit of "
                              f"{eu['max_altitude_m']} m")
                mark = comp.get("class_mark")
                if mark is not None:
                    limit = eu["class_limits_g"].get(mark)
                    if limit is None:
                        rep.error(f"compliance.class_mark {mark!r} is "
                                  f"unknown (C0-C4)")
                    elif is_num(mtom) and mtom >= limit:
                        rep.error(f"MTOM {mtom} g exceeds the {mark} "
                                  f"class limit of {limit} g")
                    if mark in eu["remote_id_required"] \
                            and comp.get("remote_id") is not True:
                        rep.error(f"class {mark} requires Direct Remote ID "
                                  f"in the EU — remote_id must be true")
                if is_num(mtom) and mtom >= eu["registration_mtom_g"]:
                    if comp.get("operator_registered") is not True:
                        rep.warning(f"MTOM {mtom} g needs operator "
                                    f"registration in the EU (>= "
                                    f"{eu['registration_mtom_g']} g)")

    return rep.finish()


if __name__ == "__main__":
    sys.exit(main())
