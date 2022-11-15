import cv2
import sys
import time
import numpy as np
from flirpy.camera.lepton import Lepton
from scipy.ndimage import interpolation
from stereovision.calibration import StereoCalibration
sys.path.insert(0,"./utils/test_equipment/StereoVision/main_scripts")
sys.path.insert(0,"./utils/test_equipment")
depthmap = __import__("5_depthmap")
from modified_start_cameras import Start_Cameras

# number to multiply raw thermal data
THERMAL_CALIBRATION_CONSTANT = 0.00995
# a feverish temperature to use as a threshold. right not this is in degrees F
FEVER_TEMP = 100

thermal_device_id = 2
# IMG_BUFFER_DISCARD = 1
CAP_BUFFER_SIZE = 1

#for writing on the images, we will use these to define the style
font = cv2.FONT_HERSHEY_COMPLEX
scale = 1
color = (255,255,255)
thickness = 1
lineType = 2

    # the following comments assume subject is about 0.5 m from camera
    #particular to line up the termal image:
x_offset_thermal = 285 #the following values were experimentally obtained
y_offset_thermal = 105 #seems to work on left camera with respective values:
x_scale_thermal = 5.65    #280,160,6,4
y_scale_thermal = 4.5
    # and to line up the depth map:
x_offset_depth = 0
y_offset_depth = 47

#venv paths
NVIDIA_python2_path = "/usr/bin/python"
cam_img_cap = "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/multipurpose_cam_main/utils/cam_img_cap.py"
stereo_device_right = 4

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
    cap = Start_Cameras(openpose_device_id).start()
    cap2 = Start_Cameras(stereo_device_right).start()

    if run_openpose:
        opWrapper = op.WrapperPython()
        opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
        opWrapper.start()

    depthmap.load_map_settings("./stereo_calibration_data/3dmap_set.txt")

    key = 0

    while key != ord('q'):
# ====================================================================================================================
                # obtaining the depth map
        datum = op.Datum()

        time_imcap_th_be = time.time()
        thermalImageToProcess,tempmap = capture_thermal_img(capth, image_path+"liveth.png", *args)
        #get simultaneous images
        time_imcap_th_fi = time.time()
        time_imcap_st_be = time.time()
        #get simultaneous images
        imageToProcess = capture_img(cap, image_path+"live.png", *args)
        stereo_image = capture_img(cap2, image_path+"live2.png", *args)
        #convert grayscale
        left_gray_frame = cv2.cvtColor(imageToProcess, cv2.COLOR_BGR2GRAY)
        right_gray_frame = cv2.cvtColor(stereo_image, cv2.COLOR_BGR2GRAY)
        #calibration config input
        calibration = StereoCalibration(input_folder='./stereo_calibration_data/calib_result')
        #obtain disparity info
        rectified_pair = calibration.rectify((left_gray_frame, right_gray_frame))
        disparity_color, disparity_normalized = depthmap.stereo_depth_map(rectified_pair)
        time_imcap_st_fi = time.time()
# ====================================================================================================================


        if run_openpose:

            time_comp_st_be=time.time()
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            time_comp_st_fi=time.time()

            if write_images:
                cv2.imwrite(image_path+"op.png",datum.cvOutputData)
# ====================================================================================================================
            # forehead detection and lifting all of the keypoints to 3D based on the depthmap readings

            # if people detected, calculate their eyes/nose. use this to calculate forehead
            if datum.poseKeypoints is not None:
                people_3D = []
                for person in range(len(datum.poseKeypoints)):
                    person3D = []                  
                    for keypoint in range(len(datum.poseKeypoints[person])):
                        (X,Y,confidence) = datum.poseKeypoints[person][keypoint]
                        #this is the default value if keypoint is not detected
                        if(X == 0 and Y == 0):
                            Z = 0
                        else:
                            Z = disparity_normalized[int(Y)][int(X)]
                        # the Z value is in centimeters by default
                        person3D.append([X,Y,Z])
                    people_3D.append(person3D)
                people_3D = np.array(people_3D)

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
                # now we can iterate through to determine distances between people
                # create a matrix so that mat[p0][p1] refers to distance from p0 to p1
                depth_pairs = []
                # body_25 model point which labels the torso of a person
                torso_keypoint = 1
                for person1 in range(len(datum.poseKeypoints)):
                    depth_pair = []
                    for person2 in range(len(datum.poseKeypoints)):
                        # if person or equal or keypoint (chest) is not detected on either person, skip the calculation
                            # failsafe distance: 0
                        if (person1 == person2) or (people_3D[person1][torso_keypoint] == [0,0,0]).all() or (people_3D[person2][torso_keypoint] == [0,0,0]).all():
                            distance_between = 0
                        else:
                            distance_between = abs(people_3D[person1][torso_keypoint][2] - people_3D[person2][torso_keypoint][2])
                        depth_pair.append(distance_between)
                    depth_pairs.append(depth_pair)
                depth_pairs = np.array(depth_pairs)

                if verbose:
                            print("matrix of pairs of people and distances between")
                            print(depth_pairs)
# ====================================================================================================================

# ====================================================================================================================
        if verbose:
            print("coordinates of 3D lifted people")
            print(people_3D)
            print("Body keypoints: \n" + str(datum.poseKeypoints))
       
        
        # Display Image
        if displaymode: 
            if run_openpose:
                time_show_be = time.time() 
                img_combined = datum.cvOutputData 

                thermalImageToProcess = cv2.resize(thermalImageToProcess,(int(thermalImageToProcess.shape[1]*x_scale_thermal),int(thermalImageToProcess.shape[0]*y_scale_thermal))) 
                tempmapscaled = interpolation.zoom(tempmap,[y_scale_thermal,x_scale_thermal])

                if verbose:                         
                    print("stereo img shape",img_combined.shape)
                    print("thermal img shape",thermalImageToProcess.shape)
                    print("tempmap scaled shape", tempmapscaled.shape)

                thermalImageToProcess = cv2.addWeighted(img_combined[y_offset_thermal:y_offset_thermal+thermalImageToProcess.shape[0],x_offset_thermal:x_offset_thermal+thermalImageToProcess.shape[1]],0.35,thermalImageToProcess,0.65,0.0)
                img_combined[y_offset_thermal:y_offset_thermal+thermalImageToProcess.shape[0],x_offset_thermal:x_offset_thermal+thermalImageToProcess.shape[1]] = thermalImageToProcess
                                    
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
                        if (x_offset_thermal < forehead[0] and forehead[0] < x_offset_thermal + thermalImageToProcess.shape[1] and y_offset_thermal < forehead[1] and forehead[1] < y_offset_thermal + thermalImageToProcess.shape[0]):
                            

                            forehead_temp = tempmapscaled[int(person_forehead[1]-y_offset_thermal),int(person_forehead[0]-x_offset_thermal)]
# ====================================================================================================================
                            # fever detection - final module of subsys 0.3              
                            has_fever = forehead_temp > FEVER_TEMP
# ====================================================================================================================
                            foreheads_temps[person_num] = forehead_temp,has_fever
                            cv2.putText(img_combined,"{:.2f}F".format(forehead_temp),(int(person_forehead[0]+10),int(person_forehead[1]-10)),
                                font, scale, color, thickness, lineType)
                    
                            if verbose:
                                print("\nperson "+ str(person_num) +"'s forehead temperature reads: " + str(foreheads_temps[person_num][0]) + "\u00B0F\n")
                            
                            if has_fever:
                                cv2.putText(img_combined,"FEVER",(int(person_forehead[0]+20),int(person_forehead[1]+20)),
                                font, scale, color, thickness, lineType)
                                if verbose:
                                    print()
                            else:
                                cv2.putText(img_combined,"NO FEVER",(int(person_forehead[0]+20),int(person_forehead[1]+20)),
                                font, scale, color, thickness, lineType)
                                if verbose:
                                    print()
# ====================================================================================================================
                        else:
                            foreheads_temps[person_num][0] = None                        
                        
                        person_num = person_num + 1

                    for person1 in range(len(datum.poseKeypoints)):
                        for person2 in range(len(datum.poseKeypoints)):
                            if person1 > person2:
                                distance_between = depth_pairs[person1][person2]
                                (X0,Y0,Z0) = people_3D[person1][torso_keypoint]
                                (X1,Y1,Z1) = people_3D[person2][torso_keypoint]
                                cv2.line(img_combined,(int(X0),int(Y0)),(int(X1),int(Y1)),(255,0,0),5)
                                cv2.putText(img_combined,"{}cm".format(depth_pairs[person1][person2]),(int((X0+X1)/2),int((Y0+Y1)/2)),
                                        font, scale, color, thickness, lineType)
                                        
                (H, W, C) = stereo_image.shape
                #due to camera aspect ratio reshaping in the capture stage
                #we must consider that the image undistortion stage will try to fix this
                #so most of the disparity map is blank and only has output to the actual capture resolution
                disparity_color = disparity_color[y_offset_depth:y_offset_depth+H,x_offset_depth:x_offset_depth+W]
                output = cv2.addWeighted(img_combined, 0.75, disparity_color, 0.25, 0.0)

                cv2.imshow("output display",output)

                time_show_fi = time.time()

                if verbose:
                    print("disparitymap shape:",disparity_color.shape)
                    print("stereo image shape:",stereo_image.shape)
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

                thermalImageToProcess = cv2.resize(thermalImageToProcess,(int(thermalImageToProcess.shape[1]*x_scale_thermal),int(thermalImageToProcess.shape[0]*y_scale_thermal))) 
                if verbose: 
                    print("stereo img shape",img_combined.shape)
                    print("thermal img shape",thermalImageToProcess.shape)

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
    cap2.release()
    capth.close()
    cv2.destroyAllWindows()
