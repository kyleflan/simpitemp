#!/usr/bin/env python3
import adafruit_dht
import board
import time
import os
from TimeLimitedRedisDict import TimeLimitedRedisDict

dht = adafruit_dht.DHT22(board.D4)

tlrd_temp = TimeLimitedRedisDict(redis_key='temperature')
tlrd_hum = TimeLimitedRedisDict(redis_key='humidity')

while True:
    try:
        temp = dht.temperature
        if not temp:  # this means we could not get an input and most likely, the libgpiod_pulsein utility is defunct
            os.system('pkill -f libgpiod_pulsein')  # we're renegades
        temp = temp * 9 / 5.0 +32  # deg C to F
        hum = dht.humidity
        tlrd_temp.insert(temp)
        tlrd_hum.insert(hum)
        #print("Temp: {:.1f} F Humidity {} %".format(temp, hum))
    except RuntimeError: # happens prety frequently, so ignore bad readings
        pass

    time.sleep(30)
    
