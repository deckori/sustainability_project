from modules.alarm import alarm
from modules.ldr import check_ldr
from modules.temperature import temperature
import _thread
import time

# _thread.start_new_thread(check_ldr())

DELAY = 1  # seconds between checks

print("[SYSTEM] Starting main loop...")

while True:
    # Run a single check cycle for LDR
    action = check_ldr()

    print("[CHECK]", action)

    if action == None:
        alarm()
    else:
        alarm(0)

    # You can handle motor actions here based on 'action' return value if you want
    # e.g., if action == "CLOCKWISE": ...

    time.sleep(DELAY)
