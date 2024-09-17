import cv2 as cv
import Pose_estimaton_module as pt
import time
import random
import math
import numpy as np
import tkinter as tk
from tkinter import simpledialog

class VideoCamera2(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)
        self.video.set(3, 1200)
        self.video.set(4, 1000)
        self.ctime = 0
        self.ptime = 0
        self.count = 0
        self.dir = 0
        self.detector = pt.poseDetector()
        self.arm = self.get_user_input()

    def get_user_input(prompt="Which side Bicep to train :"):
        root = tk.Tk()
        root.withdraw() 
        user_input = simpledialog.askstring(title="Input", prompt=prompt)
        return user_input

    def __del__(self):
        self.video.release()

    def get_bicep(self):
        per = 1000
        ret, frame = self.video.read()
        if not ret:
            return None
        frame = self.detector.findPose(frame,False)
        landmarks = self.detector.findLandmarks(frame,False)
        if len(landmarks)!=0:
            per=1000
            if(self.arm=="right"):
                angle = self.detector.findAngle(frame,12,14,16)
                per = np.interp(angle,(60,160),(0,100))
            if(self.arm=="left"):
                angle = self.detector.findAngle(frame,11,13,15)
                per = np.interp(angle,(190,310),(0,100))
            if per >= 95:
                if self.dir == 0:
                   self.count+=0.5
                   self.dir=1
            if per <=25:
                if self.dir == 1:
                   self.count+=0.5
                   self.dir=0
        cv.putText(frame,f"Curl counter = {int(self.count)}",(300,70),cv.FONT_HERSHEY_SCRIPT_COMPLEX,2,(255,255,255),2)
        ret, jpeg = cv.imencode('.jpg', frame)
        if not ret:
            return None
        return jpeg.tobytes()

    def get_count(self):
        a = self.count
        self.count = 0
        return a