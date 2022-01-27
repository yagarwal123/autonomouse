# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 16:56:24 2022

@author: User
"""

import serial
# import time
import csv
import matplotlib
matplotlib.use("tkAgg")
# import matplotlib.pyplot as plt
# import numpy as np

ser = serial.Serial("COM5", 9600)
ser.flushInput()

# plot_window = 20
# y_var = np.array(np.zeros([plot_window]))

# plt.ion()
# fig, ax = plt.subplots()
# ax.axis(ymin=0, ymax=500)
# line, = ax.plot(y_var)
with open("lick_data.csv","a") as f:
    writer = csv.writer(f,delimiter=",")
    writer.writerow(['trial', 'lick time'])

while True:
    # read trial number
    decoded_trial = None
    while decoded_trial is None:
        try:
            ser_bytes = ser.readline()
            try:
                decoded_trial = int(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                print("trial: ", decoded_trial)
            except:
                continue
        except:
            print("Keyboard Interrupt")
            break
    
    # read lickTime
    decoded_lick = None
    while decoded_lick is None:
        try:
            ser_bytes = ser.readline()
            try:
                decoded_lick = int(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                print("lick: ", decoded_lick)
            except:
                continue
        except:
            print("Keyboard Interrupt")
            break
    
    with open("lick_data.csv","a") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow([decoded_trial, decoded_lick])