
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import time
import scipy.misc
import matplotlib.animation as animation
import numpy as np
from pylab import *

def parse(temp):

    frame =[]
    heatmap = []
    for line in temp:
        if len(line) <= 15:
            del line
        else:
            frame = map(float, line.split())

        if (len(frame) == 64):
            heatmap.append(frame)

    return heatmap



filename = raw_input("Enter filename: ")
opener = filename + ".txt"
temp = open(opener,'r').read().split('\n')

heat_map = parse(temp)

#Data for the histogram
all_data = []
for i in range(len(heat_map)):
    all_data += heat_map[i]

dpi = 400
temps = heat_map
print "Length of heatmap: ", len(heat_map)

print "Creating Average temperature/frame plot"

plt.clf()
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
avg_temp = []
for l in temps:
    s = 0
    for n in l:
        s+=n
    avg_temp.append(s/64.0)
t = np.arange(1,len(temps)+1,1)
print(len(avg_temp))
plt.plot(t, avg_temp, 'k', t, avg_temp, 'bo', markersize=10)
plt.title("Average temperature per frame")
saver1 = filename + "_mean" + ".jpg"
plt.savefig(saver1)

print "Creating Variance temperature/frame plot"

plt.clf()
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
variances= []
for l in temps:
    frame = np.array(l)
    variances.append(np.var(frame))

t = np.arange(1,len(temps)+1,1)
print(len(variances))
plt.plot(t, variances, 'k', t, variances, 'bo', markersize=10)
plt.title("Variance per frame")
saver1 = filename + "_var" + ".jpg"
plt.savefig(saver1)
