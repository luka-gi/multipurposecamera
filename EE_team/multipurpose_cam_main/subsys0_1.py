import cv2
import sys
from time import time

#venv paths
NVIDIA_python2_path = "/usr/bin/python"
cam_img_cap = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/utils/cam_img_cap.py"

#other paths
openpose_build_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build"
image_path = "./imgs/live_test/"
sys.path.append(openpose_build_path + '/python')
from openpose import pyopenpose as op

# other vals/ consts
CAP_BUFFER_SIZE = 1

def capture_img(cap, image_path, displaymode,verbose,run_openpose,write_images,openpose_device_id):
    success, img = cap.read()
    if success:
        if write_images:
            cv2.imwrite(image_path,img)
        if verbose:
            print("\ncamera capture: success\n")
    else:
        if verbose:
            print("\ncamera capture: failure\n")
    return img

def subsys0_1(displaymode,verbose,run_openpose,write_images,openpose_device_id):
    args = (displaymode,verbose,run_openpose,write_images,openpose_device_id)

    cap = cv2.VideoCapture(openpose_device_id)
    if not cap.isOpened():
        print("Please make sure 'openpose_device_id' is set to the correct device.")
        print("It is currently /dev/video" + str(openpose_device_id))
    else:
        cap.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)

        opWrapper = op.WrapperPython()
        opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
        opWrapper.start()

        key = 0

        while key != ord('q'):
            datum = op.Datum()

            time_cap_in = time()
            imageToProcess = capture_img(cap, image_path+"live.png", *args)
            time_cap_fi = time()

            if run_openpose:

                time_comp_in = time()
                datum.cvInputData = imageToProcess
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                time_comp_fi = time()

                if write_images:
                    cv2.imwrite(image_path+"op.png",datum.cvOutputData)

            if verbose:
                print("Body keypoints: \n" + str(datum.poseKeypoints))

            # Display Image
            if displaymode: 
                if run_openpose: 
                    time_show_in = time()        
                    cv2.imshow("output display",datum.cvOutputData)
                    time_show_fi = time()
                else:
                    cv2.imshow("output display",imageToProcess)
                if verbose:
                    delay_cap = time_cap_fi-time_cap_in
                    delay_comp = time_comp_fi-time_comp_in
                    delay_show = time_show_fi-time_show_in

                    print("   TIMES:") 
                    print("\tCAP TIMES:")
                    print("\t\tTHERMAL:",delay_cap)
                    print("\tCOMP TIMES:")
                    print("\t\tTHERMAL:",delay_comp)
                    print("\tSHOW TIMES:")
                    print("\t\tTHERMAL:",delay_show)
                    print("\tSINGLE CYCLE DELAY:")
                    print("\t\tTHERMAL DELAY:",delay_cap+delay_comp+delay_show)
                key = cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()