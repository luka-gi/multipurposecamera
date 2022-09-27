import picamera
import picamera.array
import numpy as np
# Capture image
print("Capturing image...")
with picamera.PiCamera() as camera:
    with picamera.array.PiBayerArray(camera) as stream:
        camera.capture(stream, 'jpeg', bayer=True)
        # Demosaic data and write to rawimg
        # (stream.array contains the non-demosaiced data)
        rawimg = stream.demosaic()