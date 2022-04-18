import cv2 as cv
import numpy as np

img_ori = cv.imread("img2/plan.jpg", cv.IMREAD_GRAYSCALE)
# img_ori = cv.blur(img_ori, (5, 5), 0)
img_ori = cv.equalizeHist(img_ori)


def hist1():
    clahe = cv.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    return clahe.apply(img_ori)


cv.imshow("image", np.concatenate((img_ori, hist1(), cv.equalizeHist(img_ori)), axis=1))
cv.waitKey(0)
cv.destroyAllWindows()
