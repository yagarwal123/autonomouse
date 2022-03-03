# import cv2
# import matplotlib.pyplot as plt
# import numpy as np

# filename = '0007A0F7C4_1/0007A0F7C4_1_experiment_1_recording_1/rpicamera_video.mp4'
# cap = cv2.VideoCapture(filename)

# try:
#     frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
#     width  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
# except AttributeError:
#     frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# fig, ax = plt.subplots(1,1)
# plt.ion()
# plt.show()

# #Setup a dummy path
# x = np.linspace(0,width,frames)
# y = x/2. + 100*np.sin(2.*np.pi*x/1200)

# for i in range(frames):
#     fig.clf()
#     flag, frame = cap.read()

#     plt.imshow(frame)
#     plt.plot(x,y,'k-', lw=2)
#     plt.plot(x[i],y[i],'or')
#     plt.pause(0.01)

#     if cv2.waitKey(1) == 27:
#         break

# open TTL file
# import cv2
# import csv
# import matplotlib.pyplot as plt
# import numpy as np
# fig, (ax1,ax2) = plt.subplots(2,1)
# plt.ion()
# plt.show()
# filename = '0007A0F7C4_1/0007A0F7C4_1_experiment_1_recording_1/rpicamera_video.mp4'
# cap = cv2.VideoCapture(filename)

# #with open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv",'r') as ttl_file:
# #    TTLarray = np.loadtxt(ttl_file, dtype='int')

# ttl_file = open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv",'r')
# lick_file = open("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv",'r')
# file_time = lick_file.readline()
# file_heading = lick_file.readline()
# startTime = int(lick_file.readline())

# #millis = TTLarray[0]
# millis = int(ttl_file.readline())
# ret, frame = cap.read()
# ax1.imshow(frame)
# idx = 0
# t=0
# amps = []
# times = []
# #while millis<TTLarray[-1]:
# while ttl_file:
#     millis += 1
#     times.append(t)
#     #if millis == TTLarray[idx+1]:
#     if millis == int(ttl_file.readline()):
#         #ret, frame = cap.read()
#         ax1.clear()
#         #ax1.imshow(frame)
#         #cv2.imshow('Video',frame)
#         idx += 1 
#     #print(startTime-millis)
#     if millis > startTime:
#         data = lick_file.readline().strip().split(',')
#         if len(data) != 2:  #Something is wrong, probably a TTL entry, does not increase millis
#             continue
#         print(int(data[1]))
#         amps.append(int(data[1]))
#         # clear graph
#         #plot vs t
#         if int(data[0]) == 0:
#             # print traight line in graph
#             pass
#     else:
#         amps.append(0)
#     # plot lick data
#     ax2.clear()
#     ax2.plot(times, amps)
#     plt.pause(0.001)
#     t+=1
#     plt.show()


import cv2
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
import numpy as np
import time

# filename = '0007A0F7C4_1/0007A0F7C4_1_experiment_1_recording_1/rpicamera_video.mp4'
# cap = cv2.VideoCapture(filename)

# with open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv",'r') as ttl_file:
#     TTLarray = np.loadtxt(ttl_file)
    
# lick_file = open("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv",'r')
# file_time = lick_file.readline()
# file_heading = lick_file.readline()
# startTime = int(lick_file.readline())
# lick_file.close()

# testT,amps = np.loadtxt("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv", unpack=True,delimiter=',',skiprows=3)

# millis = int(TTLarray[0])
# idx = 0
# startTests = [i for i,k in enumerate(testT) if k==0] 
# plt_x = np.array([])
# line, = plt.plot([],[])

# #fig, ax = plt.subplots(1,1)
# plt.ion()
# # for k in startTests:
# #     line.axes.axvline(k,color = 'r')



fig, ax1 = plt.subplots()
#plt.ion()
filename = '0007A0F7C4_1/0007A0F7C4_1_experiment_1_recording_1/rpicamera_video.mp4'
cap = cv2.VideoCapture(filename)

with open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv",'r') as ttl_file:
    TTLarray = np.loadtxt(ttl_file)
    
lick_file = open("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv",'r')
file_time = lick_file.readline()
file_heading = lick_file.readline()
startTime = int(lick_file.readline())
lick_file.close()

testT,amps = np.loadtxt("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv", unpack=True,delimiter=',',skiprows=3)

millis = int(TTLarray[0])
idx = 0
#startTests = [i for i,k in enumerate(testT) if k==0] 
plt_x = np.array([])
line, = ax1.plot([],[])
end = TTLarray[-1]
while millis<end:
    if millis == TTLarray[idx]:
        idx += 1
        ret, frame = cap.read()
        cv2.imshow('Video',frame)
        cv2.waitKey(1)
    if millis > startTime:
        t = millis - startTime
        s = t-50 if t>=50 else 0
        plt_x = np.append(plt_x,t)
        plt_x = plt_x[-50:]
        plt_y = amps[s:t]
        #plt_y = amps[0:len(plt_x)]
        #plt.plot(plt_x[-1],plt_y[-1],'ro')
        #plt.plot(plt_x,plt_y,'k-')
        line.set_data(plt_x,plt_y)
        line.axes.relim()
        line.axes.set_xlim(s,t)
        line.axes.autoscale_view()
        line.axes.figure.canvas.update()
        #plt.show()
        #plt.pause(0.0001)
    millis += 1
    print(time.time())
    #plt.pause(0.0001)

# for i in range(100):
#     fig.clf()
#     flag, frame = cap.read()

#     #plt.imshow(frame)
#     cv2.imshow('Video',frame)
#     t = millis - startTime
#     # s = t-5000 if t>=5000 else 0
#     plt_x = np.append(plt_x,i)
#     plt_y = amps[0:len(plt_x)]
#     #plt.plot(testT[i],amps[i],'ro')
#     plt.plot(plt_x,plt_y,'k-')
#     plt.pause(0.01)

#     if cv2.waitKey(1) == 27:
#         break
plt.show()
cap.release()
cv2.destroyAllWindows()