# Created by Alex Bleda 4/25/2017
# Occusense Senior Design Project

# This class takes in an array of 16x4 (64) frames derived from the occusense class
# and determines the direction the person walked through

import numpy as np
import datetime

class motionDetection:
    def print_frame(self, frame):
        	print frame[:16]
        	print frame[16:32]
        	print frame[32:48]
        	print frame[48:64]

    #Used to save missed detections
    def save_subtraction(self, ppl):
    	sub_file = open("motion_save16.txt", 'a')

    	time1 = datetime.datetime.now().strftime("%H:%M:%S.%f")
    	sub_file.write(time1)
    	sub_file.write("0\n")

    	for frame in ppl:
    		count = 0
    		for n in frame:
    			count += 1
    			sub_file.write("%s  " % n)

    			if ((count) % 16 == 0):
    				sub_file.write("\n")

    		sub_file.write("\n\n")

    ###### Motion detection algorithm based on cross correlation ###########
    def correlation_coefficient(self, patch1, patch2):
        product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
        stds = patch1.std() * patch2.std()
        if stds == 0:
            return 0
        else:
            product /= stds
            return product

    def time_seriesArray(self, heat_map, start, finish, index):
        pix = []
        j = start
        while j < finish+1:
            pix.append(heat_map[j][index])
            j += 1

        pix = np.array(pix)
        return pix


    def create_corrArray(self, heat_map, start, finish):
        corr = []

        maxloc = np.argmax(heat_map[start])
        maxpix = self.time_seriesArray(heat_map, start, finish, maxloc)

        for i in range(len(heat_map[start])):
            #create 64 time series arrays (is it too much memory waste)
            pix = self.time_seriesArray(heat_map, start, finish, i)
            corr.append(round(self.correlation_coefficient(maxpix, pix), 2))

        return corr

    def rowCount_correlations(self, corr1):
        rowcount = []
        ncount = 0
        for i in range(len(corr1)):
            if (corr1[i] < 0.0):
                ncount += 1

            if ((i+1) % 16 == 0):
                rowcount.append(ncount)
                ncount = 0

        return rowcount

    def row_sumCorr(self, corr1):
        rowSum = []
        count = 0
        for i in range(len(corr1)):
            count += corr1[i]

            if ((i+1) % 16 == 0):
                rowSum.append(round(count,2))
                count = 0

        return rowSum

    #This version counts negative numbers
    def count_ppl(self, one):
        count = 0
        reversecount = 0

        for i in range(len(one) - 1):
            if (one[i] < one[i+1]):
                count += 1

            if (one[i] > one[i+1]):
                reversecount += 1

        if (count >= 2 and reversecount < 2):
            print "COUNT: Person walked in +1"
            return 1

        if reversecount >= 2 and count < 2:
            print "COUNT: Person walked out -1"
            return -1

        print "COUNT: Did not catch that"
        return 0

    #this version uses the sum of each row in the correlation matrix
    def count_sum(self, two):
    	inside = 0
    	outside = 0
    	ins = []
    	out = []
    	for i in range(len(two)-1):
    		if(two[i] < two[i+1]):
                	outside += 1
    			out.append(i)
            	if(two[i] > two[i+1]):
                	inside += 1
    			ins.append(i)

        if (inside >= 2 and outside < 2) and (ins[0]+1 == ins[1]):
                print "SUM: Person walked in +1"
            	return 1

        if (outside >= 2 and inside < 2) and (out[0]+1 == out[1]):
            	print "SUM: Person walked out -1"
            	return -1

        print "SUM: Did not catch that"
        return 0

    #main counting function puts it all together
    def counting(self, heat_map):
    	person = 0
    	secondTry = False
    	last = len(heat_map) - 1

    	print "Length of frames: ", len(heat_map)
    	corr1 = self.create_corrArray(heat_map, 0, last)
    	top_rows = sum(heat_map[last][:16]) + sum(heat_map[last][16:32])
    	bottom_rows = sum(heat_map[last][32:48]) + sum(heat_map[last][48:64])
    	print "Last frame: "
        self.print_frame(heat_map[last])
    	print "Sum top rows: ", top_rows, "   Sum bottom rows ", bottom_rows

    	print(datetime.datetime.now().strftime("%H:%M:%S.%f"))
    	one = self.rowCount_correlations(corr1)
        two = self.row_sumCorr(corr1)
    	print "Row Count: ", one, "   Row Sum: ", two

    	person = self.count_sum(two)
    	if (person == 1) and (top_rows < bottom_rows):
    		return 1

    	elif (person == -1) and (top_rows > bottom_rows):
    		return -1

    	else:
    		person = self.count_ppl(one)
    		if (person == 1) and (top_rows < bottom_rows):
    			return 1

    		elif (person == -1) and (top_rows > bottom_rows):
    			return -1

            #If it didnt error check try with less frames
            	if (len(heat_map) > 3):
                	#self.save_subtraction(heat_map)
                	print "Trying again..."
                	self.counting(np.absolute(heat_map[-3:]))

            	#Last resort the last frame decides
            	print "Last frame decides"
            	if (top_rows >= bottom_rows+10):
            		return -1

            	elif (top_rows+10 <= bottom_rows):
                    return 1

    	    	return 0
