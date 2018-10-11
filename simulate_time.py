import datetime
import subprocess
import schedule
import threading
import time


def run(current_hour,current_minute):
    time.sleep(30) #wait 30 seconds
    
    #skip forward 18 hours to turn off lights
    hour = current_hour + 18
    minute = current_minute
    if hour>23:
        hour = hour - 24
    if hour<10:
        hour_str = "0"+str(hour)
    else:
        hour_str = str(hour)
    if minute<10:
        min_str = "0"+str(minute)
    else:
        min_str = str(minute)
    subprocess.call(("sudo date 0201" + hour_str + min_str + "17"),shell = True)

    time.sleep(120) #wait 2 minutes
    
    #skip forward 8 hours to water plants
    hour = current_hour + 8
    minute = current_minute
    if hour>23:
        hour = hour - 24
    if hour<10:
        hour_str = "0"+str(hour)
    else:
        hour_str = str(hour)
    if minute<10:
        min_str = "0"+str(minute)
    else:
        min_str = str(minute)
    subprocess.call(("sudo date 0201" + hour_str + min_str + "17"),shell = True)

    time.sleep(120) #wait 2 minutes
    
    #change time to 11pm to check temp and humidity
    subprocess.call("sudo date 0201230017",shell = True)

    time.sleep(10) #wait 10 seconds

    #skip forward 12 hours to check hygrometers
    hour = current_hour + 12
    minute = current_minute
    if hour>23:
        hour = hour - 24
    if hour<10:
        hour_str = "0"+str(hour)
    else:
        hour_str = str(hour)
    if minute<10:
        min_str = "0"+str(minute)
    else:
        min_str = str(minute)
    subprocess.call(("sudo date 0201" + hour_str + min_str + "17"),shell = True)

    time.sleep(120) #wait 2 minutes

    #change time to 12am the next day to update day count
    subprocess.call("sudo date 0202000017",shell = True)

    #small basin check?
    
'''def check():
    i = 0
    while i<65:
        schedule.run_pending()
        time.sleep(1)
        i+=1
'''
#schedule.every().day.at("12:00").do(run).tag("run")
current_time = datetime.datetime.now()
#schedule.every(4).hours.do(run).tag("run")
#print(schedule.jobs)

hour = current_time.hour
minute = current_time.minute
new_thread = threading.Thread(target = run,args=(hour,minute))
new_thread.start()
'''hour += 4
if hour>23:
    hour = hour - 24
if hour<10:
    hour_str = "0"+str(hour)
else:
    hour_str = str(hour)
if min<10:
    min_str = "0"+str(minute)
else:
    min_str = str(minute)
time.sleep(5)
subprocess.call(("sudo date 0201" + hour_str + min_str + "17"),shell = True)'''
