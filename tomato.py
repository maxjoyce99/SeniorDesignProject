#Tomato main Team 3 SDP17
import OUT
import datetime
import schedule
import threading
import time
import Float
import ADC
import Valve
import HT
#import simulate_time
import RPi.GPIO as GPIO
import subprocess

#declare global variable
global timeBetweenWater
global air
global fill_pump
global hygro
global water_pump
global water_time
global light_outlet
global day_count
#read current day from cycle counter file
f_day = open("day.txt","r")
day_count = int(f_day.readline())

f_day.close()

#make a file to record what actually happened



subprocess.call(("sudo date 0330170417"),shell = True)
#get start time and define time for lights and water to be on
startTime = datetime.datetime.now()
timeBetweenWater = 8; #in hours
hoursLightsOn = 16 #starts at 18 needs to change to 12 after unknown amount of time. 8 weeks?
water_time = 30 #may need to change. 30?
hour = startTime.hour
minute = startTime.minute
hour += 1
if hour>23:
	hour = hour - 24

if hour<10:
        hour_str = "0"+str(hour)
else:
        hour_str = str(hour)
if minute+1<10:
	minute_str = "0"+str(minute+1)
else:
	minute_str = str(minute+1)
timeLightsOn = hour_str + ":" + minute_str #set different start time
hour = startTime.hour
minute = startTime.minute
hour += 1
if hour>23:
	hour = hour - 24

if (hour + hoursLightsOn) < 24:
	hour += hoursLightsOn
else:
	hour = hour + hoursLightsOn - 24
if hour<10:
        hour_str = "0"+str(hour)
else:
        hour_str = str(hour)
if minute+1<10:
	minute_str = "0"+str(minute+1)
else:
	minute_str = str(minute+1)
timeLightsOff = hour_str + ":" + minute_str #light off  a set amount laterhours later

#outlet & pin numbers
bigFloat = 33 #pin number
nuteFloat = 11 #pin number
light_outlet = 6 #outlet number
fill_pump = 3
water_pump = 4
air = 5 #air pump outlet number
light_change = 56 #amount of days until lights need to change currently 8 weeks
#f_hygro_live = open("/var/www/html/hygrometer_readings.txt","w")
hygro = [0,1,2,3] #hygro ADC input
#is_water = False #is it currently watering the plants?

def update_day(): #updates the day to keep track
	global day_count
	day_count += 1
	f_day = open("day.txt","w")
	f_day.write(str(day_count))
	f_day.close()
	
def light_on(): #turns light on
	global light_outlet
	OUT.ON(light_outlet)
	
	
def light_off(): #turns light off
	global light_outlet
	OUT.OFF(light_outlet)
	
def water(): #turns on water for specified watering interval then off again
	global water_pump
	global water_time
	OUT.ON(water_pump)
	time.sleep(water_time)
	OUT.OFF(water_pump)
	#time.sleep(10) #waits for water to seep through
	#is_water = False
	
def check_temp_humid(): #checks temp and humidity and writes to live file and history file
	#get temp and humidity with HT.read function
	humidity,temp = HT.read()
	
	#write temp and humidity to live file
	f = open("/var/www/html/humid.txt", "w")
	f.write(str(humidity))
	f.close()
	
	f2 = open("/var/www/html/temp.txt", "w")
	f2.write(str(temp))
	f2.close()
	
	#write to history file
	f2 = open("/var/www/html/tempHumidityHistory.tsv", "r")
	lines = f2.readlines()
	f2.close()

	f2 = open("/var/www/html/tempHumidityHistory.tsv", "w")
	lineNum=0

	for line in lines:
		if (lineNum!=1): #have to make this work only when there is already 7 entriesx
			f2.write(line)
		lineNum += 1

	nowTime= datetime.datetime.now()

	if nowTime.month<10:
		month="0" + str(nowTime.month)
	else:
		month = str(nowTime.month)

	if nowTime.day<10:
		day="0" + str(nowTime.day)
	else:
		day = str(nowTime.day)

	f2.write("\n" + str(nowTime.year) + str(month) + str(day) + "\t" + str(temp) + "\t" + str(humidity))
	f2.close()

	'''#write to permanent history
	f3 = open("./SDPtestingOutputs/tempHumidityDebug.txt", "a")
	f3.write("\n" + str(nowTime.year) + str(month) + str(day) + "\t" + str(temp) + "\t" + str(humidity))
	f3.close()'''

def hygro_live():#writes to live hygrometer reading
	global hygro
	readings = [ 0, 0, 0, 0, 0]
	i = 0
	f = open("/var/www/html/hygrometer_readings.txt", "w")
	while i<len(hygro):
		temp = ADC.readadc(hygro[i])
		percent = 100.0 - (temp/10.23)
		readings[i]=percent
		#write temp and humidity to live file
		f.write(str(percent) + " ")
		i+=1
	f.close()
	nowTime= datetime.datetime.now()

	if nowTime.month<10:
		month="0" + str(nowTime.month)
	else:
		month = str(nowTime.month)

	if nowTime.day<10:
		day="0" + str(nowTime.day)
	else:
		day = str(nowTime.day)
	#write to permanent history
	f3 = open("./SDPtestingOutputs/hygroDebug.txt", "a")
	f3.write("\n" + str(nowTime.year) + str(month) + str(day) + "\t" + str(nowTime.hour) + " " + str(nowTime.minute) + "\t" + str(readings[0]) + "\t" + str(readings[1]) + "\t" + str(readings[2]) + "\t" + str(readings[3]) + "\t" + str(readings[4]))
	f3.close()

def temp_humid_live(): #writes to live temp and humidity reading
	humidity,temp = HT.read()
	
	#write temp and humidity to live file
	f = open("/var/www/html/humid.txt", "w")
	f.write(str(humidity))
	f.close()
	
	f2 = open("/var/www/html/temp.txt", "w")
	f2.write(str(temp))
	f2.close()
	
	nowTime = datetime.datetime.now()

	if nowTime.month<10:
		month="0" + str(nowTime.month)
	else:
		month = str(nowTime.month)

	if nowTime.day<10:
		day="0" + str(nowTime.day)
	else:
		day = str(nowTime.day)


	#write to permanent history
	f3 = open("./SDPtestingOutputs/tempHumidityDebug.txt", "a")
	f3.write("\n" + str(nowTime.year) + str(month) + str(day) + "\t" + str(nowTime.hour) + " " + str(nowTime.minute) + "\t" + str(temp) + "\t" + str(humidity))
	f3.close()


def check_hygro(): #checks hygrometer levels and writes to live file and history file
	global hygro
	readings = [ 0, 0, 0, 0, 0]
	i = 0
	f = open("/var/www/html/hygrometer_readings.txt", "w")
	while i<len(hygro):
		temp = ADC.readadc(hygro[i])
		percent = 100.0 - (temp/10.23)
		readings[i]=percent
		#write temp and humidity to live file
		f.write(str(percent) + " ")
		i+=1
	f.close()
	
	#write to history file
	f2 = open("/var/www/html/hygrometerHistory.tsv", "r")
	lines = f2.readlines()
	f2.close()

	f2 = open("/var/www/html/hygrometerHistory.tsv", "w")
	lineNum=0

	for line in lines:
		if lineNum!=1:
			f2.write(line)
		lineNum += 1

	nowTime= datetime.datetime.now()

	if nowTime.month<10:
		month="0" + str(nowTime.month)
	else:
                month = str(nowTime.month)

	if nowTime.day<10:
		day="0" + str(nowTime.day)
	else:
                day = str(nowTime.day)
	
	readings[4] = (readings[0] + readings[1] + readings[2] + readings[3]) / 4.0	
	f2.write("\n" + str(nowTime.year) + str(month) + str(day) + "\t" + str(readings[0]) + "\t" + str(readings[1]) + "\t" + str(readings[2]) + "\t" + str(readings[3]) + "\t" + str(readings[4]))
	f2.close()

	'''#write to permanent history
	f3 = open("./SDPtestingOutputs/hygroDebug.txt", "a")
	f3.write("\n" + str(nowTime.year) + str(month) + str(day) + "\t" + str(readings[0]) + "\t" + str(readings[1]) + "\t" + str(readings[2]) + "\t" + str(readings[3]) + "\t" + str(readings[4]))
	f3.close()'''	
	
#def check_ph_file(): #just send to live file
#def adjust_ph(): #checks the ph and adds acid or base accordingly
def record_ph(): #measures ph and records to file
        time = datetime.datetime.now()
        Offset = 1.03
        temp = ADC.readadc(4)
        volt = temp*5.0/1024.0
	ph = (14.0 -(3.5*volt))*(1.536)+Offset
	
	#live reading
	f = open("/var/www/html/pH_readings.txt", "w")
	f.write(str(ph))
	f.close()
	
	f2 = open("./SDPtestingOutputs/pHDebug.txt", "a")
	f2.write(str(time.hour) + "\t" + str(time.minute) + "\t" + str(ph)+"\n")
	f2.close()
	
#code to adjust pH.
def check_ph():
	f_ph = open("./SDPtestingOutputs/pHDebug.txt", "a")
	time = datetime.datetime.now()
        Offset = 1.03
        temp = ADC.readadc(4)
        volt = temp*5.0/1024.0
	ph = (14.0 -(3.5*volt))*(1.536)+Offset
	if(ph>7.0):
                Valve.ph_down()
                f_ph.write(str(time.hour) + "\t" + str(time.minute) + "\t" + "pH down\n")
        elif(ph<5.0):
                Valve.ph_up()
                f_ph.write(str(time.hour) + "\t" + str(time.minute) + "\t" + "pH up\n")
	f_ph.close()
        
        
def notify_big_basin(): #let the user know that the main basin is empty
	f = open("./SDPtestingOutputs/test.txt","w") #needs to change
	f.write("Fill the bucket")
	f.close()

def notify_nute(): #let the user know that the nutrition 
	f = open("./SDPtestingOutputs/test.txt","w") #needs to change
	f.write("Nutrients Empty! Please Refill")
	f.close()

def fill_small_basin(): #run the filling and nutrient dispersal process
	global air
	global fill_pump
	OUT.OFF(air) #turn air pump off
	OUT.ON(fill_pump)
	time.sleep(5)
	Float.pumpOff()
	time.sleep(2)
	Valve.nute()
	OUT.ON(air) #turn air pump on
	
def change_light_cycle(hour,minute): #changes the light cycle to convince the plants to harvest
	schedule.clear("light_off1")
	if (hour + 12) < 24:
		hour += 12
	else:
		hour = hour + 12 - 24
	if hour<10:
        	hour_str = "0"+str(hour)
	else:
        	hour_str = str(hour)
	if minute+1<10:
		minute_str = "0"+str(minute+1)
	else:
		minute_str = str(minute+1)

	time = hour_str + ":" + minute_str
	schedule.every().day.at(time).do(light_off).tag("light_off2")
	return schedule.CancelJob #only runs once
	
def start_check(): #starts the code to check if small basin is empty and ph is out of range
        global timeBetweenWater
	schedule.every(timeBetweenWater).hours.do(smallFloat_check).tag("smallFloat_check")
	#schedule.every(timeBetweenWater).hours.do(check_ph).tag("check_ph")
	return schedule.CancelJob #only runs once
	
def smallFloat_check(): #fills the small basin if its empty
	if (Float.check_small() == True):
		fill_small_basin()
	
def run(): #checks for and runs functions that are scheduled to run  
	while 1:
		schedule.run_pending()
		time.sleep(1)
def start_water():
	global timeBetweenWater
	water()
	schedule.every(timeBetweenWater).hours.do(water).tag("water") #water plants every 8 hours
	return schedule.CancelJob

OUT.ON(air) #initiates air pump

#schedule the methods
#hygrometers twice a day
#temp and humidity once a day
#lights on and off at changing intervals
schedule.every().hour.do(record_ph).tag("record_ph") #checks the ph every hour
schedule.every().hour.do(temp_humid_live).tag("temp_humid_live")
schedule.every().hour.do(hygro_live).tag("hygro_live")


schedule.every().day.at(timeLightsOn).do(light_on).tag("light_on1") #turns lights on
schedule.every().day.at(timeLightsOff).do(light_off).tag("light_off1") #turns lights off


schedule.every().day.at("12:00").do(check_temp_humid).tag("check_temp_humid") #check the temp and humidity every day at 12
schedule.every(12).hours.do(check_hygro).tag("check_hygro") #checks the hygrometers every 12 hours



if day_count > 55: #if the day count is 56 or greater days then change to the new light cycle
	change_light_cycle(startTime.hour,startTime.minute)
else:
	schedule.every(light_change-day_count).days.at(timeLightsOff).do(change_light_cycle,startTime.hour,startTime.minute).tag("change_light_cycle")
	


schedule.every(4).hours.do(start_check).tag("start_check") #starts the small basin check and ph check after 4 hours
schedule.every(1).hours.do(start_water).tag("start_water") #starts the water process to make sure we stay in sync
schedule.every().day.at("00:00").do(update_day).tag("update_day") #saves the current day in life cycle of plants

#starts thread to check pending schedule every second
new_thread = threading.Thread(target=run) #thread to run scheduled functions
new_thread.start() #starts thread

'''#start the time simulation, NEEDS TO BE REMOVED
time_thread = threading.Thread(target=simulate_time.run,args=(startTime.hour,startTime.minute,startTime.day))
time_thread.start() 
'''
#print(schedule.jobs)
#check pH
#set up interupt for io pins mainly for float sensors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(bigFloat,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(nuteFloat,GPIO.IN,pull_up_down = GPIO.PUD_UP)
#need to actually write notifications


#GPIO.add_event_detect(bigFloat, GPIO.RISING, callback = notify_big_basin, bouncetime=300) #may change to falling edge
#GPIO.add_event_detect(nuteFloat, GPIO.RISING, callback = notify_nute, bouncetime=300) #may change to falling edge

 
