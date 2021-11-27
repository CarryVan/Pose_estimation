import cv2
import mediapipe as mp

import numpy as np
import pickle
import pandas as pd
import time

class poseDetector():
 
    def __init__(self,
               static_image_mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence= min_tracking_confidence
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode,
                                    self.model_complexity,
                                    self.smooth_landmarks,
                                    self.enable_segmentation,
                                    self.smooth_segmentation,
                                    self.min_detection_confidence,
                                    self.min_tracking_confidence)
 
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
 
    def draw_count(self, img, model_dir, draw, cnt):

        with open(f'{model_dir}', 'rb') as f:
            model = pickle.load(f)

        status = 'pushup_u'

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)

        self.lmList = []
        landmarks = self.results.pose_landmarks.landmark
        pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for idx, landmark in enumerate(landmarks) if idx >= 10]).flatten())
        X = pd.DataFrame([pose_row])
        body_language_class = model.predict(X)[0]
        body_language_prob = model.predict_proba(X)[0]

        if status == 'pushup_d' and body_language_class == 'pushup_u':
            cnt += 1
        status = body_language_class
        # try:

            
        # except:
        #     cv2.putText(img, "None", (30, 30), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)  
        #     cv2.putText(img, 'cnt: ' + str(cnt), (30, 200), 
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
       
        
        return img, body_language_class, body_language_prob, cnt


 
