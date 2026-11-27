# Sensor System (high)

Sensor integration: barometer, magnetometer, rangefinder and friends.

- **Barometer:** BMP388 / BMP280 / DPS310 on I2C. Keep it away from heat and prop wash — pressure readings drift with temperature and airflow. Cover it with foam, not tape.
- **Magnetometer:** QMC5883L / HMC5883L / IST8310 on I2C. Keep it away from high-current wires — motor current bends the magnetic field the compass reads.
- **Rangefinder / other sensors:** added to the config only with a datasheet source.
- **Buses:** I2C needs pull-ups; every sensor names its bus and its pins in the spec.
- **Checks:** `compatibility_check.py` (known sensor parts + buses).
