import OUT
import time
import Float
import Valve
import ADC
time.sleep(2)
f = open("/var/www/html/hygrometer_readings.txt","w") #create file to write to change!!!
temp = ADC.readadc(0) #read hygrometer value
percent = 100.0 - (temp / 10.23)
#print(str(percent))
f.write("First reading: " + str(percent) + '\n') #write first to file
#f.write("First reading: 43.3456542345" + "\n")
f.close()
OUT.ON(6) #turn on the lights
time.sleep(3) #wait 3 seconds
OUT.ON(3) #start filling bucket
time.sleep(10)#wait 10 seconds
Float.pumpOff() #waits for switch to turn off pump
time.sleep(3) #wait 3 seconds
Valve.nute() #dispenses nutrients
OUT.ON(5) #turn on air pump
time.sleep(2)
OUT.ON(4) #turn on hyrdroponic pump
time.sleep(30)
OUT.OFF(4) #turn off hydroponic pump
#OUT.ON(2)
time.sleep(10)
OUT.OFF(6) #turn off the lights
time.sleep(1)
OUT.OFF(5) #turn off air pump'''

#time.sleep(20)
f = open("/var/www/html/hygrometer_readings.txt","w")
#f.write("First reading: 43.3456542345" + "\n")
f.write("First reading: " + str(percent) + '\n') #write first to file
temp = ADC.readadc(0) #read hygrometer value
percent = 100.0 - (temp / 10.23)
f.write("Second reading: " + str(percent) + '\n')
#f.write("Second Reading 69.3456542345" + "\n")
f.close()
