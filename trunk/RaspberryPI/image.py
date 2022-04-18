"""
Le module ImageClass contient uniquement la classe Image, avec
la configuration du serveur UDP qui reçoit les images (le client).
"""
import cv2
from datetime import datetime as dt
from config import get as conf
from os.path import exists
from os import makedirs as mkdir
from numpy import (
    ones,
    uint8,
    zeros_like,
    pi,
    array,
    int0,
    mean,
    sign,
    save,
    array_split,
    where
)
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

    Attributes
    ----------
    _image : ndarray
        Image originale en nuances de gris et recadrée
    _image_thresh : ndarray
        Image seuillée
    """

    def __init__(self, image, ROI=conf("image.ROI")):
        """ Constructeur
        Conversion de l'image en nuances de gris et séléction
        de la zone d'intérêt.

        Parameters
        ----------
        ROI : int
            Compris entre 0 et 1. Pourcentage de l'image coupée en haut.
            Par exemple 0.2 signifie que l'on garde uniquement les 80% du bas
            de l'image.
        """
        self._image = image[int(ROI * len(image)):]
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        self.shift, self.angle = None, None

    def isFin(self, seuil_fin=conf("image.seuil.fin"), prc_fin=conf("image.prc_fin")):
        """
        Détecter la présence d'une ligne ou non sur une image


        Parameters
        ----------
        seuil_fin : float
            Tout ce qui est supérieur à ce seuil est considéré comme étant la
            ligne.
        prc_fin : float
            pourcentage minimum de ligne requis pour que l'image soit
            considérée comme "ayant une ligne" et que la fonction retourne False

        Returns
        -------
        bool
            Vrai si il n'y a pas de ligne, faux si il y a une ligne.


        Notes
        -----
        Seuillage de la ligne noire (pix<50)
        Compare le nbr de non-zero retrouvé l'image seuillé
        Il doit y avoir plus de prc_fin pourcents de ligne visible sinon
        le seuillage OTSU ne fonctionnera pas.
        """
        return self._image.size * prc_fin > cv2.countNonZero(cv2.threshold(
            self._image, seuil_fin, 255, cv2.THRESH_BINARY_INV)[1]
        )

    def isSurex(self, seuil_surex=conf("image.seuil.surex")):
        """
        Détecter si une image est en surexposition ou non.

        Parameters
        ----------
        seuil_surex : float
            S'il existe un pixel ayant une valeur supérieure à ce seuil, alors
            l'image est considérée comme surexposée.

        Returns
        -------
        bool
            Vrai si l'image est en surexposition, faux sinon.

        Notes
        -----
        Seuillage de la partie "Surex", partie de couleur blanche (pix>220)
        Compare le nbr de non-zero retrouvé l'image seuillé
        """
        return 0 != cv2.countNonZero(cv2.threshold(
            self._image,
            seuil_surex, 255,
            cv2.THRESH_BINARY)[1]
        )

    def log(self, categorie=None, img=None, thresh=False):
        """
        Enregistrer l'image dans un répertoire.

        Parameters
        ----------
        categorie : str
            Nom du sous dossier du répertoire log où enregistrer l'image.
        img : ndarray or None
            Si None, l'image enregistrée est self._image
            sinon l'image à enregistrer
        thresh : bool
            Si vrai, l'image enregistrée est self._image_thresh, sinon on
            suit la logique du paramètre `img`

        Returns
        -------
        str
            Le nom du fichier enregistré.

        Notes
        -----
        Cette fonction est surtout utilisée à des fins de débogage.
        """
        if img is None:
            img = self._image if not thresh else self._image_thresh
        path = "./log/" + (categorie + "/") if categorie is not None else ""
        filename = str(dt.isoformat(dt.now())) + ".png"
        if not exists(path):
            mkdir(path)
        cv2.imwrite(path + filename, img)
        return filename

    def preTraitementSurex(self):
        """
        Effectue le prétraitement lorsque self._image est une image
        surexposée et met dans la variable self._image_tresh l'image seuillée.

        Returns
        -------
        void
            Rien.
        """
        img = cv2.blur(self._image, (7, 7))
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY_INV, 501, 25)
        kernel = ones((2, 2), uint8)
        img = cv2.erode(img, kernel, iterations=7)
        self._image_thresh = img

    def preTraitementPasSurex(self):
        """
        Effectue le prétraitement lorsque self._image n'est pas une image
        surexposée et met dans la variable self._image_tresh l'image seuillée.

        Returns
        -------
        void
            Rien.

        Notes
        -----
        Le traitement optimal aurait été d'appliquer un flou médian mais à des
        fins d'optimisation du temps de calcul, il a été supprimé.
        """
        _, self._image_thresh = cv2.threshold(
            self._image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )

    def preTraitement(self):
        """
        Effectuer le prétraitement sur l'image courante.
        Le prétraitement dépend de si l'image est surexposée ou non.
        """
        if self.isSurex():
            self.preTraitementSurex()
        else:
            self.preTraitementPasSurex()

    def send(self, server=None, img=None, quality=conf("image.jpg_quality")):
        """
        Envoyer une image sur le serveur UDP du client.

        Parameters
        ----------
        server : tuple of str and int
            Adresse du serveur du client (IP et port)
        img : ndarray or None
            Si None, l'image enregistrée est self._image
            sinon l'image à enregistrer

        Returns
        -------
        void
            Rien.
        """
        if server is None:
            if conf("debug.network"):
                print("NO VIDEO SOCKET")
            return
        if img is None:
            img = self._image

        res, jpg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY),
                                              quality])
        try:
            server.sendall(int(jpg.size).to_bytes(4, 'big', signed=True)
                           + jpg.tobytes())
        except OSError:
            print("Erreur: image::Image.send")

    def shift_angle(self, height=100):
        """
        Trouver le décallage et l'angle de la ligne.

        Parameters
        ----------
        height : int
            hauteur de l'image prise pour référence. Par défaut, on prend
            le shift tout en bas de l'image.
            La hauteur est en pourcentage, donc 100% signifie tout en bas
            de l'image. 0 signifie le haut de l'image.

        Returns
        -------
        shift : float
            Décallage de la ligne par rapport au centre de l'image.
        angle : float
            Angle de la ligne compris entre -90 et 90 degrés.

        Notes
        -----
        *Angle* : Angle que forme la ligne avec l'axe vertical.
                Est compris entre -90 et 90°.
        *Décallage* : décallage de la ligne par rapport au centre bas de l'image.
                    Il est en pourcentage et oscille autour de 0% (peut
                    dont être négatif)

        | Par exemple :
        | +----------+---------+
        | |                |  ||        /
        | |               /  / |       /
        | |             /  /   |      /
        | |            |  |    |     /
        | +----------+--+-------+   /
        |            |  |          |
        |        milieu |          angle de 30°
        |               décallage de +10%
        L'image doit être déjà seuillée afin de procéder à cette analyse

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
            xbottom = ((len(img) * height / 100) - p) / m if p is not None else m

        try:
            shift = int(100 * (2 * xbottom / len(img[0]) - 1))
        except ValueError:
            self.log("NaN")
            save("NaN-log.npy", img)
            return None

        if use_hough and self.is_in_corner(True, angle):
            shift = shift_corner(shift)

        self.shift, self.angle = shift, angle
        return (shift, angle)

    def is_in_corner(self, bottom=True, shift=-1, kernel=10, img=None):
        """
        Verifie si la ligne est dans un coin de l'image.

        Parameters
        ----------
        bottom : bool
            Vrai si on sélection le coin du bas, faux si celui du haut
        shift : int
            -1 si on sélection le coin de gauche, 1 si celui de droit
        kernel : int
            Taille du carré dans le coin à prendre
        img : ndarray
            Si None, l'image est self._image_thresh sinon cette `img`.

        Returns
        -------
        bool
            true si il y a la ligne dans un coin
        """
        if img is None:
            img = self._image_thresh
        y_start = (len(img) - kernel) if bottom else 0
        x_start = (len(img[0]) - kernel) if shift > 0 else 0

        mat = img[y_start:(y_start + kernel), x_start:(x_start + kernel)]
        return (mat == 255).any()

    def approx_droite_hough(self, contours, padding=conf("image.padding")):
        """
        Approximer la droite avec la transformée de Hough

        Parameters
        ----------
        contours : array of points
            liste des points formant le contour dont on cherche la droite

        Returns
        -------
        m : float
            coefficient directeur de la droite
        p : float
            ordonnée à l'origine
        """
        img_contours = zeros_like(self._image)
        img_contours = cv2.drawContours(img_contours, [contours], -1, 255, 2)

        # Suppression du contour des bordures
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

        Parameters
        ----------
        contours : array of points
          liste des points formant le contour dont on cherche la droite

        Returns
        -------
        param : tuple of floats
            un tuple (m, p) pour la droite d'equation y = m*x + p.
            si la droite est de la forme x = constante, m = constante et p = None
        estAuCentre : float
            bool vrai si le centre du rectangle est à 50% autour du
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

    def get3x3(self, seuil=conf("image.seuil.decision")):
        """
        Réduit l'image en une matrice de 3x3 l'image seuillée en réalisant la
        moyenne des pixels

        Parameters
        ----------
        seuil : int
            En dessous de cette valeur, on considère ça comme un 0

        Returns
        -------
        ndarray
            La matrice de dimensions (3, 3).
        """

        mat = array([
            [mean(col) for col in array_split(ligne, 3, axis=1)]
            for ligne in array_split(self._image_thresh, 3, axis=0)
        ]) * 0.255
        return where(mat <= seuil, 0, mat).reshape(3, 3)
