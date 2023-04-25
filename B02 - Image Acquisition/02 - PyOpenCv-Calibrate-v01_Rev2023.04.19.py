#Import required modules
import cv2
import numpy as np
import os
import glob
import yaml
import matplotlib.pyplot as plt

# Test Name
ensayo_ID = "CalibrationImages_f"

# Storing directory
directorio_de_trabajo = "C:/Temp"

o_pth = '{0:}/{1:}'.format(directorio_de_trabajo, ensayo_ID)
os.chdir(o_pth)

# Verify if there is a directorio_de_trabajo or create if there isn't
if not os.path.exists(o_pth):
    os.makedirs(o_pth)


# Define the dimensions of checkerboard
CHECKERBOARD = (4, 8)


# stop the iteration when specified
# accuracy, epsilon, is reached or
# specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS + 
            cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Vector for 3D points
threedpoints = []

# Vector for 2D points
twodpoints = []


#  3D points real world coordinates
objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

 
# Extracting path of individual image stored
# in a given directory. Since no path is
# specified, it will take current directory
# jpg files alone
images = glob.glob('*.jpg')
  
for filename in images:
    image = cv2.imread(filename)
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
    # Find the chess board corners
    # If desired number of corners are
    # found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(
                    grayColor, CHECKERBOARD, 
                    cv2.CALIB_CB_ADAPTIVE_THRESH + 
                    cv2.CALIB_CB_FAST_CHECK + 
                    cv2.CALIB_CB_NORMALIZE_IMAGE)
  
    # If desired number of corners can be detected then,
    # refine the pixel coordinates and display
    # them on the images of checker board
    if ret == True:
        threedpoints.append(objectp3d)
  
        # Refining pixel coordinates
        # for given 2d points.
        corners2 = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)
  
        twodpoints.append(corners2)
  
        # Draw and display the corners
        image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)
  
    cv2.imshow('img', image)
    cv2.waitKey(0)
  
cv2.destroyAllWindows()
  
h, w = image.shape[:2]
  
  
# Perform camera calibration by
# passing the value of above found out 3D points (threedpoints)
# and its corresponding pixel coordinates of the
# detected corners (twodpoints)
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(threedpoints, twodpoints, grayColor.shape[::-1], None, None)



# Exporting Parameters
# transform the matrix and distortion coefficients to writable lists
data = {'ret'           : np.asarray(ret       ).tolist(),
        'camera_matrix' : np.asarray(matrix    ).tolist(),
        'dist_coeff'    : np.asarray(distortion).tolist(),
        'r_vecs'        : np.asarray(r_vecs    ).tolist(),
        't_vecs'        : np.asarray(t_vecs    ).tolist()}





# and save it to a file
with open("calibration_matrix.yaml", "w") as f:
    yaml.dump(data, f)




# Methods for storing the calibration parameters in a file for future use
# Method 01 - Save the parameters
def saveMatrices(A,B,C,D, fileName):
    with open(fileName, 'wb') as f:
        np.save(f, A)
        np.save(f, B)
        np.save(f, C)
        np.save(f, D)


# Method 02 - Loading stored parameters
def loadMatrices(fileName):
    with open(fileName, 'rb') as f:
        A = np.load(f)
        B = np.load(f)
        C = np.load(f)
        D = np.load(f)
    return (A,B,C,D)


# ------------- Testing the Methods
saveMatrices(matrix, distortion, r_vecs, t_vecs, "calibrationParameters.npy")

mtx, dist, rv, tv = loadMatrices("calibrationParameters.npy")

# Displaying required output
print(" Camera matrix:")
print(matrix)
  
print("\n Distortion coefficient:")
print(distortion)
  
print("\n Rotation Vectors:")
print(r_vecs)
  
print("\n Translation Vectors:")
print(t_vecs)






# ==============================================

# Import a distorted image
distortedImage = cv2.imread(images[1])

# Undistort the image
undistortedImage = cv2.undistort(distortedImage, mtx, dist, None, None)

# Crop the image. Uncomment these two lines to remove black lines
# on the edge of the undistorted image.
#x, y, w, h = roi
#undistorted_image = undistorted_image[y:y+h, x:x+w]

f1, ax = plt.subplots(1,2)
ax[0].imshow(distortedImage)
ax[1].imshow(undistortedImage)
plt.show()