#Created by Alex Bleda 4/25/2017
# Main class for OccuSense occupancy detection system based on the
# MLX90621 thermal sensor.

import numpy as np
import time
import datetime
import PIL
import serial
import requests
import json
from gpiozero import MotionSensor
import threading
from firebase import firebase
import motionDetection
import dataCollection

class OccuSense:
    def __init__(self, sensorId, database):
        #Useful sensor variables
        self.sensorId = sensorId
        self.serial_port = serial.Serial(port='/dev/ttyACM0', baudrate=57600)
        self.record = False
        self.record_time = 0
        self.ipAddress = '192.168.1.4'
        self.on = True
        self.firebase_url = 'https://occuserver.firebaseio.com/'

        if database:
            databaseCheck = threading.Thread(target=self.check_database)
            databaseCheck.start()
            #pirReset = threading.Thread(target=self.pir_reset)
            #pirReset.start()


    ####Function pushes +1 or -1 if someone walks through#############
    def server_push(self, count):

        time_hhmmss = time.strftime('%H:%M:%S')
        date_1 = str(time.strftime('%d-%m-%Y'))

        data = {'time':time_hhmmss,'value':count, 'sensor_id':self.sensorId}
        result = requests.post(self.firebase_url + '/' + date_1 + '.json', data=json.dumps(data))
        print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text + "\n"


    #Function checks database constantly (for possible record command) works in a separate thread
    def check_database(self):
        while True:
            #print "Checking database"
            fire = firebase.FirebaseApplication(self.firebase_url, None)
            result = fire.get('/sensors/' + str(self.sensorId) + '/record', None)
            if result >= 1:
                self.record_time = int(fire.get('/sensors/' + str(self.sensorId) + '/record_time', None))
                self.record = True
                fire.patch('/sensors/' + str(self.sensorId), {'record': 0})

            else:
                self.record = False

            isOn = fire.get('/sensors/' + str(self.sensorId) + '/on', None)
            if isOn == 1:
                self.on = True
            else:
                self.on = False

            time.sleep(0.300)

    #Function to send a reset count if no motion is detected in the room for 2 hours
    def pir_reset(self):
        pir = MotionSensor(4)
        time_to_reset = 60*60*2  #2 hours in seconds
        start_time = time.time()

        while True:
            if (time.time() - start_time) > time_to_reset:
                fire = firebase.FirebaseApplication(self.firebase_url, None)
                fire.patch('/sensors/' + str(self.sensorId), {'reset': 1})

            if pir.motion_detected:
                start_time = time.time()


    def count_people(self):
        #Global Variables
        index = 100
        counter = 0
        last_time = 0
        pcount = 0;
        isPerson = False
        p = 0.1

        #Global Arrays
        frame = []
        temp = []
        ppl = []
        background = [0] * 64
        meanprevious = [0] * 64

        while self.on:
            if (self.record):
                print "Recording data..."
                data = dataCollection.dataCollection(self.sensorId, self.record_time)
                data.run()
                print "Data recorded"

            else:
            	start = False
            	line = self.serial_port.readline()

            	if line == '0\r\n':
            		start = True

            	if index == 0:
                    	try:
                            	frame = map(float, line.split())
                            	index += 1
                    	except:
                            	index = 3

            	if index == 1:
            		if len(frame) == 64:
            			sub = [0] * 64
            			counter += 1

                        		#Threshold based on variance
            			if (np.var(frame) > 1.0):
                            		isPerson = True
            				#Background Subtraction
            				for i in range(len(frame)):
            					sub[i] = int((frame[i] - background[i]))

        					if (abs(sub[i]) == 1):
        						sub[i] = 0

					if (np.amax(sub) > 2):
                        			ppl.append(sub)

            			else:
                            		if (isPerson == True) and (len(ppl) > 2):
                                            	motion = motionDetection.motionDetection()
                                    		print len(ppl)
                				if (len(ppl) < 8):
                                        		c = motion.counting(np.absolute(ppl))

                                    		else:
                                        		c = motion.counting(np.absolute(ppl[-5:]))

                                    		print "Value of c is: ", c
                				if (c != 0):
                                    			self.server_push(c)

                                    		del ppl[:]
                                    		isPerson = False


            				for i in range(len(frame)):
                                    		if (counter < 2):
                                        			meanprevious[i] = frame[i]
                                    		else:
                                        			background[i] = round((p*frame[i] + (1-p)*meanprevious[i]),2)
                                        			meanprevious[i] = background[i]

            		index = 2
            		del frame[:]

            	if start:
            		index = 0
            		start = False
