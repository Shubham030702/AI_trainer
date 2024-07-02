# This is Pushup personal trainer 

import cv2 as cv
import numpy as np
import time
import Pose_estimaton_module as pm

capture = cv.VideoCapture(0)
capture.set(3,1400)
capture.set(4,1100)

ptime=0

detector = pm.poseDetector()
count=0
dir=0
while True:
    per=1000
    istrue,frame = capture.read()
    frame=detector.findPose(frame,draw=False)
    detect=detector.findLandmarks(frame,draw=False)
    if len(detect)!=0:
        x1,y1=detect[16][1:]
        x2,y2=detect[15][1:]
        x3,y3 = int((x2+x1)//2),int((y2+y1)//2)
        x4,y4=detect[12][1:]
        x5,y5=detect[11][1:]
        x6,y6 = int((x4+x5)//2),int((y4+y5)//2)
        cv.circle(frame,(x1,y1),20,(255,0,255),-1)
        cv.circle(frame,(x2,y2),20,(255,0,255),-1)
        cv.circle(frame,(x3,y3),20,(255,0,255),-1)
        cv.circle(frame,(x4,y4),20,(255,0,255),-1)
        cv.circle(frame,(x5,y5),20,(255,0,255),-1)
        cv.circle(frame,(x6,y6),20,(255,0,255),-1)
        cv.line(frame,(x1,y1),(x2,y2),(255,0,255),2)
        cv.line(frame,(x3,y3),(x6,y6),(255,0,255),2)
        cv.line(frame,(x4,y4),(x5,y5),(255,0,255),2)
        length = np.hypot((x6-x3),(y6-y3))
        per = np.interp(length,(160,545),(0,100))
    
    if per<30:
        if dir==0:
            count+=0.5
            dir=1
    if per>90:
        if dir==1:
            count+=0.5
            dir=0
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv.putText(frame,f"pushup counter = {int(count)}",(700,70),cv.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    cv.putText(frame,f"Fps = {str(int(fps))}",(30,50),cv.FONT_HERSHEY_SIMPLEX,2,(255,0,255),4)
    cv.imshow("Web Cam",frame)
    if cv.waitKey(20) & 0xff==ord('r'):
        count=0
        dir=0
    if cv.waitKey(20) & 0xff == ord('d'):
        break
    
capture.release()
cv.destroyAllWindows()
