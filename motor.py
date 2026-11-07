from machine import Pin, PWM
from time import sleep
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
    turn_speed.duty_u16(38588 if enable else 0)
    direction.value(state)
    EN.value(enable)


_motor_stopped = False


def stop():
    global _motor_stopped
    if _motor_stopped:
        return

    motor_turn(0, enable=0)
    _motor_stopped = True
    print(f"{get_stamp()},MOTOR,ACTION,Stopped")


def clock(duration=1):
    global _motor_stopped
    _motor_stopped = False
    print(f"{get_stamp()},MOTOR,ACTION,Clockwise")
    motor_turn(1)
    sleep(duration)
    stop()


def anticlock(duration=1):
    global _motor_stopped
    _motor_stopped = False
    print(f"{get_stamp()},MOTOR,ACTION,Anti-clockwise")
    motor_turn(0)
    sleep(duration)
    stop()


# Set motor to stop at boot
stop()

# print("turn")
# stop()
# sleep(2)
# clock()
# anticlock()
# print("set")
