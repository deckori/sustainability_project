from machine import Pin, PWM, ADC


def alarm(enable=1):
    EN = Pin(23, Pin.OUT)
    EN.value(enable)


# alarm(0)
