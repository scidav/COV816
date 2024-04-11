# -*- coding: utf-8 -*-
"""
Author:    Irving D. Hernández
Filiation: NEO-COPPE/UFRJ
Version: 2-B >> 2024-04-11 00:07:50.234 (Brasil)
"""

import numpy as np
import cv2 as cv
from datetime import datetime
import time
import os

# Test Name
ensayo_ID = "TestName"

# Storing directory
directorio_de_trabajo = "C:/COV816"
os.chdir(directorio_de_trabajo)

o_pth = '{0:}/{1:}'.format(directorio_de_trabajo, ensayo_ID)

# Verify if there is a directorio_de_trabajo or create if there isn't
if not os.path.exists(o_pth):
    os.makedirs(o_pth)

# # Comunication parameters
# cap = cv.VideoCapture(1)


cap = cv.VideoCapture(0, cv.CAP_DSHOW) # this is the magic!
hres,vres = 1280, 720
cap.set(cv.CAP_PROP_FRAME_WIDTH, hres)
cap.set(cv.CAP_PROP_FRAME_HEIGHT,vres)


if not cap.isOpened():
    print("Não é possível mostrar a camera")
    exit()

contador = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("No es posible retener algun Frame (Finalizar transmisión?). Saliendo ...")
        break
    #
    # # Exemplos de operações de cores na imagem
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # color_RGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    #=================== EXAMPLE 01 ==============================
    # # Filtering a colored marker by HSL color
    # hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # #:> define range of blue color in HSV
    # lower_bound = np.array([100, 150, 150])
    # upper_bound = np.array([254,254,254])
    # #:>Threshold the HSV image to get only blue colors
    # mask = cv.inRange(hsv, lower_bound, upper_bound)
    # #:>Bitwise-AND mask and original image
    # res = cv.bitwise_and(frame,frame, mask= mask)
    #==============================================================
    # Mostrar a imagen capturada
    sf = 0.5
    frm = frame
    frame_r = cv.resize(frm, (int(sf*hres),int(sf*vres)))
    cv.imshow('Imagen Capturada', frame_r)
    # =====================
    # obter tempo instantâneo
    now = datetime.now()
    # formatação do tempo instantâneo em formato string
    current_time = now.strftime('%Y-%m-%d_%H.%M.%S.%f')[:-3]
    #
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img = cv.cvtColor(img,   cv.COLOR_RGB2BGR)
    
    # Use a seguinte linha se for necessário salvar as imagens sem compressão
    # cv2.imwrite(o_pth+'/{0:}_{1:}.png'.format(ensayo_ID,current_time), img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    # ----------------
    # Use a seguinte linha se for necessário salvar imagens com compactação automática
    # cv.imwrite(o_pth+'/{0:}_{2:}_{1:}.jpg'.format(ensayo_ID,current_time,str(contador).zfill(5)), img)
    contador += 1
    # Use a linha a seguir se for necessário condicionar uma taxa de imposto mais lenta/mais rápida
    time.sleep(0.1)
    # =====================
    if cv.waitKey(1) == ord('q'):
        break

# Cuando todo esté listo, liberar camara y cerrar todas las ventanas
cap.release()
cv.destroyAllWindows()
