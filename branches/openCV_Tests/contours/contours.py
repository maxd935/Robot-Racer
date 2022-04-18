import cv2 as cv
import numpy as np
from bench_decorateur import benchmark

@benchmark("PC", "img2/plan.jpg")
def toLine(img_ori):
    img_ori = cv.equalizeHist(img_ori)

    img_inutile, contours, hierarchy = cv.findContours(
        cv.threshold(img_ori, 60, 255, cv.THRESH_BINARY_INV)[1],
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )
    imageContours = np.zeros_like(img_ori)
    imageContours = cv.drawContours(imageContours, contours, -1, 255, 1)
    imageContours = cv.GaussianBlur(imageContours, (5, 5), 0)

    # imageLigne = np.zeros_like(img_ori)
    lines = cv.HoughLinesP(imageContours, 1, np.pi / 180, 180, 1, 150)

    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv.line(imageLigne, (x1, y1), (x2, y2), 127, 4)

    # return imageLigne

toLine()
