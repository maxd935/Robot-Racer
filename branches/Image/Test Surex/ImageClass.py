import cv2
import numpy


class Image:
    tailleImageX = 50            # longueur de pixel horizontal
    quantification = 3          # 3 couleurs Blanc Gris Noir

    def __init__(self, image):
        # Lire et quantification de l'image
        self._image = self.resizeImage(image)
        # Binarisation
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        if(self.isSurex()):
            print("Is surex")
            return
        # Seuillage
        ret, self._image = cv2.threshold(self._image, 0, 255, cv2.THRESH_OTSU)

    def getImage(self):
        return self._image

    def resizeImage(self, image):
        tailleImageY = len(image) * self.tailleImageX / len(image[0])
        return cv2.resize(image, (self.tailleImageX, int(tailleImageY)))
        # Pixelliser en taille x taille pixels

    def isSurex(self):
        return 0 != cv2.countNonZero(cv2.threshold(self._image, 220, 255, cv2.THRESH_BINARY)[1])
        # Compare le nbr de 0 a l'image seuiller, zone blanche
