import cv2
import os
import numpy as np

# Test Name
ensayo_ID = "CalibrationImages"

# Storing directory
directorio_de_trabajo = "C:/Temp"
os.chdir(directorio_de_trabajo)

o_pth = '{0:}/{1:}'.format(directorio_de_trabajo, ensayo_ID)

# Verify if there is a directorio_de_trabajo or create if there isn't
if not os.path.exists(o_pth):
    os.makedirs(o_pth)






cam = cv2.VideoCapture(0, cv.CAP_DSHOW)
hres,vres = 1280, 720
cap.set(cv.CAP_PROP_FRAME_WIDTH, hres)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,vres)

cv2.namedWindow("Image Viewer")

img_counter = 0


while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()