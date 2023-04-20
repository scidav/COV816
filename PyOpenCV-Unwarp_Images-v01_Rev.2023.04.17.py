# -*- coding: utf-8 -*-
"""
Author:    Irving D. Hernández
Filiation: NEO-COPPE/UFRJ
Version: 1 >> 2023-04-17 22:07:50.234 (Brasil)
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np


def unwarp(img, src, dst, testing):
    h, w = img.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    M = cv2.getPerspectiveTransform(src, dst)
    # use cv2.warpPerspective() to warp your image to a top-down view
    correctedColor = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    warped = cv2.warpPerspective(correctedColor, M, (w, h), flags=cv2.INTER_LINEAR)

    if testing:
        f1, ax= plt.subplots(1, 2, figsize=(12, 6), constrained_layout = True)
        # f1.subplots_adjust(hspace=.2, wspace=.05)
        ax[0].imshow(correctedColor)
        x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
        y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
        ax[0].plot(x, y, color='lime', alpha=0.8, linewidth=3, solid_capstyle='round')
        ax[0].set_ylim([h, 0])
        ax[0].set_xlim([0, w])
        ax[0].set_title('Original Image', fontsize=15)
        ax[1].imshow(warped)#cv2.flip(warped, 1))
        ax[1].set_title('Unwarped Image', fontsize=15)
        for i in range(2):
            ax[i].grid(c="k", ls=":")
            # ax[i].set_xticks(range(0,w,50))
            # ax[i].set_yticks(range(0,h,50))
            ax[i].set_xlabel("Horizontal Pixels", fontsize=13)
            ax[i].set_ylabel("Vertical Pixels"  , fontsize=13)
        print(M)
        plt.show()
        
    else:
        return warped, M
    


# ==================================================================
inputImage = cv2.imread("myImage3.jpg")

# We will first manually select the source points 
# we will select the destination point which will map the source points in
# original image to destination points in unwarped image
src = np.float32([(144, 276),
                  (79, 116),
                  (241, 241),
                  (166, 92)
                  ])



height, width= 180, 100
delta = 50

dst = np.float32([(delta,              delta),
                  (delta+height,        delta),
                  (delta,       width+delta),
                  (delta+height, width+delta)])

# dst = np.float32([(delta,              delta),
#                   (delta+width,        delta),
#                   (delta,       height+delta),
#                   (delta+width, height+delta)])


unwarp(inputImage, src, dst, True)

# cv2.imshow("myImage", inputImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
