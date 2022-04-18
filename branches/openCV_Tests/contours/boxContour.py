import cv2 as cv
import numpy as np

img_ori = cv.imread("img2/plan_mauvais.jpg", cv.IMREAD_GRAYSCALE)
# img_ori = cv.blur(img_ori, (5, 5), 0)
img_ori = cv.equalizeHist(img_ori)


# ------------------------------------------------------------------------------
img_inutile, contours, hierarchy = cv.findContours(
    cv.threshold(img_ori, 60, 255, cv.THRESH_BINARY_INV)[1],
    cv.RETR_EXTERNAL,
    cv.CHAIN_APPROX_SIMPLE
)
imageContours = np.zeros_like(img_ori)
imageContours = cv.drawContours(imageContours, contours, -1, 255, 1)
imageContours = cv.GaussianBlur(imageContours, (5, 5), 0)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# img_work = cv.GaussianBlur(img_ori, (9, 9), 0)
# imageContours = np.zeros_like(img_work)
# imageContours = cv.Canny(img_work, 0, 170)
# imageContours = cv.dilate(imageContours, np.ones((9, 9), np.uint8))
# ------------------------------------------------------------------------------

perimMax = cv.arcLength(contours[0], True)
contoursMax = contours[0]

for i in contours:
    perim = cv.arcLength(i, True)
    if perim > perimMax:
        perimMax = perim
        contoursMax = i

rect = cv.minAreaRect(contoursMax)
box = cv.boxPoints(rect)
box = np.int0(box)
imageContours = cv.drawContours(imageContours, [box], 0, 127, 3)


cv.imshow("image", np.concatenate((img_ori,  imageContours), axis=1))
cv.waitKey(0)
cv.destroyAllWindows()
