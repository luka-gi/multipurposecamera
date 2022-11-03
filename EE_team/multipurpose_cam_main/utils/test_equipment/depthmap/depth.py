import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
imgL = cv.imread('./stereoLeft/imageL/0.png',cv.IMREAD_GRAYSCALE)
imgR = cv.imread('./stereoright/imageR/0.png',cv.IMREAD_GRAYSCALE)
stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
d = stereo.compute(imgL,imgR)
print(d)
plt.imshow(d)
plt.show()

