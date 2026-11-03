import sys
import machine, onewire, ds18x20, time

ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(4)))
try:
    rom = ds.scan()[0]
except:
    print("Temperature sensor: ERROR")
    sys.exit()

last = time.ticks_ms()
while True:
    if time.ticks_diff(time.ticks_ms(), last) >= 2000:
        last = time.ticks_ms()
        ds.convert_temp()
        time.sleep_ms(750)
        print(ds.read_temp(rom))
