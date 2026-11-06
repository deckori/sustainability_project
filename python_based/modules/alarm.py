from machine import Pin, PWM, ADC
from stamp import stamp

EN = Pin(23, Pin.OUT)
print(f"{stamp}, ALARM, STATUS, Connections are set ")


def alarm(enable=1):
    EN.value(enable)
    if enable:
        print(f"{stamp}, ALARM, ACTION, Sounded Alarm")
    else:
        print(f"{stamp}, ALARM, ACTION, Silenced Alarm")


# alarm(0)
