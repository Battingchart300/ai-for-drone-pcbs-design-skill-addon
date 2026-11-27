# Design rules

Drone-specific additions to the base skill rules:

1. **High current first.** VBAT and motor phases are routed before anything else, on wide copper, with thermal vias under the FETs. A 100 A path on 1 oz copper needs width — run `trace_width.py` from the base skill on every power net.
2. **Gyro SPI short and clean.** Gyro traces are the shortest on the board, away from the power stage and the VTX. No vias under the IMU if avoidable.
3. **One GND plane under the FC.** No splits under high-speed signals.
4. **VTX and GPS apart.** The VTX antenna and the GPS antenna must be separated — RF desense kills GPS lock. GPS on a mast/stalk where possible.
5. **Connectors locked.** Vibration undoes friction-fit connectors; glue or lock every connector that flies.
6. **Keep-outs.** No components under the battery pad area; no tall parts where the frame clamps the stack.
7. **Revision marking.** Every board revision is printed on the silkscreen (e.g. `REV A`) and logged in the changelog.
