from time import sleep
from datetime import datetime, time
import subprocess

run_time = [time(hour=10, minute=20), time(hour=10, minute=30)]

while True:
    curr = datetime.now().time()
    
    if curr > run_time[0] and curr < run_time[1]:
        subprocess.run(["python", "main.py"])
    
    # check every 10 minutes
    sleep(600)

    