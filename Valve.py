import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(21,GPIO.OUT) #top valve
GPIO.setup(22,GPIO.OUT) #bottom valve
GPIO.output(21,False)
GPIO.output(22,False)
def nute():
	GPIO.output(21,True) #open top
	time.sleep(10) #wait 10
	GPIO.output(21,False) #close top
	time.sleep(3) #wait 3
	GPIO.output(22,True) #open bottom
	time.sleep(30) #wait 30?
	GPIO.output(22,False) #close bottom
