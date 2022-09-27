import cv2
import sys
import time
import subprocess

from PIL import Image

openpose_venv_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openposevenv/bin/python"
body_to_skel_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/capture_to_skel.py"
args = [openpose_venv_path,body_to_skel_path]

def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)

    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr


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
def show_camera():

    cap = cv2.VideoCapture(gstreamer_pipeline(),cv2.CAP_GSTREAMER)
    # cap2 = cv2.VideoCapture(gstreamer_pipeline2(flip_method=0),cv2.CAP_GSTREAMER)

    num = 0

    while cap.isOpened():

        succes1, img = cap.read()
        # succes2, img2 = cap2.read()

        k = cv2.waitKey(5)

	# char 27 == escape on the keyboard

        if k == 27 or k==ord('q'):
            break
        elif k == ord('s'): # wait for 's' key to save and exit
            # success = cv2.imwrite('stereoLeft/imageL/' + str(num) + '.png', img)
            #im = Image.fromarray(img)

            #im.save("./imgs/live_test/live.png") 
            print("images saved! (not really)")
            #run(args)

            # cv2.imwrite('stereoright/imageR/' + str(num) + '.png', img2)
            # print(success)
            # num += 1

        cv2.imshow('Img 1',img)
        # cv2.imshow('Img 2',img2)

    # Release and destroy all windows before termination
    cap.release()
    # cap2.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_camera()
