import cv2 as cv
import Pose_estimaton_module as pt
import time
import random
import math
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        self.video.set(3, 1200)
        self.video.set(4, 1000)
        self.ctime = 0
        self.ptime = 0
        self.count = 0
        self.dir = 0
        self.detector = pt.poseDetector()

    def __del__(self):
        self.video.release()

    def get_pushup(self):
        per = 1000
        ret, frame = self.video.read()
        if not ret:
            return None

        frame = cv.flip(frame, 1)
        frame = self.detector.findPose(frame, draw=False)
        detect = self.detector.findLandmarks(frame, draw=False)

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
                if self.dir==0:
                    self.count+=0.5
                    self.dir=1
            if per>90:
                if self.dir==1:
                    self.count+=0.5
                    self.dir=0
        self.ctime = time.time()
        fps = 1/(self.ctime-self.ptime)
        self.ptime = self.ctime
        cv.putText(frame,f"Pushup counter = {int(self.count)}",(300,70),cv.FONT_HERSHEY_SCRIPT_COMPLEX,2,(255,255,255),2)
        ret, jpeg = cv.imencode('.jpg', frame)
        if not ret:
            return None
        return jpeg.tobytes()

    def get_count(self):
        a = self.count
        return a