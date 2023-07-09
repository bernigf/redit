import time
import datetime

from datetime import datetime, timedelta
from time import sleep

name = "redit"
version = "0.1.5"

now = datetime.now()
now_str = str(now.strftime('%H:%M:%S'))

print()
print("Starting python " + name + " at " + now_str)
print()

