import cv2 as cv
import numpy as np

img_ori = cv.imread("img2/plan.jpg", cv.IMREAD_GRAYSCALE)
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


def hough():
    imageLigne = np.zeros_like(img_ori)
    longueur_min = 1
    gap = 150
    lines = cv.HoughLinesP(imageContours, 1, np.pi / 180, 180, longueur_min, gap)

    if lines is None:
        return imageContours
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(imageLigne, (x1, y1), (x2, y2), 127, 4)

    return imageLigne


cv.imshow("image", np.concatenate((img_ori,  hough()), axis=1))
cv.waitKey(0)
cv.destroyAllWindows()
