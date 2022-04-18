import cv2
import sys
import numpy

N=5
import cv2
import numpy
imageOriginale = cv2.imread("plan.jpg", cv2.IMREAD_COLOR);
img_gray = cv2.cvtColor(imageOriginale, cv2.COLOR_BGR2GRAY)
img=cv2.resize(img_gray, (9, 9))
img2=numpy.round(img_gray*(N/255))*(255/N)

cv2.imwrite("quantification_5.png", numpy.round(img2, decimals=-1))
