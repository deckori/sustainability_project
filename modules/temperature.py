import sys
import machine, onewire, ds18x20
from time import sleep_ms
from stamp import stamp

ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(4)))
print(f"{get_stamp()}, TEMP, STATUS, Pins set ")


def temperature():
    try:
        roms = ds.scan()
    except:
        print(f"{get_stamp()}, TEMP, ERROR, Sensor malfunction")
        return
    rom = roms[0]

    ds.convert_temp()
    sleep_ms(750)  # Delay for finishing

    print(f"{get_stamp()}, TEMP, ACTION, {ds.read_temp(rom)}")

    return True
