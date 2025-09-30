import schedule
import time
from datetime import datetime
from script import run_stock_job

def basic_job():
    print("Job started at: ",datetime.now())

# basic job to run every minute
schedule.every(3).minutes.do(basic_job)

# stock job to run every minute
schedule.every(3).minutes.do(run_stock_job)

while True:
    schedule.run_pending()
    time.sleep(10)