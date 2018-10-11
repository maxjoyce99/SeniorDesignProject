import schedule
import time
print("FUCK")
def job():
    print("Hola")
schedule.every(5).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
