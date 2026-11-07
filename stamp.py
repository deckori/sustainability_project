import time

# Timezone offset in hours (UTC+3 for Qatar / AST).
# When rshell connects, it synchronizes the RTC to UTC by default.
# Adding TZ_OFFSET ensures your logs always reflect local Qatar time.
# Set to 0 if your RTC is manually set directly to local time.
TZ_OFFSET = 3


def get_stamp():
    t = time.localtime(time.time() + TZ_OFFSET * 3600)
    # time.localtime format: (year, month, mday, hour, minute, second, weekday, yearday)
    return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d}T{t[3]:02d}:{t[4]:02d}:{t[5]:02d}"
