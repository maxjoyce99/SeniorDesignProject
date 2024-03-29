import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
# SPI port on the ADC to the Cobbler
clockpin = 38 #CLK
misopin = 36 #Dout
mosipin = 32 #DIN
cspin = 37 #CS

# set up the SPI interface pins
GPIO.setup(mosipin, GPIO.OUT)
GPIO.setup(misopin, GPIO.IN)
GPIO.setup(clockpin, GPIO.OUT)
GPIO.setup(cspin, GPIO.OUT)
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
# change these as desired - they're the pins connected from the

'''i = 0
#GPIO.setup(35, GPIO.OUT)
#GPIO.output(35, True)
while i<25:
        value = readadc(0) #read adc from port 0
        print(value) #print the read value
        percent = 100.0 - (value / 10.23) #convert to percent
        print(percent) #print percent
        time.sleep(2)
        i+=1
   '''     


