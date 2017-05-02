
import numpy as np
import time

filename = raw_input("Enter filename: ")
opener = filename + ".txt"
temp = open(opener,'r').read().split('\n')

del temp[0]

frame =[]
heatmap = []
for line in temp:
    if len(line) <= 15:
            del line
    else:
        frame = map(float, line.split())

        if (len(frame) == 64):
            heatmap.append(frame)
