#Created by Alex Bleda 4/25/2017

#This file utlizes the dataCollection class to collect data during a prompted amount of seconds. It is to be used outside the webserver. Should be run straight from the raspberry pi terminal using the command "python collect_data"

import dataCollection

sensor = dataCollection.dataCollection(1122, 0)  #1122 is the sensor id (can be anything) #

sensor.run()
