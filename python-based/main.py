from machine import Pin, ADC, PWM
from time import sleep

# ---- Settings ----
DEADBAND = 300  # how big a left/right difference must be before moving
SPEED = 600  # motor speed, 0-1023
MOVE_TIME = 0.2  # seconds the motor runs per correction
DELAY = 1  # seconds between checks

# ---- LDRs (each divider: 3.3V -> LDR -> pin -> 10k -> GND) ----
left_ldr = ADC(Pin(32))  # was A0 in the drawing
right_ldr = ADC(Pin(33))  # was A1 in the drawing
left_ldr.atten(ADC.ATTN_11DB)  # read the full 0-3.3 V range
right_ldr.atten(ADC.ATTN_11DB)

# ---- IBT-2 driver inputs ----
RPWM = PWM(Pin(25), freq=1000)  # turns right
LPWM = PWM(Pin(26), freq=1000)  # turns left
R_EN = Pin(27, Pin.OUT)
L_EN = Pin(14, Pin.OUT)
RPWM.duty(0)
LPWM.duty(0)


def run(direction):
    if direction > 0:
        LPWM.duty(0)
        RPWM.duty(SPEED)
        R_EN.value(1)
        L_EN.value(1)
    else:
        RPWM.duty(0)
        LPWM.duty(SPEED)
        R_EN.value(1)
        L_EN.value(1)
    sleep(MOVE_TIME)
    RPWM.duty(0)  # stop
    LPWM.duty(0)
    R_EN.value(0)
    L_EN.value(0)


# ---- Main loop ----
while True:
    left = left_ldr.read()
    right = right_ldr.read()
    print("Left:", left, "Right:", right)  # remove later if you like

    if right - left > DEADBAND:
        run(1)  # turn right
    elif left - right > DEADBAND:
        run(-1)  # turn left

    sleep(DELAY)
