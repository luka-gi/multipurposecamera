import numpy as np
import cv2
import cv2
from matplotlib import pyplot as plt

num=99
# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()


# Open both cameras
cap_right = cv2.VideoCapture(3, cv2.CAP_V4L)                    
cap_left =  cv2.VideoCapture(4, cv2.CAP_V4L)


while(cap_right.isOpened() and cap_left.isOpened()):

    succes_right, frame_right = cap_right.read()
    succes_left, frame_left = cap_left.read()

    cv2.imwrite("0l.png",frame_left)
    cv2.imwrite("0r.png",frame_right)

    frame_left = cv2.imread('0l.png',cv2.IMREAD_GRAYSCALE)
    frame_right = cv2.imread('0r.png',cv2.IMREAD_GRAYSCALE)
    stereo = cv2.StereoBM_create(numDisparities=144, blockSize=7)

    # Undistort and rectify images
    frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    cv2.imwrite("1l.png",frame_left)
    cv2.imwrite("1r.png",frame_right)
    keyCode = cv2.waitKey(30) & 0xFF 

    # power
    frame_left = np.power(frame_left,.75).astype('uint8')
    frame_right = np.power(frame_right,.75).astype('uint8')

    # imgL = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    # imgR = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)
    # stereo = cv2.StereoBM_create(numDisparities=144, blockSize=23)
    disparity = stereo.compute(frame_left,frame_right)
    print(type(disparity[0][0]))
    # print(disparity)

    # speckle filter
    disparity,_= cv2.filterSpeckles(disparity,0,4000,128-10)

    # Show the frames
    print(stereo)
    # print(disparity)
    # print(disparity[302][500])
    # print(disparity[293][1100])
    # print(disparity.astype(np.uint8))
    # disparity = 255*(disparity - disparity.min())/(disparity.max()-disparity.min())
    disparity = cv2.applyColorMap(disparity.astype(np.uint8),cv2.COLORMAP_JET)

    cv2.imshow("disp",disparity)
    cv2.imshow("frame right", frame_left) 
    cv2.imshow("frame left", frame_right)
    if keyCode == ord('s'): # wait for 's' key to save and exit
        success=cv2.imwrite('stereoLeft/imageL/' + str(num) + '.png', frame_left)
        cv2.imwrite('stereoright/imageR/' + str(num) + '.png', frame_right)
        print("images saved!")
        print(success)
        num += 1
        print(frame_right.shape)


    # Hit "q" to close the window
    if cv2.waitKey(20) & 0xFF == 27:
        break


# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()