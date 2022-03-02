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

# fig, (ax1,ax2) = plt.subplots(2,1)
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

#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         break

# cap.release()
# cap.destroyAllWindows()

#open TTL file
from time import sleep
import cv2
import matplotlib.pyplot as plt
import numpy as np
fig, (ax1,ax2) = plt.subplots(1,2)
plt.ion()
filename = '0007A0F7C4_1/0007A0F7C4_1_experiment_1_recording_1/rpicamera_video.mp4'
cap = cv2.VideoCapture(filename)

with open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv",'r') as ttl_file:
    TTLarray = np.loadtxt(ttl_file)
    
lick_file = open("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv",'r')
file_time = lick_file.readline()
file_heading = lick_file.readline()
startTime = int(lick_file.readline())


millis = TTLarray[0]
idx = 0
amps = []
startTests = []
x_ax = []
while millis<TTLarray[-1]:
    #print(millis)
    if millis == TTLarray[idx]:
        ret, frame = cap.read()
        #ax2.imshow(frame)
        cv2.imshow('Video',frame)
        idx += 1 
    if millis > startTime:
        data = lick_file.readline().strip().split(',')
        if len(data) != 2:  #Something is wrong, probably a TTL entry, does not increase millis
            continue
        ax1.clear()
        amps.append(int(data[1]))
        x_ax.append(millis-startTime)
        amps = amps[-5000:]
        x_ax = x_ax[-5000:]
        # clear graph
        ax1.plot(x_ax,amps)
        ax1.set_ylim(bottom=0)
        if int(data[0]) == 0:
            startTests.append(x_ax[-1])
            # print traight line in graph
        for t in startTests:
            ax1.axvline(x=t,color='r')
        plt.pause(0.001)
    if millis%10000 == 0:
        print(millis)
    millis += 1

plt.show()