"""
Le module ImageClass contient uniquement la classe Image, avec
la configuration du serveur UDP qui reçoit les images (le client).
"""
import cv2
from numpy import ones, uint8, zeros_like, pi, array, int0, mean, sign, save, NaN
from datetime import datetime as dt
from config import get as conf
from os.path import exists
from os import makedirs as mkdir
from util import (
    colsort,
    norme,
    points_to_droite,
    droite_to_angle,
    shift_corner
)


class Image:
    """
    La classe Image représente une image et permet de réaliser les
    opérations de contrôle du robot nécessaire pour qu'il suive
    la ligne.
    Elle contient comme attributs de classe :
    - tailleImageY :    La hauteur de l'image
    - tailleImageX :    La largeur de l'image (calculée en fct de la hauteur)

    Et comme attributs privés :
    - image :       Image originale en nuances de gris et recadrée
    - image_thresh  Image seuillée
    """

    def __init__(self, image, ROI=conf("image.ROI")):
        self._image = image[int(ROI * len(image)):]
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        self.shift, self.angle = None, None

    def isFin(self, seuil_fin=conf("image.seuil.fin")):
        """
        Détecter la présence d'une ligne
        Seuillage de la ligne noire (pix<50)
        Compare le nbr de non-zero retrouvé l'image seuillé
        """
        return 100 > cv2.countNonZero(cv2.threshold(
            self._image, seuil_fin, 255, cv2.THRESH_BINARY_INV)[1]
        )

    def isSurex(self):
        """
        Détecter si une image est en surexposition ou non.

        Seuillage de la partie "Surex", partie de couleur blanche (pix>220)
        Compare le nbr de non-zero retrouvé l'image seuillé

        Renvoie True si l'image est en surexposition, False sinon.
        """
        return 0 != cv2.countNonZero(cv2.threshold(
            self._image,
            conf("image.seuil.surex"), 255,
            cv2.THRESH_BINARY)[1]
        )

    def log(self, categorie=None, img=None, thresh=False):
        if img is None:
            img = self._image if not thresh else self._image_thresh
        path = "./log/" + (categorie + "/") if categorie is not None else ""
        filename = str(dt.isoformat(dt.now())) + ".png"
        if not exists(path):
            mkdir(path)
        cv2.imwrite(path + filename, img)

    def preTraitementSurex(self):
        img = cv2.blur(self._image, (7, 7))
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY_INV, 501, 25)
        # Transformations morphologiques
        kernel = ones((2, 2), uint8)
        img = cv2.erode(img, kernel, iterations=7)
        img = cv2.dilate(img, kernel, iterations=7)
        self._image_thresh = img

    def preTraitementPasSurex(self):
        ksize = int(len(self._image[0]) / 12.5)
        cv2.medianBlur(self._image, ksize,
                       dst=self._image)
        _, self._image_thresh = cv2.threshold(
            self._image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )

    def send(self, server=None, img=None):
        """
        Envoyer l'image courante (ou passée en paramètre) sur le serveur UDP
        """
        if server is None:
            if conf("debug.network"):
                print("NO VIDEO SOCKET")
            return
        if img is None:
            img = self._image

        res, jpg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY),
                                              conf("image.jpg_quality")])
        try:
            server.sendall(int(jpg.size).to_bytes(4, 'big', signed=True)
                           + jpg.tobytes())
        except OSError:
            print("Erreur: image::Image.send")

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

        use_hough = False
        (m, p), estCentree = self.approx_droite_rect(best_contours)
        (best_contours)
        xbottom = None
        if p is None:
            keepRect = False
            if not estCentree:
                m2, p2 = self.approx_droite_hough(best_contours)
                if p2 is not None:
                    if conf("debug.image.angle_fct"):
                        print("USE HUGH de hough")
                    use_hough = True
                    m, p = m2, p2
                else:
                    keepRect = True
            if keepRect or estCentree:
                xbottom = m
                angle = 0

        if xbottom is None:
            angle = - droite_to_angle(m, p)
            if m == 0:
                return None
            xbottom = (len(img) - p) / m if p is not None else m

        try:
            shift = int(100 * (2 * xbottom / len(img[0]) - 1))
        except ValueError:
            self.log("NaN")
            save("NaN-log.npy", img)
            return None

        if use_hough and sign(shift) == sign(angle):
            if self.is_in_corner(True, shift):
                shift = shift_corner(shift)

        self.shift, self.angle = shift, angle
        return (shift, angle)

    def is_in_corner(self, bottom=True, shift=-1, kernel=10, img=None):
        if img is None:
            img = self._image_thresh
        y_start = (len(img) - kernel) if bottom else 0
        x_start = (len(img[0]) - kernel) if shift > 0 else 0

        mat = img[y_start:(y_start + kernel), x_start:(x_start + kernel)]
        return (mat == 255).any()

    def approx_droite_hough(self, contours):
        """
        Approximer la droite avec la transformée de Hough
        """
        img_contours = zeros_like(self._image)
        img_contours = cv2.drawContours(img_contours, [contours], -1, 255, 2)

        # Suppression du contour des bordures
        padding = conf("image.padding_width")
        img_contours[:, :padding] = 0
        img_contours[:, -padding:] = 0
        img_contours[:padding, :] = 0
        img_contours[-padding:, :] = 0

        lines = cv2.HoughLinesP(img_contours, 1, pi / 180, 25,
                                minLineLength=20, maxLineGap=5)

        res = list()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # cv2.line(img, (x1, y1), (x2, y2), 127, 4)
                res.append(points_to_droite((x1, y1), (x2, y2)))

        if len(res) == 0:
            return None, None

        # choix de ligne :
        # - maximisant le coef directeur (ligne la plus vertiale)
        #   res = array(res)
        #   res[res[:, 0] == res[:, 0].max()][0]

        # - moyenne des lignes :
        #   x0  = moyenne des x pour y = 0
        #   x50 = - - - - des x pour y = 50
        #   droite qui passe par (x0, 0) et (x50, 50)
        if len(list(filter(
            lambda point: point[1] is not None and point[0] != 0, res
        ))) == 0:
            res = array(res)
            return res[res[:, 0] == res[:, 0].max()][0]

        return points_to_droite(
            (mean([-p / m for m, p in res if p is not None and m != 0]), 0),
            (mean([(50 - p) / m for m, p in res if p is not None and m != 0]), 50)
        )

    def approx_droite_rect(self, contours):
        """
        Calculer l'équation de la droite qui approche la ligne.
        Renvoie un tuple (param, estAuCentre), avec
        - param : un tuple (m, p) pour la droite d'equation y = m*x + p.
          si la droite est de la forme x = constante, m = constante et p = None
        - estAuCentre : bool vrai si le centre du rectangle est à 50% autour du
          centre de l'image
        """
        (cx, cy), (height, width), angle = rect = cv2.minAreaRect(contours)

        # estAuCentre
        imY, imX = len(self._image) // 2, len(self._image[0]) // 2
        estAuCentre = True
        if cx > imX + imX // 2 or cx < imX - imX // 2:
            estAuCentre = False
        elif cy > imY + imY // 2 or cy < imY - imY // 2:
            estAuCentre = False
        if angle == 0.0:
            return (cx, None), estAuCentre

        box = int0(cv2.boxPoints(rect))

        box2 = colsort(box, 1)
        (h1, h2), (b1, b2) = colsort(box2[0:2]), colsort(box2[2:4])

        if norme(h1, h2) > norme(h2, b2):
            if h2[1] > h1[1]:
                h1, b2 = b2, h1
            elif h1[1] > h2[1]:
                b1, h2 = h2, b1

        mhx, mhy = (h1[0] + (h2[0] - h1[0]) / 2,
                    h1[1] + (h2[1] - h1[1]) / 2)
        mbx, mby = (b1[0] + (b2[0] - b1[0]) / 2,
                    b1[1] + (b2[1] - b1[1]) / 2)

        # draw = self._image_thresh.copy()
        # cv2.drawContours(draw, [box], 0, 127, 3)
        # cv2.line(draw, (int(mbx), int(mby)), (int(mhx), int(mhy)), 127)
        # self.send(draw)

        ret = points_to_droite((mbx, mby), (mhx, mhy))
        return ret, estAuCentre
