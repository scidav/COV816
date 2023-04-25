import numpy as np
import cv2 as cv
from datetime import datetime
import time
import os


# Calibration file directory
calibrationPath = "C:/Temp/CalibrationImages_old"
os.chdir(calibrationPath)

# Method 02 - Loading stored parameters
def loadMatrices(fileName):
    with open(fileName, 'rb') as f:
        A = np.load(f)
        B = np.load(f)
        C = np.load(f)
        D = np.load(f)
    return (A,B,C,D)

mtx, dist, rv, tv = loadMatrices("calibrationParameters.npy")



# Camera configuration
cap = cv.VideoCapture(1, cv.CAP_DSHOW) # this is the magic!
hres,vres = 1280, 720
cap.set(cv.CAP_PROP_FRAME_WIDTH, hres)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,vres)


if not cap.isOpened():
    print("Não é possível mostrar a camera")
    exit()

contador = 0

# Image acquisition
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("No es posible retener algun Frame (Finalizar transmisión?). Saliendo ...")
        break
    #
    # Mostrar a imagen capturada
    sf = 0.3
    dImage  = frame
    uImage  = cv.undistort(dImage, mtx, dist, None, None)
    dIma_r  = cv.resize(dImage, (int(sf*hres),int(sf*vres)))
    uIma_r  = cv.resize(uImage, (int(sf*hres),int(sf*vres)))
    cv.imshow('Imagen Capturada', np.hstack([dIma_r,uIma_r]))
    # =====================
    time.sleep(0.1)
    # =====================
    if cv.waitKey(1) == ord('q'):
        break

# Cuando todo esté listo, liberar camara y cerrar todas las ventanas
cap.release()
cv.destroyAllWindows()
