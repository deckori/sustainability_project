import serial

PORT = "/dev/ttyUSB1"
BAUD = 115200

# Open the serial connection from the PC side
ser = serial.Serial(PORT, BAUD, timeout=1)

# Open specific files on the PC in append mode ("a")
temp_file = open("outputs/temperature_log.txt", "a")
ldr_file = open("outputs/ldr_log.txt", "a")
motor_file = open("outputs/motor_log.txt", "a")
alarm_file = open("outputs/alarm_log.txt", "a")

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
        if line.startswith("[TEMP]"):
            temp_file.write(line + "\n")
            temp_file.flush()  # Forces it to write immediately to disk

        elif line.startswith("[LDR]"):
            ldr_file.write(line + "\n")
            ldr_file.flush()

        elif line.startswith("[MOTOR]"):
            motor_file.write(line + "\n")
            motor_file.flush()

        elif line.startswith("[ALARM]"):
            alarm_file.write(line + "\n")
            alarm_file.flush()

except KeyboardInterrupt:
    print("\nStopping logger and closing files...")

finally:
    ser.close()
    temp_file.close()
    ldr_file.close()
    motor_file.close()
    alarm_file.close()
    print("Done.")
