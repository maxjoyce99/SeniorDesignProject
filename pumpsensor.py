import RPi.GPIO as GPIO
import OUT
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN, pull_up_down=GPIO.PUD_UP) #bottom sensor. connected between ground and GPIO3
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_UP) #top sensor. connected between ground and GPIO5
while True:
    if (GPIO.input(3)==0):
        #OUT.ON(4)
        print("pump on")
    if (GPIO.input(5)):
        #OUT.OFF(4)
        print("pump off")
    time.sleep(5)
