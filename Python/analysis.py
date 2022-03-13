import cv2
import pyqtgraph as pg
import numpy as np

#test_id = '0007A0F7C4_1'

def analysis_window(test_id):
    filename = f'{test_id}/{test_id}_experiment_1_recording_1/rpicamera_video.h264'
    #subprocess.run(['ffmpeg','-y','-i',f'{filename}.h264',f'{filename}.mp4'])
    cap = cv2.VideoCapture(filename)

    with open(f"{test_id}/TTL high millis - {test_id}.csv",'r') as ttl_file:
        TTLarray = np.loadtxt(ttl_file)

    TTLarray =  np.unique(TTLarray)

    with open(f"{test_id}/Test data - {test_id}.csv",'r') as ttl_file:
        for line in ttl_file:
            l = line.strip().split(',')
            if l[0] == 'lick_threshold':
                threshold = int(l[1])
                break
        
    lick_file = open(f"{test_id}/Raw lick data - {test_id}.csv",'r')
    _ = lick_file.readline()    #file_time
    _ = lick_file.readline()    #file_heading
    startTime = int(lick_file.readline())
    lick_file.close()

    #threshold = 100

    testT,amps = np.genfromtxt(f"{test_id}/Raw lick data - {test_id}.csv", unpack=True,delimiter=',',skip_header=3,skip_footer=1)

    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    millis = int(TTLarray[0])
    idx = 0
    startTests = [i for i,k in enumerate(testT) if k==0] 
    line = pg.plot(amps,pen='b')
    for k in startTests:
        v = pg.InfiniteLine(k,angle=90,pen='r')
        line.addItem(v)
    h = pg.InfiniteLine(threshold,angle=0)
    line.addItem(h)
    line.setYRange(0,threshold*1.5)

    while millis<TTLarray[-1]:
        #print(millis)
        try:
            _, frame = cap.read()
            cv2.imshow('Press q to exit',frame)
        except:
            break
        #ax2.imshow(frame)
        idx += 1 

        #frame_rate to be adjusted according to the PC
        #frame_rate = 15 if millis < startTime else 10
        frame_rate = 1
        if cv2.waitKey(frame_rate) & 0xFF == ord('q'):
            break
        if millis > startTime:
            #ax1.clear()
            t = millis - startTime
            s = t-5000 if t>=5000 else 0
            # plt_y = amps[s:t]
            # plt_x = np.append(plt_x,t)
            # plt_x = plt_x[-5000:]
            # # clear graph
            # line.set_data(plt_x,plt_y)
            # line.axes.relim()
            line.setXRange(s,t)
            
            # line.axes.autoscale_view()
            # line.axes.figure.canvas.draw()
            #ax1.set_ylim(bottom=0)

            #plt.pause(0.001)
        # if millis%10000 == 0:
        #     print(millis)
        millis = TTLarray[idx]

    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    test_id = '00079EB022_1'
    analysis_window(test_id)