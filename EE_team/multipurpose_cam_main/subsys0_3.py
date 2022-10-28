import cv2
import sys
import time
import numpy as np
from flirpy.camera.lepton import Lepton
from scipy.ndimage import interpolation

# number to multiply raw thermal data
THERMAL_CALIBRATION_CONSTANT = 0.00995
# number of forehead temps to take before running statistical analysis. excluded for now. see function details
# NUM_FOREHEAD_TEMPS_PER_LOOP = 30
# a feverish temperature to use as a threshold. right not this is in degrees F
FEVER_TEMP = 100

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

def capture_img(cap, image_path, displaymode,verbose,run_openpose,write_images,openpose_device_id):
    success, img = cap.read()
    
    if success:
        if write_images:
            cv2.imwrite(image_path,img)
        if verbose:
            print("\nstereo camera cap success")
    else:
        if verbose:
            print("\n{} camera cap failure")
    return img

def capture_thermal_img(cap, image_path, displaymode,verbose,run_openpose,write_images,openpose_device_id):
    tempmap = cap.grab().astype(np.float32)
    # convert kelvin to celsius and multiply by some calibration constant
    tempmap = np.multiply(tempmap,THERMAL_CALIBRATION_CONSTANT) - 273.15
    # convert celsius to fahrenheit
    tempmap = np.multiply(tempmap,9/5) +32

    #apply colormap to temp data to make RGB image
    img = 255*(tempmap - tempmap.min())/(tempmap.max()-tempmap.min())
    img = cv2.applyColorMap(img.astype(np.uint8),cv2.COLORMAP_INFERNO)

    if write_images:
        cv2.imwrite(image_path,img)
    if verbose:
        print("\nthermal camera cap complete. displaying temps in F")
        print(tempmap)

    return img, tempmap

def run(displaymode,verbose,run_openpose,write_images,openpose_device_id):
    args = (displaymode,verbose,run_openpose,write_images,openpose_device_id)

    capth = Lepton()
    cap = cv2.VideoCapture(openpose_device_id)
    cap.set(cv2.CAP_PROP_BUFFERSIZE,CAP_BUFFER_SIZE)

    #initialization in order to run statistic analysis in loop. excluded for now. see function details.
    # forehead_temps_loop = 0
    # forehead_stats = [0] * NUM_FOREHEAD_TEMPS_PER_LOOP

    if not cap.isOpened():
        print("Please make sure 'openpose_device_id' is set to the correct device.")
        print("It is currently /dev/video" + str(openpose_device_id))
    else:
        if run_openpose:
            opWrapper = op.WrapperPython()
            opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
            opWrapper.start()

        key = 0

        while key != ord('q'):

            datum = op.Datum()

            time_imcap_th_be = time.time()
            thermalImageToProcess,tempmap = capture_thermal_img(capth, image_path+"liveth.png", *args)
            time_imcap_th_fi = time.time()
            time_imcap_st_be = time.time()
            imageToProcess = capture_img(cap, image_path+"live.png", *args)
            time_imcap_st_fi = time.time()

            if run_openpose:

                time_comp_st_be=time.time()
                datum.cvInputData = imageToProcess
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                time_comp_st_fi=time.time()

                if write_images:
                    cv2.imwrite(image_path+"op.png",datum.cvOutputData)
# ====================================================================================================================
                # forehead detection

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

                        #math is included in report
                        eyes_midpoint = np.array([key_eye_R[0]+(key_eye_L[0]-key_eye_R[0])/2,
                                key_eye_L[1]+(key_eye_R[1]-key_eye_L[1])/2])
                        
                        eyes_midpoint_to_nose_scalefactor = 1.3
                        forehead = eyes_midpoint-eyes_midpoint_to_nose_scalefactor*(nose-eyes_midpoint)

                        foreheads[person_num] = forehead

                        if verbose:
                            print("person "+ str(person_num) +"'s nose coords: " + str(nose))
                            print("person "+ str(person_num) +"'s eyeL coords: " + str(key_eye_L))
                            print("person "+ str(person_num) +"'s eyeR coords: " + str(key_eye_R))
                            print("person "+ str(person_num) +"'s forehead coords: " + str(forehead))

                        person_num = person_num + 1
# ====================================================================================================================
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
                    tempmapscaled = interpolation.zoom(tempmap,[y_scale,x_scale])

                    if verbose:                         
                        print("stereo img shape",img_combined.shape)
                        print("thermal img shape",thermalImageToProcess.shape)
                        print("tempmap scaled shape", tempmapscaled.shape)

                    img_combined[y_offset:y_offset+thermalImageToProcess.shape[0],x_offset:x_offset+thermalImageToProcess.shape[1]] = thermalImageToProcess
                                        
# ====================================================================================================================
                    # forehead fever detection

                    if run_openpose and datum.poseKeypoints is not None:
                        person_num = 0
                        # this array has the format [forehead_temp,has_fever]
                        foreheads_temps = [[0,False]] * len(datum.poseKeypoints)
                        
                        for person_forehead in foreheads:  
                            # add forehead marker (if applicable)
                            forehead_marker_color = (255,255,255)

                            cv2.drawMarker(img_combined,(int(person_forehead[0]),int(person_forehead[1])), forehead_marker_color,
                            markerType=cv2.MARKER_DIAMOND, markerSize=10, thickness=10, line_type=cv2.LINE_AA)

                            #make sure detected forehead is in range of thermal cam otherwise program will crash or report incorrect value
                            # please do not confuse forehead[0] (x value) with .shape[0] (y_value). I don't know why images are heightxwidth here
                            # set out of bound forehead temp to None to reduce ambiguity
                            if (x_offset < forehead[0] and forehead[0] < x_offset + thermalImageToProcess.shape[1] and y_offset < forehead[1] and forehead[1] < y_offset + thermalImageToProcess.shape[0]):
                                font = cv2.FONT_HERSHEY_COMPLEX
                                scale = 1
                                color = (255,255,255)
                                thickness = 1
                                lineType = 2

                                forehead_temp = tempmapscaled[int(person_forehead[1]-y_offset),int(person_forehead[0]-x_offset)]
# ====================================================================================================================
# see test 0.3.3 rev 1 and COF 0.3.3.1 details for why this is excluded
                                # # temperature statistics

                                # # now save this value to perform statistical analysis
                                # # assume same person is person0 in frame the whole time. if we're in this loop we know that there is at least 1 person detected.
                                # forehead_stats[forehead_temps_loop] = forehead_temp
                                # forehead_temps_loop = forehead_temps_loop + 1
                                # if forehead_temps_loop >= NUM_FOREHEAD_TEMPS_PER_LOOP: 
                                #     num_std_filter = 1

                                #     avg = np.mean(forehead_stats)
                                #     std = np.std(forehead_stats)
                                    
                                #     filtered_stats = []
                                #     for temp in forehead_stats:
                                #         if avg-num_std_filter*std < temp and temp < avg+num_std_filter*std:
                                #             filtered_stats.append(temp)

                                #     filtered_avg = np.mean(filtered_stats)

                                #     if verbose:
                                #         print("forehead_stats",forehead_stats)
                                #         print("avg",avg)
                                #         print("std",std)
                                #         print("filtered_stats",filtered_stats)
                                #         print("filtered_avg",filtered_avg)
                                    
# ====================================================================================================================
# ====================================================================================================================
                                # fever detection - final module of subsys 0.3              
                                has_fever = forehead > FEVER_TEMP
# ====================================================================================================================
                                foreheads_temps[person_num] = forehead_temp,has_fever
                                cv2.putText(img_combined,"{:.2f}F".format(forehead_temp),(int(person_forehead[0]+10),int(person_forehead[1]-10)),
                                    font, scale, color, thickness, lineType)
                                if verbose:
                                    print("\nperson "+ str(person_num) +"'s forehead temperature reads: " + str(foreheads_temps[person_num][0]) + "\u00B0F\n")
                                
                                if has_fever:
                                    cv2.putText(img_combined,"FEVER",(int(person_forehead[0]+10),int(person_forehead[1])),
                                    font, scale, color, thickness, lineType)
                                    if verbose:
                                        print()
                                else:
                                    cv2.putText(img_combined,"NO FEVER",(int(person_forehead[0]+10),int(person_forehead[1])),
                                    font, scale, color, thickness, lineType)
                                    if verbose:
                                        print()
# ====================================================================================================================
                            else:
                                foreheads_temps[person_num][0] = None                        
                            
                            person_num = person_num + 1
                            
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

        cap.release()
        capth.close()
        cv2.destroyAllWindows()
