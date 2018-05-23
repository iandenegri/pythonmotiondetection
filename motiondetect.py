# This project requires a base image file before hand for it to work. You need
# a base image of the background of your video. Used for comparison in frames.
# You need a webcame for this to work. If you want to use a video file then in
# in the VideoCapture method you have to change the 0 to the file path of your
# video and have an image of the video background to use as comparison.

import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list=[None, None]
times=[]
df=pandas.DataFrame(columns=['Start','End'])

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    # if 0 there is no motion, if 1 there is something moving.
    motion_status = 0

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame = gray
        continue
        # continue means to restart the loop and don't carry out the lines under
        # this line

# frames
    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

# Countour work
    (_,cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            continue
        motion_status=1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

# updating status for determining when movement is occuring for logging purposes
    status_list.append(motion_status)
    # Something appears
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    # Something disappears
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

# display
    cv2.imshow('Detection Frame', frame)



    key=cv2.waitKey(50)


    if key==ord('q'):
        if motion_status==1:
            times.append(datetime.now())
        break

# Iterating through start and end times by taking steps of 2.
for i in range(0,len(times),2):
    df=df.append({'Start':times[i],'End':times[i+1]},ignore_index=True)

df.to_csv('Times.csv')

video.release()
cv2.destroyAllWindows
