import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.IN,pull_up_down = GPIO.PUD_UP) #float sensor IO pin
GPIO.wait_for_edge(40,GPIO.RISING)
print("it worked")
