import cv2
import sys
import time
from gi.repository import Gtk

#building gstreamer pipeline
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=256,
    capture_height=128,
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

def cam_img_cap(img_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/imgs/test/test.png"):
    start_time = time.time()
    cap = cv2.VideoCapture(gstreamer_pipeline(),cv2.CAP_GSTREAMER)
    print("EXEC TIME:",1000*(time.time()-start_time))
    success, img = cap.read()
    if success:
        cv2.imwrite(img_path,img)
        print("\ncamera capture: success\n")
    else:
        print("\ncamera capture: failure\n")
    cap.release()
    return

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cam_img_cap(sys.argv[1])
        print("\nsaving img to:" + sys.argv[1] + "\n")
    else:
        print("\nsaving img to test folder\n")
        cam_img_cap()