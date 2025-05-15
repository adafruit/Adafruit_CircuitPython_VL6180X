# SPDX-FileCopyrightText: 2022 Jonas Schatz
# SPDX-License-Identifier: MIT

# Demo of reading the range from the VL6180x distance sensor in
# different access modes (single shot, continuous, history)

import time

import board
import busio

import adafruit_vl6180x

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
sensor = adafruit_vl6180x.VL6180X(i2c)

# Define the number of measurements
# n_measurements = 1000 will run for about 2 minutes
n_measurements: int = 100

# Single shot
print("Starting single-shot measurement...")
start = time.time()
for i in range(n_measurements):
    range_mm = sensor.range
print(f"Performed {n_measurements} measurements in single-shot mode in {time.time() - start}s\n")

# Sleep is required, otherwise the sensor might freeze when switching to
# continuous mode too quickly after the last single shot
time.sleep(2)

# Continuous with no delay between measurements
print("Starting continuous measurement...")
sensor.start_range_continuous(20)
start = time.time()
for i in range(n_measurements):
    range_mm = sensor.range
print(f"Performed {n_measurements} measurements in continuous mode in {time.time() - start}s\n")

# Continuous, reading data from history.
# Note: This is fast, since you don't have to wait for the measurement to be
# finished. On the downside, you will read the same value multiple times
print("Starting continuous measurement with history enabled...")
start = time.time()
for i in range(n_measurements):
    range_mm = sensor.range_from_history
print(
    f"Performed {n_measurements} measurements in continuous mode, reading form history, in {time.time() - start}s\n"  # noqa: E501
)

sensor.stop_range_continuous()
print("Finished")
