#Created by Alex Bleda 4/25/2017
# This program initializes and runs the Occusense class.

import OccuSense

sensor = OccuSense.OccuSense(1122, False) #1122 is the sensor id

sensor.count_people()
