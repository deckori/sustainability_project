import threading
import serial


class SafeSerial:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.lock = threading.Lock()

    def send(self, tag, message):
        # Formats it cleanly: e.g., "[LDR] Left sensor reading: 512"
        payload = f"[{tag}] {message}\n"

        # The lock ensures Thread A finishes its entire line
        # before Thread B can write anything. Zero corruption.
        with self.lock:
            self.ser.write(payload.encode("utf-8"))
            self.ser.flush()
