import schedule
import time
import sys
from core.jobs import fetch_and_save_data

def run_scheduler():

    # Wait until kafka is up and running
    time.sleep(10)

    fetch_and_save_data()

    schedule.every().day.at("00:00").do(fetch_and_save_data)

    print("Starting the scheduler")
    sys.stdout.flush()

    print("Entering the main loop")
    sys.stdout.flush()

    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    run_scheduler()
