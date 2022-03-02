import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2
import numpy as np
from itertools import count

filename = '0007A0F7C4_1/0007A0F7C4_1_experiment_1_recording_1/rpicamera_video.mp4'
cap = cv2.VideoCapture(filename)

with open("0007A0F7C4_1/TTL high millis - 0007A0F7C4_1.csv",'r') as ttl_file:
    TTLarray = np.loadtxt(ttl_file)

lick_file = open("0007A0F7C4_1/Raw lick data - 0007A0F7C4_1.csv",'r')
file_time = lick_file.readline()
file_heading = lick_file.readline()
startTime = int(lick_file.readline())

amps = []
idx = [0]
t = count()

def animate(i):
    #print(idx)
    millis = next(t) + TTLarray[0]
    if millis == TTLarray[idx[0]]:
        ret, frame = cap.read()
        cv2.imshow('Frame',frame)
        idx[0] += 1
    if millis > startTime:
        data = lick_file.readline().strip().split(',')
        if len(data) != 2:
            return
        amps.append(data[1])
        # clear graph
        plt.cla()
        plt.plot(amps)
        if data[0] == 0:
            # print traight line in graph
            pass

ani = FuncAnimation(plt.gcf(),animate,1)
plt.show()

# while True:
#     ret, frame = cap.read()
#     #assert(ret)
#     cv2.imshow('a',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
# plt.show()