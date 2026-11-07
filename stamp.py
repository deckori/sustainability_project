import machine


def get_stamp():
    t = machine.RTC().datetime()
    return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d}T{t[4]:02d}:{t[5]:02d}:{t[6]:02d}"
