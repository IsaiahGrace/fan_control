#! /usr/bin/python3

## Isaiah Grace
# This script will read my fan.log history
# and create an ascii plot of the temperatures

import os

# Define some unicode values, so we can alternativly use ASCII
CHAR1 = "\033[1;34;40m"

# Get the size of the terminal from the OS
rows, cols = os.popen('stty size', 'r').read().split()

# we subtract 1 from rows because the prompt will take the last row on the screen
rows = int(rows) - 1
cols = int(cols)

# Create the 2D array that will serve as our working structure for the graph
graph = [[" " for i in range(cols)] for j in range(rows)] 

# Determine the fan cutoff temperature
with open("fan_control.sh", "r") as f:
    lines = f.readlines()

upperCutoff = False
lowerCutoff = False

for line in lines:
    if line[0:3] == "MAX":
        upperCutoff = int(line[4:6])
    if line[0:3] == "MIN":
        lowerCutoff = int(line[4:6])

if not upperCutoff or not lowerCutoff:
    print("ERROR: could not find MAX and MIN in fan_control.sh")
    exit
    
# Read the lines from the log file
with open("fan.log", "r") as f:
    lines = f.readlines()

temps = []

for line in lines:
    splits = line.split(" ")
    if splits[3] == "Info:" and splits[5][0:2] != 'up':
        temps.append([splits[0],splits[1],int(splits[5][0:2])])

# Determine the offset
minTemp = 666 # Hell's temp
for temp in temps:
    if temp[2] < minTemp:
        minTemp = temp[2]

xOffset = minTemp - 3

# Determine the veritcal scale, 1:1 or 1:2 vertically,
scale = 1
if rows < (upperCutoff - xOffset):
    scale = 2

# write the Y axis label on the left side of the screen
# and create a dashed line at the cutoff temp
yLabel = (rows * scale) + xOffset
for row in graph:
    row[0] = "\033[1;34;40m" + str(int(yLabel / 10) % 10)
    row[1] = "\033[1;34;40m" + str(yLabel % 10)

    if yLabel == upperCutoff or (yLabel == upperCutoff+1 and scale == 2):
        for i in range(cols - 2):
            row[2 + i] = "\033[1;33;40m\u2594"
    if yLabel == lowerCutoff or (yLabel == lowerCutoff+1 and scale == 2):
        for i in range(cols - 2):
            row[2 + i] = "\033[1;33;40m\u2581"
            
    yLabel = yLabel - scale

# Plot the data points onto the graph
xPos = cols - 1
prevTemp = False
discontinuity = 0
while(xPos > 1):
    try:
        temp = temps[xPos - cols + discontinuity]
    except IndexError as e:
        # This means we've reached the end of our temp history
        break
        
    if prevTemp and (int(prevTemp[1][3:5]) != int(temp[1][3:5]) + 1) and (int(prevTemp[1][3:5]) != 00 and int(temp[1][3:5]) != 59):
        for i in range(len(graph)):
            graph[i][xPos] = "\033[1;34;40m" + "\u2502"
        xPos = xPos - 1
        discontinuity = discontinuity + 1
    
    for i in range(len(graph)):
        if (rows - i) * scale + xOffset <= temp[2]:
            if (rows - i) * scale + xOffset > upperCutoff:
                color = "\033[1;31;40m"
            elif (rows - i) * scale + xOffset >= lowerCutoff:
                color = "\033[1;33;40m"
            else:
                color = "\033[1;32;40m"
            graph[i][xPos] = color + "\u2588"
            
    prevTemp = temp
    xPos = xPos - 1


# Add time delineations on the last row
for i in range(cols-2,0,-10):
    label = str(cols - i - 2)
    graph[-2][i+1] = "\033[1;34;40m" + "|"
    for j in range(1,len(label) + 1):
        graph[-1][i+j] = "\033[1;34;40m" + label[j-1]
    

# Print out our graph
for row in graph:
    line = ""
    for char in row:
        line = line + char
    print(line)
