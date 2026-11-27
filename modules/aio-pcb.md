# AIO PCB (high)

All-in-one board: flight controller + ESC (and often PDB + BEC) on one PCB.

- **Pros:** one board, less wiring, lighter stack, cheaper build.
- **Cons:** shared copper and shared heat — the ESC heats the FC; one fault can kill both; a dead ESC means replacing the whole board.
- **Rules:** the same blocks still exist and the same checks apply (power, compatibility, thermal, firmware). The thermal budget matters MORE on an AIO, because the VTX/ESC heat has nowhere else to go.
- **Spec:** `flight_controller.stack: "aio"` marks an AIO build.
