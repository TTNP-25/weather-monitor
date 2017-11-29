import logging

import time
import random

import thingspeak
import config

ts = thingspeak.Channel(374732,"%s" % config.THINGSPEAK_APIWRITE)

def random_values():
    field_data = {}
    field_data['api_key'] = config.THINGSPEAK_APIWRITE
    field_data['channel_id'] = 374732
    field_data['field1'] = random.randrange(-4,15)
    field_data['field2'] = random.randrange(5,25)
    field_data['field3'] = random.randrange(1,5)
    field_data['field4'] = random.randrange(25,50)
    return field_data

while True:
    print(random_values())
    ts.update(random_values())
    print(ts.get())
    time.sleep(15)
