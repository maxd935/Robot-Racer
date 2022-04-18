import cv2


class Image:
    tailleImageX = 50            # longueur de pixel horizontal

    def __init__(self, image):
        # pour ImageTest
        self._image = cv2.imread(image, cv2.IMREAD_COLOR)
        # pour video
        # self._image = image
        # Binarisation
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)

    def traitement(self):
        # Seuillage Otsu : Image binaire & seuil optimal
        rel, self._image = cv2.threshold(self._image, 0, 255, cv2.THRESH_OTSU)
        return rel

    def shift_angle(self):
            """
        Trouver le décallage et l'angle de la ligne.
        Angle : Angle que forme la ligne avec l'axe vertical.
                Est compris entre -90 et 90°.
        Décallage : décallage de la ligne par rapport au centre bas de l'image.
                    Il est en pourcentage et oscille autour de 0% (peut
                    dont être négatif)
        Par exemple :
        +----------+---------+
        |                |  ||
        |               /  / |
        |             /  /   |
        |            |  |    |
        +----------+--+-------+
                   |  |
               milieu |
                      décallage de +10%

        """
        # Contours
        img = self._image_thresh
        _, contours, _ = cv2.findContours(img, cv2.RETR_CCOMP,
                                          cv2.CHAIN_APPROX_SIMPLE)

        if contours is None or len(contours) == 0:
            if conf("debug.image.analyse"):
                print("Image.shift_angle : Pas de contours trouvé")
            return None

        best_contours = max(contours, key=cv2.contourArea)

        (m, p), estCentree = self.approx_droite_rect(best_contours)
        xbottom = None
        if p is None:
            keepRect = False
            if not estCentree:
                m2, p2 = self.approx_droite_hough(best_contours)
                if p2 is not None:
                    if conf("debug.image.angle_fct"):
                        print("USE HUGH de hough")
                    m, p = m2, p2
                else:
                    keepRect = True
            if keepRect or estCentree:
                xbottom = m
                angle = 0

        if xbottom is None:
            angle = atan(m) * 180 / PI + 90 if m != 0 else 90
            xbottom = (len(img) - p) / m if m != 0 else m

        shift = int(100 * (2 * xbottom / len(img[0]) - 1))

        return (shift, angle)

    def getImage(self):
        return self._image

    # Pixelliser en taille x taille pixels
    def resizeImage(self):
        tailleImageY = len(self._image) * self.tailleImageX / len(self._image[0])
        self._image = cv2.resize(self._image, (self.tailleImageX, int(tailleImageY)))

    def isSurex(self):
        return 0 != cv2.countNonZero(cv2.threshold(self._image, 220, 255, cv2.THRESH_BINARY)[1])
        # Detection de la surexposition
        # Seuillage de la partie "Surex", partie de couleur blanche (pix>220)
        # Compare le nbr de non-zero retrouvé l'image seuillé

    def isFin(self):
        return 0 == cv2.countNonZero(cv2.threshold(self._image, 40, 255, cv2.THRESH_BINARY_INV)[1])
        # Detection d'une ligne
        # Seuillage de la ligne noire (pix<40)
        # Compare le nbr de non-zero retrouvé l'image seuillé
