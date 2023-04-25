import cv2
import os
import numpy as np
from datetime import datetime
import time

# Test Name
ensayo_ID = "CalibrationImages_f"

# Storing directory
workingDirectory = "C:/Temp"
os.chdir(workingDirectory)

o_pth = '{0:}/{1:}'.format(workingDirectory, ensayo_ID)

# Verify if there is a directorio_de_trabajo or create if there isn't
if not os.path.exists(o_pth):
    os.makedirs(o_pth)


cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
hres,vres = 1280, 720
cam.set(cv2.CAP_PROP_FRAME_WIDTH, hres)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,vres)

cv2.namedWindow("Image Viewer")

img_counter = 0


while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Image Viewer", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        # =====================
        # Get current time
        now = datetime.now()
        # Add the desired string format to the current time
        current_time = now.strftime('%Y-%m-%d_%H.%M.%S.%f')[:-3]
        # Sve the frame to the working directory
        cv2.imwrite(o_pth+'/{0:}_{2:}_{1:}.jpg'.format(ensayo_ID,current_time,str(img_counter).zfill(5)), frame)
        print("Image {0:03} written!".format(img_counter))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()