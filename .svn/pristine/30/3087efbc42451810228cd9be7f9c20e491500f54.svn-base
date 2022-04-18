import cv2 as cv
import numpy as np

img_ori = cv.imread("img2/plan_mauvais.jpg", cv.IMREAD_GRAYSCALE)
# img_ori = cv.blur(img_ori, (5, 5), 0)
img_ori = cv.resize(img_ori, (320, 240))
img_ori = cv.equalizeHist(img_ori)


def contour2(param):
    img_work = cv.GaussianBlur(img_ori, (9, 9), 0)
    imageContours = np.zeros_like(img_work)
    imageContours = cv.Canny(img_work, 0, 160, param)
    # imageContours = cv.GaussianBlur(imageContours, (5, 5), 0)
    return imageContours


def hough(param):
    imageContours = np.zeros_like(img_ori)
    cont = contour2(param)
    cont = cv.dilate(cont, np.ones((param, param), np.uint8))
    cv.imshow("image", np.concatenate((img_ori, cont), axis=1))
    cv.waitKey(0)
    minLineLength = 20
    maxLineGap = 10
    lines = cv.HoughLinesP(cont, 1, np.pi/180, 180, minLineLength, maxLineGap)
    if lines is None:
        return imageContours
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(imageContours, (x1, y1), (x2, y2), 127, 4)
    return imageContours


i = 1
while i < 10:
    # cv.imshow("image", np.concatenate((img_ori, contour2(i)), axis=1))
    # cv.waitKey(0)
    cv.imshow("image", np.concatenate((img_ori, hough(i)), axis=1))
    cv.moveWindow("image", 20, 20)
    if cv.waitKey(0) == ord('q'):
        cv.destroyAllWindows()
        break
    cv.destroyAllWindows()
    i += 2
