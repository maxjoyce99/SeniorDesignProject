import RPi.GPIO as GPIO
import schedule
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.OUT)
on = True
def switch(on):
    if on == True:
        GPIO.output(40,False)
        on = False
    else:
        GPIO.output(40,True)
        on = True
schedule.every(5).seconds.do(switch,on) #its not reupdating on. just using same on every time
while True:
    schedule.run_pending()
    time.sleep(1)

