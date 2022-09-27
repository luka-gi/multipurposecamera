import subprocess
import cv2
import sys
import keyboard

displaymode = False

#venv paths
NVIDIA_python2_path = "/usr/bin/python"
cam_img_cap = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/util/cam_img_cap.py"

#other paths
openpose_build_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build"
image_path = "./imgs/live_test/"
sys.path.append(openpose_build_path + '/python')
from openpose import pyopenpose as op

def testcode():
    print("Python version: "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+"."+str(sys.version_info.micro)+"\n")

def live_to_openpose():
    opWrapper = op.WrapperPython()
    opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
    opWrapper.start()

    key = 0

    while key != ord('q'):
        #run the camera cap module
        subprocess.run([NVIDIA_python2_path,cam_img_cap,image_path+"live.png"])

        datum = op.Datum()
        imageToProcess = cv2.imread(image_path+"live.png")
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        # Display Image
        print("Body keypoints: \n" + str(datum.poseKeypoints))
        cv2.imwrite(image_path+"op.png",datum.cvOutputData)

        if displaymode:          
            cv2.imshow("before op",imageToProcess)
            cv2.imshow("after op",datum.cvOutputData)
            key = cv2.waitKey(5)

    cv2.destroyAllWindows()

if __name__ == "__main__":   
    # subprocess.run([NVIDIA_python2_path,"--version"])
    if len(sys.argv)==1:
        print("shell script in regular mode")
        print("Please ensure that you are only running this from the bash script. Python version should be 3.6.9")
        print("Python version: "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+"."+str(sys.version_info.micro)+"\n")
        live_to_openpose()
    elif len(sys.argv)==2 and (sys.argv[1] == "-d" or sys.argv[1] == "--display"):
        print("shell script in display mode")
        displaymode = True
        live_to_openpose()
    else:
        print("incorrect arguments")
