import cv2
import numpy as np

tailleImage = (32, 24)
tailleFenetre = (600, 600)
secondPointY = 0.6
quantification = 255

cap = cv2.VideoCapture(0)
cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)


def skeletize(img):
    skeleton = np.zeros(img.shape, np.uint8)
    eroded = np.zeros(img.shape, np.uint8)
    temp = np.zeros(img.shape, np.uint8)

    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (6, 6))

    while(True):
        cv2.erode(img, element, eroded)
        cv2.dilate(eroded, element, temp)
        cv2.subtract(img, temp, temp)
        cv2.bitwise_or(skeleton, temp, skeleton)
        img, eroded = eroded, img  # Swap instead of copy

        if cv2.countNonZero(img) == 0:
            return skeleton


# C'est parti !
img = cv2.imread("coupure.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, tailleImage)
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
img = skeletize(img)
cv2.imshow('fenetreImage', img)
cv2.waitKey(0)

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
