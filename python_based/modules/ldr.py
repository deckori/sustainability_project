from machine import Pin, ADC
from time import sleep
from turn_motor import turn_anticlockwise, turn_clockwise

# ---- Settings ----
BASE_DEADBAND_PERCENT = 0.05
MIN_DEADBAND = 100
# DEADBAND = 100  # how big a left/right difference must be before moving
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
    # Calculate average light level to gauge current brightness
    avg_light = (left + right) / 2

    # Scale deadband dynamically based on ambient light
    scaled_deadband = max(MIN_DEADBAND, avg_light * BASE_DEADBAND_PERCENT)

    error = abs(right - left)
    print(f"Left: {left}, Right: {right}, Deadband: {scaled_deadband:.1f}")

    if error > scaled_deadband:
        if right > left:
            turn_clockwise()
            print("Clockwise")
        else:
            turn_anticlockwise()
            print("Anti-clockwise")
    else:
        print("Stay")

    sleep(DELAY)
