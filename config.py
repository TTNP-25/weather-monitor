import logging
import os

THINGSPEAK_APIWRITE=os.environ['THINGSPEAK_API_WRITE']
logging.warning("Starting with API KEY %s" % THINGSPEAK_APIWRITE)
