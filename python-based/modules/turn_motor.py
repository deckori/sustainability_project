from machine import Pin, PWM, ADC
from time import sleep, ticks_ms


def motor_turn(state, speed=38588, enable=1):
    # Initialize motor driver pins and PWM frequency (1 kHz)
    RPWM = PWM(Pin(25), freq=1000)
    LPWM = Pin(26, Pin.OUT)
    EN = Pin(27, Pin.OUT)

    turn_speed = RPWM
    direction = LPWM

    # Motor speed value mapped to MicroPython's 16-bit PWM range (0 - 65535)
    # A value of 38588 roughly corresponds to ~60% speed.
    turn_speed.duty_u16(speed)
    direction.value(state)
    EN.value(enable)


def stop_motor():
    # Cuts all power and disables the motor driver
    motor_turn(state=0, enable=0)


def turn_clockwise():
    motor_turn(0)


def turn_anticlockwise():
    motor_turn(1)


print("turn")
turn_anticlockwise()
print("set")
