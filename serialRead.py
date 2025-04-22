#!/usr/bin/env python3
"""
read_arduino.py – Stream text lines from an Arduino’s Serial.print()
                  to the console (Ctrl‑C to quit).
"""

import serial          # pip install pyserial
import time
from datetime import datetime

# 1. --- USER SETTINGS -------------------------------------------------
port       = "/dev/tty.usbmodemF412FA75DE8C2"        # Windows example – replace with /dev/ttyACM0, /dev/ttyUSB0, etc.
baud_rate  = 9600        # Must match Serial.begin() in your sketch
log_to_csv = False         # True => also append to a CSV file
csv_path   = "arduino_log.csv"
# ---------------------------------------------------------------------

def open_serial(wait_for_arduino_reset: bool = True) -> serial.Serial:
    """Open the serial port and optionally wait 2 s for the Arduino auto‑reset."""
    ser = serial.Serial(port, baud_rate, timeout=1)
    if wait_for_arduino_reset:
        time.sleep(2)      # most Arduinos reset when the port opens
        ser.reset_input_buffer()
    return ser

def main() -> None:
    print(f"🔌 Opening {port} @ {baud_rate} baud …")
    try:
        ser = open_serial()
    except serial.SerialException as e:
        print(f"❌ Could not open serial port: {e}")
        return

    if log_to_csv:
        print(f"📝 Appending data to {csv_path}")

    try:
        while True:
            line = ser.readline()          # reads up to '\n'
            if not line:
                continue                   # timeout without data
            text = line.decode(errors="replace").rstrip()
            timestamp = datetime.now().isoformat(timespec="seconds")
            print(f"[{timestamp}] {text}")

            if log_to_csv:
                with open(csv_path, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp},{text}\n")

    except KeyboardInterrupt:
        print("\n👋 Exiting on Ctrl‑C")
    finally:
        ser.close()

if __name__ == "__main__":
    main()