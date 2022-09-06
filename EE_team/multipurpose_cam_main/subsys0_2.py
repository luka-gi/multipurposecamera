import cv2
import sys
import numpy as np
from time import time
from stereovision.calibration import StereoCalibration
sys.path.insert(0,"./utils/test_equipment/StereoVision/main_scripts")
sys.path.insert(0,"./utils/test_equipment")
depthmap = __import__("5_depthmap")
from modified_start_cameras import Start_Cameras

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
            print("\ncamera capture: success")
    else:
        if verbose:
            print("\ncamera capture: failure")
    return img

def run(displaymode,verbose,run_openpose,write_images,openpose_device_id):
    args = (displaymode,verbose,run_openpose,write_images,openpose_device_id)

    cap = Start_Cameras(openpose_device_id).start()
    cap2 = Start_Cameras(stereo_device_right).start()

    opWrapper = op.WrapperPython()
    opWrapper.configure({"model_folder":openpose_build_path + "/../models/"})
    opWrapper.start()

    depthmap.load_map_settings("./stereo_calibration_data/3dmap_set.txt")

    key = 0

    while key != ord('q'):
        datum = op.Datum()
# ====================================================================================================================
                # obtaining the depth map
        time_cap_in = time()
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
        time_cap_fi = time()
# ====================================================================================================================
                
        if run_openpose:

            time_comp_in = time()
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            time_comp_fi = time()

            if write_images:
                cv2.imwrite(image_path+"op.png",datum.cvOutputData)
# ====================================================================================================================
            # lifting all of the keypoints to 3D based on the depthmap readings
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
                        
                if verbose:
                    print("coordinates of 3D lifted people")
                    print(people_3D)
# ====================================================================================================================
# ====================================================================================================================
                # now we can iterate through to determine distances between people
                num_people = len(datum.poseKeypoints)
                # create a matrix so that mat[p0][p1] refers to distance from p0 to p1
                depth_pairs = []
                # body_25 model point which labels the torso of a person
                torso_keypoint = 1
                for person1 in range(num_people):
                    depth_pair = []
                    for person2 in range(num_people):
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

                font = cv2.FONT_HERSHEY_COMPLEX
                scale = 1
                color = (255,255,255)
                thickness = 1
                lineType = 2

                for person1 in range(num_people):
                    for person2 in range(num_people):
                        if person1 > person2:
                            distance_between = depth_pairs[person1][person2]
                            (X0,Y0,Z0) = people_3D[person1][torso_keypoint]
                            (X1,Y1,Z1) = people_3D[person2][torso_keypoint]
                            cv2.line(imageToProcess,(int(X0),int(Y0)),(int(X1),int(Y1)),(255,0,0),5)
                            cv2.putText(imageToProcess,"{}cm".format(depth_pairs[person1][person2]),(int((X0+X1)/2),int((Y0+Y1)/2)),
                                    font, scale, color, thickness, lineType)
# ====================================================================================================================
        if verbose:
            print("Body keypoints: \n" + str(datum.poseKeypoints))
        # Display Image
        if displaymode: 
            if run_openpose: 
                time_show_in = time()        
                cv2.imshow("output display",imageToProcess)                
                time_show_fi = time()
            else:
                cv2.imshow("output display",imageToProcess)

            (H, W, C) = stereo_image.shape
            #due to camera aspect ratio reshaping in the capture stage
            #we must consider that the image undistortion stage will try to fix this
            #so most of the disparity map is blank and only has output to the actual capture resolution
            x_offset = 0
            y_offset = 47

            if verbose:
                print("disparitymap shape:",disparity_color.shape)
                print("stereo image shape:",stereo_image.shape)

            disparity_color = disparity_color[y_offset:y_offset+H,x_offset:x_offset+W]

            cv2.imshow("stereo_display",stereo_image)
            output = cv2.addWeighted(stereo_image, 0.5, disparity_color, 0.5, 0.0)
            cv2.imshow("DepthMap", output)

            if verbose:
                delay_cap = time_cap_fi-time_cap_in                        

                print("   TIMES:") 
                print("\tCAP TIMES:")
                print("\t\tSTEREO CAP:",delay_cap)
                if run_openpose:
                    delay_show = time_show_fi-time_show_in
                    delay_comp = time_comp_fi-time_comp_in
                    print("\tCOMP TIMES:")
                    print("\t\tSTEREO COMP:",delay_comp)
                    print("\tSHOW TIMES:")
                    print("\t\tSTEREO SHOW:",delay_show)
                print("\tSINGLE CYCLE DELAY:")
                if run_openpose:
                    print("\t\tTOTAL STEREO DELAY:",delay_cap+delay_comp+delay_show)
                else:
                    print("\t\tTOTAL STEREO DELAY:",delay_cap)
            key = cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()