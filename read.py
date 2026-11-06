import os
import serial

PORT = "/dev/ttyUSB0"
BAUD = 115200

# Open the serial connection from the PC side
ser = serial.Serial(PORT, BAUD, timeout=1)
# Clear past bytes
ser.reset_input_buffer()

# string = "[TEMP] time, temperature"

# Open specific files on the PC in append mode ("a")

with (
    open("outputs.csv", "a") as outputs,
):
    print(f"Listening on {PORT}... Writing output to specific files.")

    try:
        while True:
            # Read line from ESP32 over USB
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue

            # Print to PC terminal so you can see it live
            print(f"Raw -> {line}")

            # Route and write to specific files based on tags sent from ESP32
            outputs.write(line + "\n")

    except KeyboardInterrupt:
        print("\nStopping logger and closing files...")
