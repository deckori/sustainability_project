import sys
import machine, onewire, ds18x20, time


def temperature(log_file):
    ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(4)))
    try:
        rom = ds.scan()[0]
    except:
        print("Temperature sensor: ERROR")
        sys.exit()

    start = time.ticks_ms()
    last = time.ticks_ms()
    while True:
        if time.ticks_diff(time.ticks_ms(), last) >= 2000:
            last = time.ticks_ms()
            ds.convert_temp()
            time.sleep_ms(750)
            secs = time.ticks_diff(time.ticks_ms(), start) // 1000
            stamp = "%02d:%02d:%02d" % (
                secs // 3600,
                (secs % 3600) // 60,
                secs % 60,
            )  # NEW
            print(stamp, "-", ds.read_temp(rom))
            log_file.write(f"{stamp} - {ds.read_temp(rom)}\n")
            # log_file.write(stamp, "-", ds.read_temp(rom))


with open("temp_log.txt", "w") as log_file:
    temperature(log_file)
