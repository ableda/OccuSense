# Created by Alex Bleda 4/25/2017
# OccuSense Senior Design Project

#This class is used to simultaneously collect raw data from the sensor in one file
# and save the detection events on another one. They are both synchronized by time stamps
# at every frame. This class is time based (only record for amount of seconds specified)

import numpy as np
import time
import datetime
import PIL
import scipy.misc
import serial
import requests
import json
from firebase import firebase
import motionDetection

class dataCollection:
    def __init__(self, sensorId):
        self.sensorId = sensorId
        self.serial_port = serial.Serial(port='/dev/ttyACM0', baudrate=57600)

        self.run_time = int(raw_input('Enter the amount of seconds you want to run this: '))
        self.start_time = time.time()

    def save_frame(self, frame):
	date_1 = str(time.strftime('%d-%m-%Y'))
	time2 = datetime.datetime.now().strftime("%H:%M:%S.%f")
        filename = date_1 + ".txt"
        fileSave = open(filename, 'a')
	fileSave.write(time2 + "\n")
	for n in frame:
		fileSave.write("%s  " % n)

        fileSave.write("\n\n")

    def save_detection(self, c, frames):
        date_1 = str(time.strftime('%d-%m-%Y'))
        time2 = datetime.datetime.now().strftime("%H:%M:%S.%f")
        filename = date_1 + "-detection.txt"
        fileSave = open(filename, 'a')
        fileSave.write(time2 + "\n")
        fileSave.write(str(c) + " " + str(frames) + "f\n")


    ####Function pushes +1 or -1 if someone walks through#############
    def server_push(self, count):
        firebase_url = 'https://occuserver.firebaseio.com/'

        time_hhmmss = time.strftime('%H:%M:%S')
        date_1 = str(time.strftime('%d-%m-%Y'))

        data = {'time':time_hhmmss,'value':count, 'sensor_id':self.sensorId}
        result = requests.post(firebase_url + '/' + date_1 + '.json', data=json.dumps(data))
        print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text + "\n"

    # MAIN FUNCTION runs algorithm as long as record is active
    def run(self):
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

        while (time.time() - self.start_time) < self.run_time:
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
                    		raw_frame = frame
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

                            self.save_frame(raw_frame)

        			else:
                        		if (isPerson == True) and (len(ppl) > 2):
                                        	motion = motionDetection.motionDetection()
                                		print len(ppl)
            				    	if (len(ppl) < 8):
                                                	numframes = len(ppl)
                                    			c = motion.counting(np.absolute(ppl))

                                		else:
                                                	numframes = 5
                                    			c = motion.counting(np.absolute(ppl[-5:]))

                                		print "Value of c is: ", c
            					if (c != 0):
                                			self.server_push(c)

                                            	self.save_frame(raw_frame)
                                            	self.save_detection(c, numframes)
                                		del ppl[:]
                                		isPerson = False

					else:
                        			self.save_frame(raw_frame)


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
