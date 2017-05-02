
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
        if len(line) < 17:
            del line
        else:
            frame = map(float, line.split())

        if (len(frame) == 64):
            heatmap.append(frame)

    return heatmap

def min_max(temps):
    mn = 10000
    mx = 0
    for l in temps:
        m = min(l)
        if (m<mn):
            mn = m
        m = max(l)
        if (m>mx):
            mx = m
    return mn,mx

def dto2d (l):
    if len(l) == 64:
        y = 4
        x = 16
    else:
        y = 8
        x = 32
    res = []
    for i in range(y):
        res.append(l[x*i:(i+1)*x])
    return res

def get_temp(pure, mn, mx, scale = "None"):
    temp = dto2d(pure)
    y = len(temp)
    x = len(temp[0])

    for i in range(y):
        for j in range(x):
            if temp[i][j] < mn:
                temp[i][j] = 0
            elif temp[i][j]>mx:
                temp[i][j] = 1
            else:
                temp[i][j] = round((temp[i][j]-mn)/(mx-mn),3)

    for i in range(y):
        for j in range(x):
            el = temp[i][j]
            if (el<0.33):
                r = el*3
                g = 0
                b = 0
            elif(el<0.66):
                r = 1
                g = (el-0.33)*3
                b = 0
            else:
                r = 1
                g = 1
                b = (el-0.66)*3
            if (scale == "None"):
                temp[i][j] = [r,g,b]
            else:
                g = temp[i][j]
                temp[i][j] = [g,g,g]
    return temp


###################### Start ###############################################
filename = raw_input("Enter filename: ")
opener = filename + ".txt"
temp = open(opener,'r').read().split('\n')
heat_map = parse(temp)

dpi = 400
temps = heat_map
mn,mx = min_max(heat_map)
print(mn, mx)
print "Length of heatmap: ", len(heat_map)

#----------VIDEO--------------------
saver = filename + "_video" + ".mp4"
i = 0

def ani_frame():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    im = ax.imshow(get_temp(heat_map[0],mn+4,mx+1))

    def update_img(n):
        global i
        i = i+1
        if (i%50==0):
            print(i)
        im.set_data(get_temp(heat_map[i],mn+4,mx+1))
        return im

    ani = animation.FuncAnimation(fig,update_img,len(temps)-2,interval=30)
    #mappable = plt.cm.ScalarMappable(cmap='gray')
    #mappable.set_array([mn+4,mx+1])
    #cbar = fig.colorbar(mappable, shrink=0.5, spacing='proportional')
    #cbar.ax.tick_params(labelsize=10)
    writer = animation.writers['ffmpeg'](fps=12)
    ani.save(saver,writer=writer,dpi=dpi)
    return ani


ani_frame()
