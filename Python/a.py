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
import cv2
import csv
import matplotlib.pyplot as plt
import numpy as np
fig, (ax1,ax2) = plt.subplots(2,1)
plt.ion()
plt.show()
t=0
filename = '0007A0F7C4_1/0007A0F7C4_1_experiment_1_recording_1/rpicamera_video.mp4'
cap = cv2.VideoCapture(filename)

with open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv",'r') as ttl_file:
    TTLarray = np.loadtxt(ttl_file)
    
lick_file = open("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv",'r')
file_time = lick_file.readline()
file_heading = lick_file.readline()
startTime = lick_file.readline()


millis = TTLarray[0]
ret, frame = cap.read()
ax1.imshow('Frame',frame)
idx = 0
amps = []
while millis<TTLarray[-1]:
    fig.clf()
    millis += 1
    t+=1
    if millis == TTLarray[idx+1]:
        ret, frame = cap.read()
        ax1.imshow('Frame',frame)
        idx += 1 
    if millis > startTime:
        data = lick_file.readline()
        amps.append(data[1])
        # clear graph
        #plot vs t
        if data[0] == 0:
            # print traight line in graph
            pass
    plt.pause(0.01)