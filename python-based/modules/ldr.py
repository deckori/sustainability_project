from machine import Pin, ADC
from time import sleep
from turn_motor import turn_anticlockwise, turn_clockwise

# ---- Settings ----
DEADBAND = 300  # how big a left/right difference must be before moving
MOVE_TIME = 0.2  # seconds the motor runs per correction
DELAY = 1  # seconds between checks

# ---- LDRs (each divider: 3.3V -> LDR -> pin -> 10k -> GND) ----
left_ldr = ADC(Pin(32))  # was A0 in the drawing
right_ldr = ADC(Pin(33))  # was A1 in the drawing
left_ldr.atten(ADC.ATTN_11DB)  # read the full 0-3.3 V range
right_ldr.atten(ADC.ATTN_11DB)


# ---- Main loop ----
while True:
    left = left_ldr.read()
    right = right_ldr.read()
    print("Anticlock:", left, "Clock:", right)  # remove later if you like

    if right - left > DEADBAND:
        turn_clockwise()  # turn right
    elif left - right > DEADBAND:
        turn_anticlockwise()  # turn left

    sleep(DELAY)
