import sys

sys.path.append("/remote/modules")

from modules.alarm import alarm
from modules.ldr import check_ldr
from modules.temperature import temperature
from modules.turn_motor import stop_motor
import _thread
import time

# _thread.start_new_thread(check_ldr())

DELAY = 2  # seconds between checks

print("[SYSTEM] Starting main loop...")

try:
    while True:
        # _thread.start_new_thread(temperature, ())

        temp = temperature()

        # Run a single check cycle for LDR
        ldr = check_ldr()

        if (temp or ldr) is None:
            alarm()
        else:
            alarm(0)

        # You can handle motor actions here based on 'action' return value if you want
        # e.g., if action == "CLOCKWISE": ...

        time.sleep(DELAY)
except:
    print("\n[SYSTEM] Interrupted by user. Cleaning up...")
    alarm(0)  # Ensure the alarm turns off when exiting
    stop_motor()
    print("[SYSTEM] Stopped safely.")
