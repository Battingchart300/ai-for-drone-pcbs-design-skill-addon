# Architecture

A civil FPV drone is a stack, not a single board:

```
Battery (LiPo, XT60/XT90/XT150)
  └─ PDB (power distribution, current sensing)
       ├─ ESC (4-in-1 or singles) → motors
       ├─ Flight controller (STM32 + IMU + barometer)
       │    ├─ GPS (UART, UBX/NMEA)
       │    ├─ Receiver / telemetry (CRSF / ELRS / MAVLink)
       │    └─ Camera + VTX (analog CVBS or digital link)
       └─ 5 V / 9 V / 12 V BEC rails (FC, GPS, camera, receiver)
```

Rules: the power stage (battery → PDB → ESC → motors) is one subsystem; the flight controller is another; the video link is a third. A fault in one must not take the others down — the PDB fuse/protection and the BEC sizing are what separate a brownout from a crash. AIO boards merge FC + ESC on one PCB; the same blocks still exist, they just share copper and heat (see `modules/aio-pcb.md`).

Maturity: this document is architecture guidance (conceptual). It proves nothing about a built board — see SKILL.md §1.
