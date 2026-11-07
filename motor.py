from machine import Pin, PWM, ADC, RTC
from time import sleep, ticks_ms
from stamp import get_stamp

# Initialize motor driver pins and PWM frequency (1 kHz)
RPWM = PWM(Pin(25), freq=1000)
LPWM = Pin(26, Pin.OUT)
EN = Pin(27, Pin.OUT)
print(f"{get_stamp()},MOTOR,STATUS,Pins set")

turn_speed = RPWM
direction = LPWM


def motor_turn(state, enable=1):
    # Motor speed value mapped to MicroPython's 16-bit PWM range (0 - 65535)
    # A value of 38588 roughly corresponds to ~60% speed.
    turn_speed.duty_u16(38588)
    direction.value(state)
    EN.value(enable)


_motor_state = None

_motor_state = None  # Tracks current state: "CLOCKWISE", "ANTICLOCKWISE", "STOP"


def _set_motor_state(state, action_label):
    global _motor_state

    # If the state hasn't changed, do nothing
    if state == _motor_state:
        return

    _motor_state = state

    if state == "CLOCKWISE":
        motor_turn(1)
    elif state == "ANTICLOCKWISE":
        motor_turn(0)
    else:  # STOP
        motor_turn(0, enable=0)

    print(f"{get_stamp()}, MOTOR, ACTION, {action_label}")
    sleep(1)


def clock():
    _set_motor_state("CLOCKWISE", "Clockwise")


def anticlock():
    _set_motor_state("ANTICLOCKWISE", "Anti-clockwise")


def stop():
    _set_motor_state("STOP", "Stopped")


# Set motor to stop at boot
stop()


# print("turn")
# stop()
# sleep(2)
# clock()
# anticlock()
# print("set")
