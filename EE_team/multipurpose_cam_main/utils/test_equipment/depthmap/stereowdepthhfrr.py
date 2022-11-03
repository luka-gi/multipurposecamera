import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
import mediapipe as mp

# Function for stereo vision and depth estimation
import triangulation as tri
import calibration

# Mediapipe for face detection

import time

mp_facedetector = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils

# Open both cameras
cap_right = cv2.VideoCapture(4, cv2.CAP_V4L)                    
cap_left =  cv2.VideoCapture(3, cv2.CAP_V4L)


# Stereo vision setup parameters
frame_rate = 20   #Camera frame rate (maximum at 120 fps)
B = 6               #Distance between the cameras [cm]
f = 2.6              #Camera lense's focal length [mm]
alpha = 73       #Camera field of view in the horisontal plane [degrees]




# Main program loop with face detector and depth estimation using stereo vision
#with mp_facedetector.FaceDetection(min_detection_confidence=0.7) as face_detection:

while(cap_right.isOpened() and cap_left.isOpened()):

    succes_right, frame_right = cap_right.read()
    succes_left, frame_left = cap_left.read()

    ################## CALIBRATION #########################################################

    frame_right, frame_left = calibration.undistortandRectify(frame_right, frame_left)

    ########################################################################################

        # If cannot catch any frame, break
    if not succes_right or not succes_left:                    
        break

    else:

        start = time.time()
            
            # Convert the BGR image to RGB
        frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
        frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)

        #     # Process the image and find faces
        results_right = face_detection.process(frame_right)
        results_left = face_detection.process(frame_left)

            # Convert the RGB image to BGR
        frame_right = cv2.cvtColor(frame_right, cv2.COLOR_RGB2BGR)
        frame_left = cv2.cvtColor(frame_left, cv2.COLOR_RGB2BGR)


            ################## CALCULATING DEPTH #########################################################

        center_right = frame_right[640,360,0]
        center_left = frame_left[640,360,0]



        plsbedepth = tri.find_depth(center_right, center_left, frame_right, frame_left, B,f, alpha)
        if results_right.detections:
            for id, detection in enumerate(results_right.detections):
                mp_draw.draw_detection(frame_right, detection)

                bBox = detection.location_data.relative_bounding_box

                h, w, c = frame_right.shape

                boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

                center_point_right = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                cv2.putText(frame_right, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)


            if results_left.detections:
                for id, detection in enumerate(results_left.detections):
                    mp_draw.draw_detection(frame_left, detection)

                    bBox = detection.location_data.relative_bounding_box

                    h, w, c = frame_left.shape

                    boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

                    center_point_left = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                    cv2.putText(frame_left, f'{int(detection.score[0]*100)}%', (boundBox[0], boundBox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
        
        print(plsbedepth)