import cv2
import sys
import time

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

    capth = cv2.VideoCapture(thermal_device_id)
    cap = cv2.VideoCapture(openpose_device_id)
    cap.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)
    capth.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)

    if not cap.isOpened():
        print("Please make sure 'openpose_device_id' is set to the correct device.")
        print("It is currently /dev/video" + str(openpose_device_id))
    else:
        opWrapper = op.WrapperPython()
        opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
        opWrapper.start()

        key = 0
        # images_discarded_from_buffer = IMG_BUFFER_DISCARD

        while key != ord('q'):

            datum = op.Datum()
            # datum_thermal = op.Datum()

            time_imcap_th_be = time.time()
            thermalImageToProcess = capture_img(capth, image_path+"liveth.png", "thermal", *args)
            time_imcap_th_fi = time.time()
            time_imcap_st_be = time.time()
            imageToProcess = capture_img(cap, image_path+"live.png", "stereo", *args)
            time_imcap_st_fi = time.time()

            if run_openpose:
                # images_discarded_from_buffer = 0

                # time_comp_th_be=time.time()
                # compute_openpose(opWrapper,datum_thermal,thermalImageToProcess)
                # time_comp_th_fi=time.time()

                time_comp_st_be=time.time()
                datum.cvInputData = imageToProcess
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                time_comp_st_fi=time.time()

                if write_images:
                    print()
                    #cv2.imwrite(image_path+"op.png",datum_stereo.cvOutputData)
                    # cv2.imwrite(image_path+"th.png",datum_thermal.cvOutputData)

            if verbose:
                print()
                #print("Body keypoints: \n" + str(datum_stereo.poseKeypoints))
                # print("Thermal keypoints: \n" + str(datum_thermal.poseKeypoints))

            # Display Image
            if displaymode: 
                    # the following comments assume subject is about 0.5 m from camera
                x_offset = 285 #the following values were experimentally obtained
                y_offset = 125 #seems to work on left camera with respective values:
                x_scale = 5.65    #280,160,6,4
                y_scale = 4.5
                if run_openpose:
                    time_show_be = time.time() 
                    img_combined = datum.cvOutputData 

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

                key = cv2.waitKey(1)

        #cap.release()
        capth.release()
        cv2.destroyAllWindows()
