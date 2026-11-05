from machine import Pin, PWM, ADC
from time import sleep, ticks_ms


def turn(sleep_time, f):
    # Initialize motor driver pins
    RPWM = Pin(25, Pin.OUT)
    LPWM = Pin(26, Pin.OUT)
    EN = Pin(27, Pin.OUT)

    def motor_turn(state, enable=1):
        # Direction is set by the two constant-voltage pins
        RPWM.value(state)
        LPWM.value(1 - state)
        EN.value(enable)

    def stop_motor():
        # Cuts all power and disables the motor driver
        motor_turn(state=0, enable=0)

    # Initial system stop and startup delay
    stop_motor()
    sleep(1)

    start_time = ticks_ms()

    while True:
        print("CLOCKWISE")

        t_clock = ticks_ms() - start_time
        print(f"{t_clock}\tCLOCKWISE")
        f.write(f"{t_clock}\tCLOCKWISE\n")
        f.flush()

        motor_turn(state=1)
        sleep(sleep_time)

        print("STOP")

        t_stop1 = ticks_ms() - start_time
        print(f"{t_stop1}\tSTOP")
        f.write(f"{t_stop1}\tSTOP\n")
        f.flush()

        stop_motor()
        sleep(sleep_time - 5)

        print("ANTICLOCKWISE")

        t_anticlock = ticks_ms() - start_time
        print(f"{t_anticlock}\tANTICLOCKWISE")
        f.write(f"{t_anticlock}\tANTICLOCKWISE\n")
        f.flush()

        motor_turn(state=0)
        sleep(sleep_time)

        print("STOP")

        t_stop2 = ticks_ms() - start_time
        print(f"{t_stop2}\tSTOP")
        f.write(f"{t_stop2}\tSTOP\n")
        f.flush()

        stop_motor()
        sleep(sleep_time - 5)

        # print("REPEATING LOOP")
        global motor_running
        motor_running = False
        break

        return motor_running


# Open a log file in write mode and pass it to the function
with open("motor_log.txt", "w") as log_file:
    turn(15, log_file)
