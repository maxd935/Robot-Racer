"""
Le module ImageClass contient uniquement la classe Image, avec
la configuration du serveur UDP qui reçoit les images (le client).
"""
import cv2
from numpy import int0
from util import (
    colsort,
    rect_to_points,
    points_to_droite,
    droite_to_angle
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

    def __init__(self, image):
        self._image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def isFin(self):
        """
        Détecter la présence d'une ligne
        Seuillage de la ligne noire (pix<50)
        Compare le nbr de non-zero retrouvé l'image seuillé
        """
        return 50 > cv2.countNonZero(cv2.threshold(
            self._image, 50, 255,
            cv2.THRESH_BINARY_INV)[1]
        )

    def isSurex(self):
        """
        Détecter si une image est en surexposition ou non.

        Seuillage de la partie "Surex", partie de couleur blanche (pix>220)
        Compare le nbr de non-zero retrouvé l'image seuillé

        Renvoie True si l'image est en surexposition, False sinon.
        """
        return 50 < cv2.countNonZero(cv2.threshold(
            self._image, 245, 255,
            cv2.THRESH_BINARY)[1]
        )
    
    def Traitement(self):
        """
        Effectue un seuillage en fonction de l'exposition.
        """
        if self.isSurex(): 
            self._image_thresh = cv2.adaptiveThreshold(self._image, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 501, 25)
        else:
            _, self._image_thresh = cv2.threshold(self._image,
            0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)                  

    def send(self, server=None, img=None):
        """
        Envoyer l'image courante (ou passée en paramètre) sur le serveur UDP
        """
        if server is None: return
        
        if img is None:
            img = self._image

        res,jpg=cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 10])
        
        try:
            server.sendall(int(jpg.size).to_bytes(4, 'big', signed=True)
                           + jpg.tobytes())
        except OSError:
            print("Erreur: image::Image.send")

    def shift_angle(self, nbRec=1):
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
        X = len(img[0])
        Y = len(img)
        ligne_split = int(Y/nbRec)
        tab = [] 
        
        for i in range(1,nbRec+1):
            contours, _ = cv2.findContours(img[ligne_split*(i-1):ligne_split*i], cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
            if contours is None or len(contours) == 0: 
                tab.append(None)
            else:
                best_contours = max(contours, key=cv2.contourArea)
                rect = cv2.minAreaRect(best_contours)
                (cx, cy), size, angle = rect
                rect = (cx, cy+ligne_split*(i-1)), size, angle
                box = int0(cv2.boxPoints(rect))
                box2 = colsort(box, 1)
                A, B = rect_to_points(X, Y, box2)
                (m, p) = points_to_droite(A, B)
                
                angle = droite_to_angle(m, p)
                xbottom = -(p/m) if p is not None else m              
                shift = int((xbottom*100) / (X/2))
                tab.append((shift, angle))
                
                img = cv2.drawContours(img, [box], 0, 127, 3)
                img = cv2.line(img, (int(A[0]+X/2), int(Y-A[1])), (int(B[0]+X/2), int(Y-B[1])), 50, 10)
               
        self._image_thresh = img 
        return tab

def __imageTest__(image):
    image = cv2.imread(image)
    img = Image(image)
    img.Traitement()
    resultat_analyse = img.shift_angle(1)

    for i in range (len(resultat_analyse)):
        shift, angle = resultat_analyse[i]
        print (shift, angle)
    
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', (640, 380))
    cv2.moveWindow('img', 480, 0)
    cv2.imshow("img", img._image_thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return "Fini \n"


print(__imageTest__("image\img.jpg"))
print(__imageTest__("image\surex2.jpg"))
print(__imageTest__("image\surex.jpg"))
