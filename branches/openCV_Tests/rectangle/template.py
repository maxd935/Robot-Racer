import cv2
import numpy as np

tailleImage = (64, 48)
tailleFenetre = (600, 600)
secondPointY = 0.6
quantification = 255

cap = cv2.VideoCapture("/dev/video3")
cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)

while True:
    ret, img = cap.read()            # Récuperer le flux
    if ret is False:                           # Si jamais il y a un erreur
        print("Impossible de joindre la caméra")
        exit(1)


    # C'est parti !
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, tailleImage)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, 2)
    cnt = contours[0]
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    img = cv2.drawContours(img, [box], 0, 127, 1)

    cv2.imshow('fenetreImage', img)
    if cv2.waitKey(1) == ord('q'):
        break

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
