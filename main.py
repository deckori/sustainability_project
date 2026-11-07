from stamp import get_stamp

print(f"{get_stamp()},SYSTEM,STATUS,Initializing system...")

from alarm import alarm
from ldr import check_ldr
from temperature import temperature
from turn_motor import stop_motor
import _thread
import time

# _thread.start_new_thread(check_ldr())

DELAY = 2  # seconds between checks

print(f"{get_stamp()},SYSTEM,STATUS,Starting main loop...")

try:
    while True:
        # _thread.start_new_thread(temperature, ())

        temp = temperature()

        # Run a single check cycle for LDR
        ldr = check_ldr()

        if temp is None or ldr is None:
            alarm()
        else:
            alarm(0)

        # You can handle motor actions here based on 'action' return value if you want
        # e.g., if action == "CLOCKWISE": ...

        time.sleep(DELAY)
except KeyboardInterrupt:
    print(f"{get_stamp()},SYSTEM,STATUS,Interrupted by user. Cleaning up...")
    alarm(0)  # Ensure the alarm turns off when exiting
    stop_motor()
    print(f"{get_stamp()},SYSTEM,STATUS,Stopped safely.")
