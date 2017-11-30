#!/usr/bin/python2.7

# Title:  ThingSpeak / RaspberryPi Weather station
# Author: AndyPi

# Hardware
# DHT22 (temp / humidity)
# BMP085 (temp/atmospheric pressure)
# (air quality)

# Todo:
# add other sensors
# rpi sd card hardeneing

# import libraries
import sys, httplib, urllib, time, bmp, DHT22, pigpio, atexit
from config import *
from air_quality import sensor as airqsense

# Setup RPi GPIO pins
PIN_DHT22=8
PIN_AIRQ=7

pi = pigpio.pi() # Connect to Pi.
bmp_sensor = bmp.BMP()

# update thingspeak routine (max once every 15 seconds)
def update_thingspeak(data1, data2, data3, data4):
        params = urllib.urlencode({"field1": data1, "field2": data2, "field3": data3, "field4": data4,'api_key':THINGSPEAK_APIWRITE})
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")                
        try:
                conn.request("POST", "/update", params, headers)
                #response = conn.getresponse()
                #print response.status, response.reason
                #data = response.read()
                conn.close()
        except:
                pass
                # error handler if needed


# main loop
if __name__ == "__main__":

     s = airqsense(pi, PIN_AIRQ) # set the GPIO pin number
     while True:
     
  
        # Use 30s for a properly calibrated reading.
        time.sleep(30) 
        
        # get the gpio, ratio and concentration in particles / 0.01 ft3
        g, r, c = s.read()
  
        if (c==1114000.62):
            print("Error\n")
            continue
  
        # convert to SI units
        concentration_ugm3=s.pcs_to_ugm3(c)
        
        # convert SI units to US AQI
        # input should be 24 hour average of ugm3, not instantaneous reading
        aqi=s.ugm3_to_aqi(concentration_ugm3)
        
        bmp_readings = bmp_sensor.get_data()
        print(bmp_readings)

        update_thingspeak(bmp_readings['cTemp'],
                          bmp_readings['pressure'],
                          aqi,
                          bmp_readings['humidity'])
