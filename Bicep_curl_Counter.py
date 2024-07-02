# this is a program to count the push ups 

import cv2 as cv
import numpy as np
import time
import Pose_estimaton_module as pt
import tkinter as tk
from tkinter import simpledialog

def get_user_input(prompt="Which side Bicep to train :"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = simpledialog.askstring(title="Input", prompt=prompt)
    return user_input


capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FRAME_WIDTH,1400)
capture.set(cv.CAP_PROP_FRAME_HEIGHT,1300)
ptime=0

arm = get_user_input()

detector = pt.poseDetector()


count = 0
dir = 0
while True:
    istrue,frame = capture.read()
    detector.findPose(frame,False)
    landmarks = detector.findLandmarks(frame,False)
    if len(landmarks)!=0:
        per=1000
        if(arm=="right"):
            angle = detector.findAngle(frame,12,14,16)
            per = np.interp(angle,(33,167),(0,100))
        if(arm=="left"):
            angle = detector.findAngle(frame,11,13,15)
            per = np.interp(angle,(210,325),(0,100))
        # check for the perfect curl
        if per >= 95:
            if dir == 0:
                count+=0.5
                dir=1
        if per <=10:
            if dir==1:
                count+=0.5
                dir=0

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv.putText(frame,f"FPS = {str(int(fps))}",(30,70),cv.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    cv.putText(frame,f"Curl counter = {int(count)}",(700,70),cv.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    cv.imshow("WebCam",frame)
    if cv.waitKey(20) & 0xff==ord('r'):
        count=0
        dir=0
    if cv.waitKey(20) & 0xff==ord('d'):
        break

capture.release()
cv.destroyAllWindows()