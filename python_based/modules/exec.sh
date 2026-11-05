python3 -c "
import datetime, subprocess
now = datetime.datetime.now()
dt = (now.year, now.month, now.day, now.weekday(), now.hour, now.minute, now.second, 0)
subprocess.run(['mpremote', 'exec', f'import machine; machine.RTC().datetime({dt})'])
" && mpremote mount . exec "import temperature"
