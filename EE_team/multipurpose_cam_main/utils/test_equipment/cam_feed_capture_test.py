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

def show_camera():

    cap0 = cv2.VideoCapture(gstreamer_pipeline(0),cv2.CAP_GSTREAMER)
    cap1 = cv2.VideoCapture(gstreamer_pipeline(1),cv2.CAP_GSTREAMER)

    num = 0

    while cap0.isOpened() and cap1.isOpened():

        success0, img0 = cap0.read()
        success1, img1 = cap1.read()

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

        cv2.imshow('Img 0',img0)
        cv2.imshow('Img 1',img1)

    # Release and destroy all windows before termination
    cap0.release()
    cap1.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_camera()
