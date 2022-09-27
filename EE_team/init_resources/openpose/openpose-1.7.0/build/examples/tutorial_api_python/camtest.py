import sys
import cv2



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


def read_cam():
    cap = cv2.VideoCapture(gstreamer_pipeline(),cv2.CAP_GSTREAMER)

    num = 0

    while cap.isOpened():

        succes1, img = cap.read()

        k = cv2.waitKey(5)

        if k == 27:
            break
        # elif k == ord('s'): # wait for 's' key to save and exit
        #     success=cv2.imwrite('stereoLeft/imageL/' + str(num) + '.png', img)
        #     print("images saved!")
        #     print(success)
        #     num += 1

        #     cv2.imshow('Img 1',img)



    #cv2.imshow('Img 2',img2)

    # cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    # if cap.isOpened():
    #     cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
    #     while True:
    #         ret_val, img = cap.read();
    #         cv2.imshow('demo',img)
    #         cv2.waitKey(10)
    # else:
    #  print("camera open failed")

    # cv2.destroyAllWindows()


if __name__ == '__main__':
    read_cam()
