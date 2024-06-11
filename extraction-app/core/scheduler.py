import schedule
import time
import sys
from core.jobs import fetch_and_save_data

def run_scheduler():
    # Programa la tarea para que se ejecute cada minuto
    schedule.every(10).seconds.do(fetch_and_save_data)

    print("Starting the scheduler")
    sys.stdout.flush()

    print("Entering the main loop")
    sys.stdout.flush()
    while True:
        schedule.run_pending()
        time.sleep(1)
