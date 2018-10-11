#Humidity and Temp Sensor
import Adafruit_DHT
sensor = Adafruit_DHT.AM2302
pin = 18 #12 on Board
def read():
    humid, temp = Adafruit_DHT.read_retry(sensor,pin)
    F_temp = temp*(9.0/5.0) + 32.0
    return humid,F_temp
#temp1,temp2 = read()
#print(str(temp1) + ' ' + str(temp2))

