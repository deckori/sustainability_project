import serial

PORT = "/dev/ttyUSB0"
BAUD = 115200

# Open the serial connection from the PC side
ser = serial.Serial(PORT, BAUD, timeout=1)

# string = "[TEMP] time, temperature"

# Open specific files on the PC in append mode ("a")

with (
    open("temperature_log.txt", "a") as temp_file,
    open("ldr_log.txt", "a") as ldr_file,
    open("motor_log.txt", "a") as motor_file,
    open("alarm_log.txt", "a") as alarm_file,
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
