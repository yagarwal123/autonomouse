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
fig, ax = plt.subplots()
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
while millis<TTLarray[-1]:
    #print(millis)
    if millis == TTLarray[idx]:
        ret, frame = cap.read()
        #cv2.imshow('Frame',frame)
        idx += 1 
    if millis > startTime:
        data = lick_file.readline().strip().split(',')
        if len(data) != 2:
            continue
        ax.clear()
        amps.append(data[1])
        # clear graph
        ax.plot(amps)
        plt.show(block=False)
        if data[0] == 0:
            # print traight line in graph
            pass
    millis += 1
    if millis%10000 == 0:
        print(millis)

print('done')