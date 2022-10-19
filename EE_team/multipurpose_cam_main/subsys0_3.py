import cv2
import sys
import time
import numpy as np
from flirpy.camera.lepton import Lepton

thermal_device_id = 2
# IMG_BUFFER_DISCARD = 1
CAP_BUFFER_SIZE = 1

#venv paths
NVIDIA_python2_path = "/usr/bin/python"
cam_img_cap = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/utils/cam_img_cap.py"

#other paths
openpose_build_path = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build"
image_path = "./imgs/live_test/"
sys.path.append(openpose_build_path + '/python')
from openpose import pyopenpose as op

def capture_img(cap, image_path, capname, displaymode,verbose,run_openpose,write_images,openpose_device_id):
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


def run(displaymode,verbose,run_openpose,write_images,openpose_device_id):
    args = (displaymode,verbose,run_openpose,write_images,openpose_device_id)

    # capth = cv2.VideoCapture(thermal_device_id)
    # capth.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)
    tempcap = Lepton()
    cap = cv2.VideoCapture(openpose_device_id)
    cap.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)

    if not cap.isOpened():
        print("Please make sure 'openpose_device_id' is set to the correct device.")
        print("It is currently /dev/video" + str(openpose_device_id))
    else:
        if run_openpose:
            opWrapper = op.WrapperPython()
            opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
            opWrapper.start()

        key = 0
        # images_discarded_from_buffer = IMG_BUFFER_DISCARD

        while key != ord('q'):

            datum = op.Datum()

            time_imcap_th_be = time.time()
            
            tempmap = tempcap.grab()
            print("Thermal camera cap: success")
            tempmap= np.multiply(tempmap,0.005)
            tempmap = tempmap - 273.15
            tempmap = np.multiply(tempmap,9/5) +32
            #Rescale to 8 bit
            imagenorm = 255*(tempmap - tempmap.min())/(tempmap.max()-tempmap.min()) 
            # thermalImageToProcess = cv2.applyColorMap((tempmap/256).astype(np.uint8),cv2.COLORMAP_JET)
            thermalImageToProcess = cv2.applyColorMap((tempmap/256).astype(np.uint8),cv2.COLORMAP_JET)
            # thermalImageToProcess = capture_img(capth, image_path+"liveth.png", "thermal", *args)
            time_imcap_th_fi = time.time()
            time_imcap_st_be = time.time()
            imageToProcess = capture_img(cap, image_path+"live.png", "stereo", *args)
            time_imcap_st_fi = time.time()

            if run_openpose:

                time_comp_st_be=time.time()
                datum.cvInputData = imageToProcess
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                time_comp_st_fi=time.time()

                if write_images:
                    cv2.imwrite(image_path+"op.png",datum.cvOutputData)

                # if people detected, calculate their eyes/nose. use this to calculate forehead
                if datum.poseKeypoints is not None:
                    person_num = 0
                    foreheads = [0] * len(datum.poseKeypoints)

                    for person in datum.poseKeypoints:
                        # according to default body_25 model, keypoint0 is nose, keypoint15/16 are eyes
                        # keypoint is made up of (xcoord,ycoord,confidence). we ignore confidence
                        nose = person[0][0:-1]
                        key_eye_R = person[15][0:-1]
                        key_eye_L = person[16][0:-1]

                        if verbose:
                            print("person "+ str(person_num) +"'s nose coords:" + str(nose))
                            print("person "+ str(person_num) +"'s eyeL coords:" + str(key_eye_L))
                            print("person "+ str(person_num) +"'s eyeR coords:" + str(key_eye_R))

                        #math is included in report
                        eyes_midpoint = np.array([key_eye_R[0]+(key_eye_L[0]-key_eye_R[0])/2,
                                key_eye_L[1]+(key_eye_R[1]-key_eye_L[1])/2])
                        
                        eyes_midpoint_to_nose_scalefactor = 1.6
                        forehead = eyes_midpoint-eyes_midpoint_to_nose_scalefactor*(nose-eyes_midpoint)

                        foreheads[person_num] = forehead

                        person_num = person_num + 1

                    print("foreheads:",foreheads)

            if verbose:
                print()
                print("Body keypoints: \n" + str(datum.poseKeypoints))

            # Display Image
            if displaymode: 
                    # the following comments assume subject is about 0.5 m from camera
                x_offset = 260 #the following values were experimentally obtained
                y_offset = 125 #seems to work on left camera with respective values:
                x_scale = 5.65    #280,160,6,4
                y_scale = 4.5
                if run_openpose:
                    time_show_be = time.time() 
                    img_combined = datum.cvOutputData 

                    thermalImageToProcess = cv2.resize(thermalImageToProcess,(int(thermalImageToProcess.shape[1]*x_scale),int(thermalImageToProcess.shape[0]*y_scale))) 
                    
                    #get temps from thermal image (after resizing)
                    # n = 0.005
                    # m = (9/5)
                    # temps_from_image = np.multiply(tempmap,n)
                    # temps_from_image = temps_from_image - 273.15
                    # temps_from_image = np.multiply(temps_from_image,m) +32
                    # temps_from_image = 255*(temps_from_image - temps_from_image.min())/(temps_from_image.max()-temps_from_image.min())

                    if verbose: 
                        # print("temps from thermal img", temps_from_image)
                        print("stereo img shape",img_combined.shape)
                        print("thermal img shape",thermalImageToProcess.shape)

                    img_combined[y_offset:y_offset+thermalImageToProcess.shape[0],x_offset:x_offset+thermalImageToProcess.shape[1]] = thermalImageToProcess
                    
                    # add forehead marker (if applicable)
                    if run_openpose and datum.poseKeypoints is not None:
                        forehead_marker_color = (0,0,0)

                        for person_forehead in foreheads:
                            cv2.drawMarker(img_combined,(int(person_forehead[0]),int(person_forehead[1])), forehead_marker_color,
                             markerType=cv2.MARKER_DIAMOND, markerSize=10, thickness=10, line_type=cv2.LINE_AA)
                    cv2.imshow("output display",img_combined)
                    time_show_fi = time.time()

                    if verbose:
                        delay_imcap_th = time_imcap_th_fi-time_imcap_th_be
                        delay_imcap_st = time_imcap_st_fi-time_imcap_st_be
                        delay_comp_st = time_comp_st_fi-time_comp_st_be
                        delay_show = time_show_fi-time_show_be

                        print("   TIMES:") 
                        print("\tCAP TIMES:")
                        print("\t\tTHERMAL:",delay_imcap_th)
                        print("\t\tSTEREO:",delay_imcap_st)
                        print("\tCOMP TIMES:")
                        print("\t\tSTEREO:",delay_comp_st)
                        print("\tSHOW TIME:")
                        print("\t\tSHOW DELAY:",delay_show)
                        print("\tSINGLE CYCLE DELAY:")
                        print("\t\tTHERMAL DELAY:",delay_imcap_th)
                        print("\t\tSTEREO DELAY:",delay_imcap_st+delay_comp_st)
                        print("\t\tTOTAL DELAY:",delay_imcap_th+delay_show+delay_imcap_st+delay_comp_st)
                else:
                    time_show_be = time.time() 
                    img_combined = imageToProcess

                    thermalImageToProcess = cv2.resize(thermalImageToProcess,(int(thermalImageToProcess.shape[1]*x_scale),int(thermalImageToProcess.shape[0]*y_scale))) 
                    if verbose: 
                        print("stereo img shape",img_combined.shape)
                        print("thermal img shape",thermalImageToProcess.shape)

                    img_combined[y_offset:y_offset+thermalImageToProcess.shape[0],x_offset:x_offset+thermalImageToProcess.shape[1]] = thermalImageToProcess
                    cv2.imshow("output display",img_combined)
                    time_show_fi = time.time() 
                    if verbose:
                        delay_imcap_th = time_imcap_th_fi-time_imcap_th_be
                        delay_imcap_st = time_imcap_st_fi-time_imcap_st_be
                        delay_show = time_show_fi-time_show_be

                        print("   TIMES:") 
                        print("\tCAP TIMES:")
                        print("\t\tTHERMAL:",delay_imcap_th)
                        print("\t\tSTEREO:",delay_imcap_st)
                        print("\tSHOW TIME:")
                        print("\t\tSHOW DELAY:",delay_show)
                        print("\tSINGLE CYCLE DELAY:")
                        print("\t\tTHERMAL DELAY:",delay_imcap_th)
                        print("\t\tSTEREO DELAY:",delay_imcap_st)
                        print("\t\tTOTAL DELAY:",delay_imcap_th+delay_show+delay_imcap_st)

                if write_images:
                    cv2.imwrite(image_path+"th+op.png",img_combined)

                key = cv2.waitKey(1)

        #cap.release()
        # capth.release()
        cv2.destroyAllWindows()
