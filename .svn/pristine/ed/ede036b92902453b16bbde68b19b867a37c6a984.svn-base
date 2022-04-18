import cv2
import numpy as np

tailleImage = (32, 24)
tailleFenetre = (600, 600)
secondPointY = 0.6
quantification = 255

cap = cv2.VideoCapture(0)
cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)
img = cv2.imread("surex.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, tailleImage)
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

size = np.size(img)
skel = np.zeros(img.shape, np.uint8)
done = False
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

cv2.waitKey(0)
cv2.waitKey(0)
while(not done):
    print("----------------------------------------")
    print("Début boucle")
    cv2.imshow('fenetreImage', img)
    cv2.waitKey(0)

    eroded = cv2.erode(img, element)
    print("Erosion")
    cv2.imshow('fenetreImage', eroded)
    cv2.waitKey(0)

    temp = cv2.dilate(eroded, element)
    print("Dilatation")
    cv2.imshow('fenetreImage', temp)
    cv2.waitKey(0)

    print("Substract avec ça")
    cv2.imshow('fenetreImage', img)
    cv2.waitKey(0)

    temp = cv2.subtract(img, temp)
    print("Soustraction")
    cv2.imshow('fenetreImage', temp)
    cv2.waitKey(0)

    skel = cv2.bitwise_or(skel, temp)
    print("OU binaire")
    cv2.imshow('fenetreImage', skel)
    cv2.waitKey(0)

    img = eroded.copy()

    zeros = size - cv2.countNonZero(img)
    if zeros == size:
        done = True

while True:
    cv2.imshow('fenetreImage', skel)
    if cv2.waitKey(1) == ord('q'):
        break

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
