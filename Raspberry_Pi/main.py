#Created by Alex Bleda 4/25/2017
# This program initializes and runs the Occusense class.

import OccuSense

sensor = OccuSense.OccuSense(1122, True) #1122 is the sensor id

while True: #while loop keeps running (in case sensor.on is false) would keep checking in case the sensor should be turned on again
    sensor.count_people()
