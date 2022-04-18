import cv2 as cv
import numpy as np

img_ori = cv.imread("img2/surex.jpg", cv.IMREAD_GRAYSCALE)
# img_ori = cv.blur(img_ori, (5, 5), 0)
img_ori = cv.equalizeHist(img_ori)


def hist1():
    clahe = cv.createCLAHE(clipLimit=4.0, tileGridSize=(16, 16))
    return clahe.apply(img_ori)


def contour4():
    ret, img = cv.threshold(img_ori, 60, 255, cv.THRESH_BINARY_INV)
    img_inutile, contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL,
                                                       cv.CHAIN_APPROX_SIMPLE)
    imageContours = np.zeros_like(img)
    imageContours = cv.drawContours(imageContours, contours, -1, 255, 1)
    # imageContours = cv.GaussianBlur(imageContours, (5, 5), 0)
    # imageContours = cv.dilate(imageContours, np.ones((5,5),np.uint8))
    # ret, imageContours = cv.threshold(imageContours, 30, 255, cv.THRESH_BINARY)
    return imageContours


def contour4b():
    ret, img = cv.threshold(img_ori, 60, 255, cv.THRESH_BINARY_INV)
    img_inutile, contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL,
                                                       cv.CHAIN_APPROX_SIMPLE)
    imageContours = np.zeros_like(img)
    imageContours = cv.drawContours(imageContours, contours, -1, 255, 1)
    imageContours = cv.GaussianBlur(imageContours, (5, 5), 0)
    # imageContours = cv.dilate(imageContours, np.ones((5,5),np.uint8))
    # ret, imageContours = cv.threshold(imageContours, 30, 255, cv.THRESH_BINARY)
    return imageContours


def contour2():
    img_work = cv.GaussianBlur(img_ori, (9, 9), 0)
    imageContours = np.zeros_like(img_work)
    imageContours = cv.Canny(img_work, 0, 160)
    # imageContours = cv.GaussianBlur(imageContours, (5, 5), 0)
    return imageContours


def contour1():
    imageContours = cv.GaussianBlur(img_ori, (5, 5), 0)
    dst = cv.Laplacian(img_ori, cv.CV_16S, ksize=1)
    imageContours = cv.convertScaleAbs(dst)
    return imageContours


def contour3():
    delta = 0
    scale = 1
    grad_x = cv.Sobel(img_ori, cv.CV_16S, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(img_ori, cv.CV_16S, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad


numpy_vertical = np.vstack((np.concatenate((img_ori,  contour1(), contour2()), axis=1),
                           np.concatenate((contour3(), contour4(), contour4b()), axis=1)))
cv.imshow("image", numpy_vertical)
cv.waitKey(0)
cv.destroyAllWindows()
