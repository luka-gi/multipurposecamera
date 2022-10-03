import cv2
import sys
import argparse
import time
from multiprocessing import Process
import matplotlib.pyplot

displaymode = False
verbose = False
run_openpose = False
write_images = False
thermal_device_id = 2
openpose_device_id = 3
IMG_BUFFER_DISCARD = 1
CAP_BUFFER_SIZE = 1

#venv paths
NVIDIA_python2_path = "/usr/bin/python"
cam_img_cap = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/utils/cam_img_cap.py"

#other paths
openpose_build_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build"
image_path = "./imgs/live_test/"
sys.path.append(openpose_build_path + '/python')
from openpose import pyopenpose as op

def capture_img(cap, image_path, capname):
    success, img = cap.read()
    if success:
        if write_images:
            cv2.imwrite(image_path,img)
        if verbose:
            print("\n{} camera cap: success".format(capname))
    else:
        if verbose:
            print("\n{} camera cap: failure".format(capname))
    return img

def compute_openpose(opWrapper, datum, imageToProcess):
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))

def live_to_openpose():
    capth = cv2.VideoCapture(thermal_device_id)
    #cap = cv2.VideoCapture(openpose_device_id)
    #cap.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)
    capth.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)

    if not capth.isOpened():
        print("Please make sure 'openpose_device_id' is set to the correct device.")
        print("It is currently /dev/video" + str(openpose_device_id))
    else:
        opWrapper = op.WrapperPython()
        opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
        opWrapper.start()

        key = 0
        images_discarded_from_buffer = IMG_BUFFER_DISCARD

        while key != ord('q'):

            #datum_stereo = op.Datum()
            datum_thermal = op.Datum()

            time_imcap_th_be = time.time()
            thermalImageToProcess = capture_img(capth, image_path+"liveth.png", "thermal")
            time_imcap_th_fi = time.time()
            #time_imcap_st_be = time.time()
            #imageToProcess = capture_img(cap, image_path+"live.png", "stereo")
            #time_imcap_st_fi = time.time()

            images_discarded_from_buffer = images_discarded_from_buffer + 1
            if run_openpose and images_discarded_from_buffer >= IMG_BUFFER_DISCARD:
                images_discarded_from_buffer = 0

                time_comp_th_be=time.time()
                compute_openpose(opWrapper,datum_thermal,thermalImageToProcess)
                time_comp_th_fi=time.time()

                #time_comp_st_be=time.time()
                #compute_openpose(opWrapper,datum_stereo,imageToProcess)
                #time_comp_st_fi=time.time()

                if write_images:
                    #cv2.imwrite(image_path+"op.png",datum_stereo.cvOutputData)
                    cv2.imwrite(image_path+"th.png",datum_thermal.cvOutputData)

            if verbose:
                #print("Body keypoints: \n" + str(datum_stereo.poseKeypoints))
                print("Thermal keypoints: \n" + str(datum_thermal.poseKeypoints))

            # Display Image
            if displaymode: 
                if run_openpose:
                    #time_show_st_be = time.time()         
                    #cv2.imshow("output display",datum_stereo.cvOutputData)
                    #time_show_st_fi = time.time() 
                    time_show_th_be = time.time() 
                    cv2.imshow("thermal display",datum_thermal.cvOutputData)
                    time_show_th_fi = time.time()

                    delay_imcap_th = time_imcap_th_fi-time_imcap_th_be
                    #delay_imcap_st = time_imcap_st_fi-time_imcap_st_be
                    delay_comp_th = time_comp_th_fi-time_comp_th_be
                    #delay_comp_st = time_comp_st_fi-time_comp_st_be
                    delay_show_th = time_show_th_fi-time_show_th_be
                    #delay_show_st = time_show_st_fi-time_show_st_be
                    print("   TIMES:") 
                    print("\tCAP TIMES:")
                    print("\t\tTHERMAL:",delay_imcap_th)
                    #print("\t\tSTEREO:",delay_imcap_st)
                    print("\tCOMP TIMES:")
                    print("\t\tTHERMAL:",delay_comp_th)
                    #print("\t\tSTEREO:",delay_comp_st)
                    print("\tSHOW TIMES:")
                    print("\t\tTHERMAL:",delay_show_th)
                    #print("\t\tSTEREO:",delay_show_st)
                    print("\tSINGLE CYCLE DELAY:")
                    print("\t\tTHERMAL DELAY:",delay_imcap_th+delay_comp_th+delay_show_th)
                    #print("\t\tSTEREO DELAY:",delay_imcap_st+delay_comp_st+delay_show_st)
                    #print("\t\tTOTAL DELAY:",delay_imcap_th+delay_comp_th+delay_show_th+delay_imcap_st+delay_comp_st+delay_show_st)
                else:
                    #cv2.imshow("output display",imageToProcess)

                    cv2.imshow("thermal display",thermalImageToProcess)

                key = cv2.waitKey(1)

        #cap.release()
        capth.release()
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
    if (args.device == 3 or args.device == 4):
        openpose_device_id = args.device
    else:
        print("\nDevice ID not valid. --device 3 for stereo left and --device 4 for stereo right.\n")

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
