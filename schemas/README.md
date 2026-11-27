# Drone spec schema

`drone-spec.schema.json` (JSON Schema draft-07) documents the expected shape of a drone spec. The validators in `scripts/` enforce the rules — types, ranges, known parts, EU limits. The schema alone does not pass a design; only the validators do.

Required top-level sections: `drone`, `battery`, `flight_controller`, `esc`, `motors`, `power_domains`, `thermal`. Optional: `pdb`, `bms`, `gps`, `camera`, `vtx`, `vrx`, `telemetry`, `sensors`, `connectors`, `compliance`.

A bool is never a number: `true` where a current or a lane count belongs is a validation error, not a 1.
