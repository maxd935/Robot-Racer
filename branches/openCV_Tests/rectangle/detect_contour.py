import cv2
import numpy as np
from sys import argv

IMAGES = [
    "img.jpg",
    "plan.jpg",
    "plan_mauvais.jpg",
    "coupure.jpg"
]

tailleImage = (64, 48)
tailleFenetre = (600, 600)


def calculer_angle(img, pourcentage_split=0.5):
    size = len(img)
    ligne_split = int(size * (pourcentage_split if len(argv) <= 1 else float(argv[1])))
    rect0 = (0, 0, 0)
    rect1 = (0, 0, 0)

    im2, contours, hierarchy = cv2.findContours(img[0:ligne_split], cv2.RETR_EXTERNAL, 2)
    if contours:
        rect0 = cv2.minAreaRect(contours[0])
        box = np.int0(cv2.boxPoints(rect0))
        img = cv2.drawContours(img, [box], 0, 127, 1)

    im2, contours, hierarchy = cv2.findContours(img[ligne_split:size], cv2.RETR_EXTERNAL, 2)
    if contours:
        rect1 = cv2.minAreaRect(contours[0])
        (cx, cy), size, angle = rect1
        rect1 = (cx, cy + ligne_split), size, angle
        box = np.int0(cv2.boxPoints(rect1))
        img = cv2.drawContours(img, [box], 0, 127, 1)

    return (rect0[2], rect1[2])


cap = cv2.VideoCapture(0)
cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)

def afficher(img):
    # C'est parti !
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, tailleImage)
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    angle1, angle2 = calculer_angle(img, 0.3)

    cv2.imshow('fenetreImage', img)
    cv2.waitKey(0)

for image in IMAGES:
    afficher(image)

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
