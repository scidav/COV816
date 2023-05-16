# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
basePath = r""


os.chdir(basePath)

import glob
fname = glob.glob1(os.getcwd(),'**.mp4')[0]

print('Video {0:} was detected in the directory.'.format(fname))


import cv2
import numpy as np

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)




# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(fname)
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
 
    # Display the resulting frame
    blur = cv2.blur(frame,(5,5))
    blur0= cv2.medianBlur(blur,5)
    blur1= cv2.GaussianBlur(blur0,(5,5),0)
    frame2= cv2.bilateralFilter(blur1,9,75,75)
    
    hsv = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    low_blue = np.array([25, 0, 0])
    high_blue = np.array([255, 150, 255])
    mask = cv2.inRange(hsv, low_blue, high_blue)
    
    resize = ResizeWithAspectRatio(mask, width=640)
    
    cv2.imshow('Frame',resize)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()