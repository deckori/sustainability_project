import sys
import machine, onewire, ds18x20, time


def temperature(log_file, interval):
    ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(4)))
    try:
        rom = ds.scan()[0]
    except:
        print("Temperature sensor: ERROR")
        sys.exit()

    start = time.ticks_ms()
    last = time.ticks_ms()

    # 1st line of file
    string = "time, temperature"
    print(string)
    log_file.write(string + "\n")

    while True:
        if time.ticks_diff(time.ticks_ms(), last) >= interval:
            last = time.ticks_ms()

            ds.convert_temp()
            time.sleep_ms(750)

            t = machine.RTC().datetime()
            stamp = "%02d:%02d:%02d" % (t[4], t[5], t[6])

            string = f"{stamp}, {ds.read_temp(rom)}"
            print(string)
            log_file.write(string + "\n")


with open("temp_log.txt", "a") as log_file:
    temperature(log_file, 10000)
