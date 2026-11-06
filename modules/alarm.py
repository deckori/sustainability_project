from machine import Pin, PWM, ADC
from stamp import get_stamp

EN = Pin(23, Pin.OUT)
print(f"{get_stamp()}, ALARM, STATUS, Connections are set ")


def alarm(enable=1):
    EN.value(enable)
    if enable:
        print(f"{get_stamp()},ALARM,ACTION,Sounded Alarm")
    else:
        print(f"{get_stamp()},ALARM,ACTION,Silenced Alarm")


# alarm(0)
