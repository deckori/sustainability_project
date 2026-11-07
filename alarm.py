from machine import Pin
from stamp import get_stamp

EN = Pin(23, Pin.OUT)
print(f"{get_stamp()},ALARM,STATUS,Connections are set")
_alarm_state = None


def alarm(enable=1):
    global _alarm_state

    # If the state hasn't changed, do nothing
    if enable == _alarm_state:
        return

    _alarm_state = enable
    EN.value(enable)

    if enable:
        print(f"{get_stamp()},ALARM,ACTION,Sounded Alarm")
    else:
        print(f"{get_stamp()},ALARM,ACTION,Silenced Alarm")


# Set Alarm to 0 at boot
alarm(0)
