# Connector System (high)

Connector and wiring control: every connector rated, every wire sized.

- **Battery:** XT60 (60 A), XT90 (90 A), XT150 (150 A), XT30 (30 A). The declared current must not exceed the connector rating — `compatibility_check.py` enforces it.
- **Signal:** JST-GH (3 A), JST-SH (1 A) for GPS/sensors; SMA / RP-SMA / MMCX / U.FL for RF; USB-C (5 A) for configuration.
- **RF connectors are not power connectors:** SMA/MMCX/U.FL carry signal, not current — their rating in the config is 0 A on purpose.
- **Vibration:** lock or glue every connector that flies. A connector that backs out in flight is a crash.
- **Wiring:** wire gauge follows the current (use the base skill's trace/wire tables); signal wires twisted or shielded where they run next to power wires.
