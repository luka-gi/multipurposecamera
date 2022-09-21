import cv2
import sys
import time


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=3280,
    capture_height=2464,
    display_width=960,
    display_height=540,
    framerate=10,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# def gstreamer_pipeline2(
#     sensor_id=1,
#     capture_width=3280,
#     capture_height=2464,
#     display_width=960,
#     display_height=540,
#     framerate=10,
#     flip_method=0,
# ):
#     return (
#         "nvarguscamerasrc sensor-id=%d !"
#         "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
#         "nvvidconv flip-method=%d ! "
#         "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
#         "videoconvert ! "
#         "video/x-raw, format=(string)BGR ! appsink"
#         % (
#             sensor_id,
#             capture_width,
#             capture_height,
#             framerate,
#             flip_method,
#             display_width,
#             display_height,
#         )
#     )
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0),cv2.CAP_GSTREAMER)
# cap2 = cv2.VideoCapture(gstreamer_pipeline2(flip_method=0),cv2.CAP_GSTREAMER)

num = 0

while cap.isOpened():

    succes1, img = cap.read()
    # succes2, img2 = cap2.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        success=cv2.imwrite('stereoLeft/imageL/' + str(num) + '.png', img)
        # cv2.imwrite('stereoright/imageR/' + str(num) + '.png', img2)
        print("images saved!")
        print(success)
        # num += 1

    cv2.imshow('Img 1',img)
    cv2.imshow('Img 2',img2)

# Release and destroy all windows before termination
cap.release()
cap2.release()

cv2.destroyAllWindows()