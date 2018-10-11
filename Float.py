import RPi.GPIO as GPIO
import OUT
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.IN,pull_up_down = GPIO.PUD_UP) # top float sensor of small basin IO pin
GPIO.setup(35,GPIO.IN,pull_up_down = GPIO.PUD_UP) # bottom float sensor of small basin IO pin
def pumpOff():
	GPIO.wait_for_edge(40,GPIO.RISING)
	OUT.OFF(3)
#GPIO.add_event_detect(40, GPIO.RISING, callback = pumpOff)
def check_small(): #checks if small bucket is empty and returns a boolean
	if (GPIO.input(35) == 0):
		return True
	else:
		return False