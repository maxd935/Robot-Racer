import cv2
import numpy as np
from threading import Thread
from time import sleep

tailleImage = (32, 24)
pourcentage_split = 0.5


class Analyse(Thread):

    def __init__(self):
        self._cap = cv2.VideoCapture("/dev/video2")
        self.setDaemon(True)
        print("Analyse initiée")

    def calculer_angles(img):
        size = len(img)
        ligne_split = int(size * pourcentage_split)
        rect0 = (0, 0, 0)
        rect1 = (0, 0, 0)

        im2, contours, hierarchy = cv2.findContours(img[0:ligne_split],
                                               cv2.RETR_EXTERNAL, 2)
        if contours:
            rect0 = cv2.minAreaRect(contours[0])
            box = np.int0(cv2.boxPoints(rect0))
            img = cv2.drawContours(img, [box], 0, 127, 1)

        im2, contours, hierarchy = cv2.findContours(img[ligne_split:size],
                                               cv2.RETR_EXTERNAL, 2)
        if contours:
            rect1 = cv2.minAreaRect(contours[0])
            (cx, cy), size, angle = rect1
            rect1 = (cx, cy + ligne_split), size, angle
            box = np.int0(cv2.boxPoints(rect1))
            img = cv2.drawContours(img, [box], 0, 127, 1)

        return (rect1[2], rect0[2])

    def run(self):
        print("Analyse démarrée")
        while True:
            ret, img = self._cap.read()            # Récuperer le flux
            if ret is False:                 # Si jamais il y a un erreur
                print("Impossible de joindre la caméra")
                exit(1)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, tailleImage)
            # On peut aussi calculer le seuil cv2.THRESH_OTSU)
            ret, img = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY_INV)
            angle1, angle2 = self.calculer_angles(img)
            print(angle1 % 90, " --- ", angle2 % 90, " --- ", ret)

            sleep(1e-5)

    def __del__(self):
        print("Analyse arrêté")
        # Libération des ressources
        self._stop.set()
        self._cap.release()
        cv2.destroyAllWindows()
