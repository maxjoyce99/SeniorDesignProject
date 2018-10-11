import schedule
import time
#global a
a = 4
b = 3
def add():
	#global a
	#a = a + b
	#b = 0
	call()
def call():
	print("test")
schedule.every(1).seconds.do(add).tag("add")
i = 0
while i<5:
	schedule.run_pending()
	time.sleep(1)
	i += 1
#print(a)