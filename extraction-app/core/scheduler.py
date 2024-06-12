import schedule
import time
import sys
from core.jobs import fetch_and_save_data

def run_scheduler():
    schedule.every(20).minutes.do(fetch_and_save_data)

    print("Starting the scheduler")
    sys.stdout.flush()

    print("Entering the main loop")
    sys.stdout.flush()
    
    while True:
        schedule.run_pending()
        time.sleep(50)
