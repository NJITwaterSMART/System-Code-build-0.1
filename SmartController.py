import requests
from nanpy import ArduinoApi
from nanpy import SerialManager
import time
from time import sleep


'''arduino = {
'digital' : tuple(x for x in range(14)),
'analog' : tuple(x for x in range(6)),
'pwm' : (3, 5, 6, 9, 10, 11),
'use_ports' : True,
'disabled' : (0, 1) # Rx, Tx, Crystal
}'''

connection = SerialManager(device='/dev/ttyACM0')
a = ArduinoApi(connection=connection)
a.pinMode(8, a.OUTPUT)

while True:

    #Call weather api and pull needed info
    r = requests.get("http://api.wunderground.com/api/b78b58a1991d6ae8/geolookup/conditions/forecast/hourly/q/NJ/Newark.json")
    data = r.json()
    #current precip
    rain = data['current_observation']['precip_today_in']
    #precip in an hour
    rain1hr = data['current_observation']['precip_1hr_in']
    #relative humidity
    humidity = data['current_observation']['relative_humidity']
    rain = float(rain)
    rain1hr = float(rain1hr)
    humidity = float(humidity.strip('%'))

    #read the soil readings for both sensors
    output_value1 = a.analogRead(3)
    output_value = a.analogRead(0)

    i = 0
    #variables to store sensor readings
    mositureValue1 = 0
    moistureValue = 0

    #variables for sums of sampled values
    moistureSum1 = 0
    moistureSum = 0

    #take an average of 10 samples
    for i in range(10):
        moistureSum1 = moistureSum1 + output_value1  # adds value of moisture
        # by value of analog  pin 3
        moistureSum = moistureSum + output_value  # adds value of moisture sum by value of analog pin 0

    sleep(0.005)
    moistureValue1 = moistureSum1 / 10  # averages value at analog pin 3
    moistureValue = moistureSum / 10  # averages value at analog pin 0

    #wet threshold value of sensor at analog pin 3
    dryValue1 = 400
    #dry threshold of air
    wetValue1 = 1023

    #check precipitation and soil moisture to determine if the system should be started
    list = [rain,rain1hr,humidity,moistureValue,moistureValue1]
    max = [0.09,0.09,40,600,600]
    min = [0.00,0.00,20,950,950]

    for j in range(5):
        if list[j] <= max[j] and list[j] >= min[j]:

            a.digitalWrite(8, a.HIGH)
            sleep(.5)
            a.digitalWrite(8, a.LOW)
            sleep(.5)
            a.digitalWrite(8, a.HIGH)
            sleep(.5)
            a.digitalWrite(8, a.LOW)
            sleep(.5)
            a.digitalWrite(8, a.HIGH)
            sleep(.5)
            a.digitalWrite(8, a.LOW)

        '''else: 
            
            print "Too Humid"
            break'''

    time.sleep(120)



