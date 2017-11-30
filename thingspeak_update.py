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
import sys, httplib, urllib, time, Adafruit_BMP.BMP085, DHT22, pigpio, atexit
BMP085sensor=Adafruit_BMP.BMP085.BMP085(address=0x76)
from config import *
from air_quality import sensor as airqsense

# Setup RPi GPIO pins
PIN_DHT22=8
PIN_BMP085_SDA=2
PIN_BMP085_SCL=3
PIN_TGS2600=0
PIN_AIRQ=7

pi = pigpio.pi() # Connect to Pi.

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

     while True:
     
        s = airqsense(pi, PIN_AIRQ) # set the GPIO pin number
  
        # Use 30s for a properly calibrated reading.
        time.sleep(30) 
        
        # get the gpio, ratio and concentration in particles / 0.01 ft3
        g, r, c = s.read()
  
        if (c==1114000.62):
            print("Error\n")
            continue
  
        print( "Air Quality Measurements for PM2.5:" )
        print( "  " + str(int(c)) + " particles/0.01ft^3" )
  
        # convert to SI units
        concentration_ugm3=s.pcs_to_ugm3(c)
        print( "  " + str(int(concentration_ugm3)) + " ugm^3")
        
        # convert SI units to US AQI
        # input should be 24 hour average of ugm3, not instantaneous reading
        aqi=s.ugm3_to_aqi(concentration_ugm3)
        
        print( "  Current AQI (not 24 hour avg): " + str(int(aqi)))
        print( "" )
  
  
        # Humidity and temp from DHT22 (outisde)
        s = DHT22.sensor(pi, PIN_DHT22, LED=None, power=8)   
        s.trigger()
        time.sleep(0.2)
        humidity=s.humidity()
        temp1=s.temperature()
        
#       si = DHT22.sensor(pi, PIN_DHT22i, LED=None, power=8)   
#       si.trigger()
#       time.sleep(0.2)
#       humidityi=si.humidity()
        
        # temp and pressure from BMP085
        temp2=BMP085sensor.read_temperature()
        pressure = BMP085sensor.read_pressure()

        # calc average temp of 2 sensors
        temperature = 0
        temperature=(temp1+temp2)/2

        update_thingspeak(temperature, humidity, pressure, aqi)
        print( "Temp (DHT22) " + str(temp1))
        print( "Temp (BMP)" + str(temp2))
        print( "Humidity (outide): " + str(humidity))
        print( "Pressure: " + str(pressure))    
        print( "Air Quality: " + str(aqi))    
        
        pi.stop() # Disconnect from Pi.
        time.sleep(5)
