import cv2
import numpy as np

tailleImage = (32, 24)
tailleFenetre = (600, 600)


cap = cv2.VideoCapture("/dev/video2")
cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)


def calculer_angles(img):
    rect0 = (0, 0, 0)

    im, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, 2)
    if contours:
        rect0 = cv2.minAreaRect(contours[0])
        box = np.int0(cv2.boxPoints(rect0))
        img = cv2.drawContours(img, [box], 0, 127, 1)

    return rect0[2]


while True:
    ret, img = cap.read()            # Récuperer le flux
    if ret is False:                 # Si jamais il y a un erreur
        print("Impossible de joindre la caméra")
        exit(1)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, tailleImage)
    ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)

    angle1 = calculer_angles(img)
    print(angle1 % 90)
    cv2.imshow('fenetreImage', img)
    if cv2.waitKey(1) == ord('q'):
        break

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
