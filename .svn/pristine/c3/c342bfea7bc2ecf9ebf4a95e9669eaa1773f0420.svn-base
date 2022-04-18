import cv2
import numpy as np
import time
from bench_decorateur import benchmark


@benchmark("PC", "plan.jpg")
def calculer_angle(img, pourcentage_split=0.5):
    size = len(img)
    ligne_split = int(size * pourcentage_split)

    im2, contours, hierarchy = cv2.findContours(img[0:ligne_split],
                                                cv2.RETR_EXTERNAL, 2)
    rect0 = cv2.minAreaRect(contours[0])
    box = np.int0(cv2.boxPoints(rect0))
    img = cv2.drawContours(img, [box], 0, 127, 1)

    im2, contours, hierarchy = cv2.findContours(img[ligne_split:size],
                                                cv2.RETR_EXTERNAL, 2)
    rect1 = cv2.minAreaRect(contours[0])
    (cx, cy), size, angle = rect1
    rect1 = (cx, cy + ligne_split), size, angle
    box = np.int0(cv2.boxPoints(rect1))
    img = cv2.drawContours(img, [box], 0, 127, 1)

    return (rect0[2], rect1[2], img)


calculer_angle()
