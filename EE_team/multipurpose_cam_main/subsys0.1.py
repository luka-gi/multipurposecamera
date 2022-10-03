import cv2
import sys
import argparse

displaymode = False
verbose = False
run_openpose = False
write_images = False
openpose_device_id = 3

#venv paths
NVIDIA_python2_path = "/usr/bin/python"
cam_img_cap = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/utils/cam_img_cap.py"

#other paths
openpose_build_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build"
image_path = "./imgs/live_test/"
sys.path.append(openpose_build_path + '/python')
from openpose import pyopenpose as op

# device id of camera we analyze openpose images from

def capture_img(cap, image_path):
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

def live_to_openpose():
    cap = cv2.VideoCapture(openpose_device_id)
    if not cap.isOpened():
        print("Please make sure 'openpose_device_id' is set to the correct device.")
        print("It is currently /dev/video" + str(openpose_device_id))
    else:
        opWrapper = op.WrapperPython()
        opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
        opWrapper.start()

        key = 0

        while key != ord('q'):
            datum = op.Datum()

            imageToProcess = capture_img(cap, image_path+"live.png")

            if run_openpose:
                datum.cvInputData = imageToProcess
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                if write_images:
                    cv2.imwrite(image_path+"op.png",datum.cvOutputData)

            if verbose:
                print("Body keypoints: \n" + str(datum.poseKeypoints))

            # Display Image
            if displaymode: 
                if run_openpose:         
                    cv2.imshow("output display",datum.cvOutputData)
                else:
                    cv2.imshow("output display",imageToProcess)
                key = cv2.waitKey(5)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Args for multipurposecamera script. All false by default')
    parser.add_argument('-v','--verbose', action='store_true', help='verbose output')
    parser.add_argument('-d','--display', action='store_true', help='display images to monitor')
    parser.add_argument('-p','--process', action='store_true', help='process using openpose (default off to save memory)')
    parser.add_argument('-w','--write', action='store_true', help='save images to disk')
    parser.add_argument('-a','--all', action='store_true', help='enable all options')
    parser.add_argument('--device', type=int, help='specify device number')

    args = parser.parse_args()

    displaymode = args.display or args.all
    verbose = args.verbose or args.all
    run_openpose = args.process or args.all
    write_images = args.write or args.all
    if (args.device == 2 or args.device == 3 or args.device == 4):
        openpose_device_id = args.device
    else:
        print("\nDevice ID not valid. --device 2 for thermal, --device 3 for stereo left, and --device 4 for stereo right.\n")

    if verbose:
        print("\nrunning with arguments:\n")
        print("verbose =",verbose)
        print("display =",displaymode)
        print("process =",run_openpose)
        print("write =",write_images)
        print("using device /dev/video"+str(openpose_device_id))

    if not (verbose or displaymode or run_openpose or write_images or args.all):
        print("\n=====================================================================")
        print("  WARN: you have not run the module with any args. see list with -h")
        print("=====================================================================")

    print("\nPlease ensure that you are only running this from the bash script. Python version should be 3.6.9")
    print("Python version: "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+"."+str(sys.version_info.micro)+"\n")

    live_to_openpose()
