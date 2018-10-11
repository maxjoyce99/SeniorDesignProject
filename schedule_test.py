import schedule
import time
import threading
def job1():
	print("Fuck")
def job2():
	print("You")
def run():
	i = 0
	while i<60:
		schedule.run_pending()
		time.sleep(1)
		i += 1
def job3():
	print("Dank")
def cancel():
	schedule.clear("job1")
	schedule.every(5).seconds.do(job3).tag("job3")
	return schedule.CancelJob #only runs once
schedule.every(5).seconds.do(job1).tag("job1")
schedule.every(15).seconds.do(cancel).tag("cancel")
#time.sleep(6)
#schedule.run_pending()
#run_continuously()
#time.sleep(15)
#schedule.cancel_job(job1)
#schedule.every(5).seconds.do(job2)
new_thread = threading.Thread(target=run)
new_thread.start()
time.sleep(12)
schedule.every(5).seconds.do(job2).tag("job2")
time.sleep(10)
print(str(schedule.jobs))
#a = schedule.jobs
#print(str(a[0]))
#print(len(a))
print(str(schedule.jobs))
print("test")