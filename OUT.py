import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)# sets up GPIO pins as outputs
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT) # these can be changed
GPIO.setup(8,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.output(3,True)
GPIO.output(5,True)
GPIO.output(7,True)
GPIO.output(8,True)
GPIO.output(10,True)
bools = [False,False,False,False,False] #weather outlets are on or off
outlet_convert = {2:3,3:5,4:7,5:8,6:10} #convert between outlet # and IO pin
def toggle(a): #a=input number written on outlet cover. Turns on if off and vice versa
    temp = outlet_convert[a]
    if bools[a-2] == False:
        GPIO.output(temp,False)
        bools[a-2] = True
        print("ON")#test
    else:
        GPIO.output(temp,True)
        bools[a-2] = False
        print("OFF")#test
def OFF(a): #turns off outlet
    temp = outlet_convert[a]
    GPIO.output(temp,True)
    bools[a-2] = False
def ON(a): #turns on outlet
    temp = outlet_convert[a]
    GPIO.output(temp,False)
    bools[a-2] = True
