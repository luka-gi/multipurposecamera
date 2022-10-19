import cv2
import numpy as np
import time
from flirpy.camera.lepton import Lepton
n=0.00995
m=(9/5)
with Lepton() as camera:
    while True:
        img = camera.grab().astype(np.float32)

        #  =================================
        # print(type(n))
        # print(type(img))
        # img = np.multiply(img,n)
        # img = img - 273.15
        # img = np.multiply(img,m) +32
        # #Rescale to 8 bit
        imagenorm = 255*(img - img.min())/(img.max()-img.min())
        # ===========================
        print(img)
        time.sleep(0.5)
        img = cv2.applyColorMap(imagenorm.astype(np.uint8),cv2.COLORMAP_INFERNO)
        cv2.imshow("s",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    





