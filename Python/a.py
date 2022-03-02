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
fig, ax1 = plt.subplots()
plt.ion()
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
startTests = [i for i,k in enumerate(testT) if k==0] 
line, = ax1.plot([],[])
for k in startTests:
    line.axes.axvline(k,color = 'r')
while millis<TTLarray[-1]:
    #print(millis)
    if millis == TTLarray[idx]:
        ret, frame = cap.read()
        #ax2.imshow(frame)
        cv2.imshow('Video',frame)
        idx += 1 
    if millis > startTime:
        #ax1.clear()
        t = millis - startTime
        s = t-5000 if t>=5000 else 0
        plt_y = amps[s:t+1]
        plt_x = np.arange(s,t+1)
        # clear graph
        line.set_data(plt_x,plt_y)
        line.axes.relim()
        line.axes.set_xlim(s,t)
        
        line.axes.autoscale_view()
        line.axes.figure.canvas.draw()
        #ax1.set_ylim(bottom=0)

        plt.pause(0.001)
    if millis%10000 == 0:
        print(millis)
    millis += 1

plt.show()
cap.release()
cv2.destroyAllWindows()