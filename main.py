from stamp import get_stamp

print(f"{get_stamp()},SYSTEM,STATUS,Initializing system...")

from alarm import alarm
from ldr import check_ldr
from temperature import temperature
import motor
import time

DELAY = 2  # seconds between checks

print(f"{get_stamp()},SYSTEM,STATUS,Starting main loop...")

try:
    while True:
        has_error = False

        # 1. Temperature check
        try:
            temp = temperature()
            if temp is None:
                has_error = True
        except Exception as e:
            print(f"{get_stamp()},TEMP,ERROR,{e}")
            has_error = True

        # 2. LDR check
        try:
            ldr = check_ldr()
            if ldr is None:
                has_error = True
        except Exception as e:
            print(f"{get_stamp()},LDR,ERROR,{e}")
            has_error = True

        # 3. Alarm logic: sound on any error, silence when system is healthy
        alarm(1 if has_error else 0)

        time.sleep(DELAY)
except KeyboardInterrupt:
    print(f"{get_stamp()},SYSTEM,STATUS,Interrupted by user. Cleaning up...")
    alarm(0)  # Ensure the alarm turns off when exiting
    motor.stop()
    print(f"{get_stamp()},SYSTEM,STATUS,Stopped safely.")
