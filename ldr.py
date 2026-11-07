from machine import Pin, ADC
from stamp import get_stamp
from turn_motor import turn_anticlockwise, turn_clockwise, stop_motor

# ---- LDRs (each divider: 3.3V -> LDR -> pin -> 10k -> GND) ----
left_ldr = ADC(Pin(32))  # was A0 in the drawing
right_ldr = ADC(Pin(33))  # was A1 in the drawing
print(f"{get_stamp()},LDR,STATUS,Connections are set ")

left_ldr.atten(ADC.ATTN_11DB)  # read the full 0-3.3 V range
right_ldr.atten(ADC.ATTN_11DB)

# ---- Settings ----
BASE_DEADBAND_PERCENT = 0.30
MIN_DEADBAND = 100
MIN_LIGHT_THRESHOLD = 1000


# ---- Main loop ----
def check_ldr():
    left = left_ldr.read()
    right = right_ldr.read()

    if left == 0 and right != 0:
        print(f"{get_stamp()},LDR,ERROR,Left LDR Connection Issue")
        return None
    if left != 0 and right == 0:
        print(f"{get_stamp()},LDR,ERROR,Right LDR Connection Issue")
        return None

    # Check maximum intensity to see if there is enough ambient light to track
    max_light = max(left, right)

    if max_light < MIN_LIGHT_THRESHOLD:
        stop_motor()
        print(
            f"{get_stamp()}, LDR, STATUS, Low Light ({max_light} < {MIN_LIGHT_THRESHOLD}); Stay"
        )
        return True

    # Calculate average light level to gauge current brightness
    avg_light = (left + right) / 2

    # Scale deadband dynamically based on ambient light
    scaled_deadband = max(MIN_DEADBAND, avg_light * BASE_DEADBAND_PERCENT)

    error = abs(right - left)
    print(
        f"{get_stamp()},LDR,STATUS,Left: {left}; Right: {right}; Deadband: {scaled_deadband:.1f}"
    )

    if error > scaled_deadband:
        if right > left:
            print(f"{get_stamp()},LDR,STATUS,Clockwise")
            turn_clockwise()
        else:
            print(f"{get_stamp()},LDR,STATUS,Anti-clockwise")
            turn_anticlockwise()
    else:
        print(f"{get_stamp()},LDR,STATUS,Stay")
        stop_motor()

    return True
