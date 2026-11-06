from machine import Pin, ADC
# from turn_motor import turn_anticlockwise, turn_clockwise

# ---- Settings ----
BASE_DEADBAND_PERCENT = 0.30
MIN_DEADBAND = 100
# DEADBAND = 100  # how big a left/right difference must be before moving
MOVE_TIME = 0.2  # seconds the motor runs per correction

# ---- LDRs (each divider: 3.3V -> LDR -> pin -> 10k -> GND) ----
left_ldr = ADC(Pin(32))  # was A0 in the drawing
right_ldr = ADC(Pin(33))  # was A1 in the drawing
left_ldr.atten(ADC.ATTN_11DB)  # read the full 0-3.3 V range
right_ldr.atten(ADC.ATTN_11DB)
print("[LDR] Connections are set")


# ---- Main loop ----
def check_ldr():
    left = left_ldr.read()
    right = right_ldr.read()

    if left == 0:
        print("[LDR] [ERROR] Left LDR Connection Issue")
        return None
    if right == 0:
        print("[LDR] [ERROR] Right LDR Connection Issue")
        return None

    # Calculate average light level to gauge current brightness
    avg_light = (left + right) / 2

    # Scale deadband dynamically based on ambient light
    scaled_deadband = max(MIN_DEADBAND, avg_light * BASE_DEADBAND_PERCENT)

    error = abs(right - left)
    print(f"[LDR] Left: {left}, Right: {right}, Deadband: {scaled_deadband:.1f}")

    if error > scaled_deadband:
        if right > left:
            # turn_clockwise()
            print("[LDR] Clockwise")
        else:
            # turn_anticlockwise()
            print("[LDR] Anti-clockwise")
    else:
        print("[LDR] Stay")

    return True
