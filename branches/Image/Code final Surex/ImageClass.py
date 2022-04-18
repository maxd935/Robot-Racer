"""
Le module ImageClass contient uniquement la classe Image, avec
la configuration du serveur UDP qui reçoit les images (le client).
Variables de configuration :

- UDP_SERVER    : La socket pour envoyer les images sur le srv distant
- PORT_UDP      : Port du serveur UDP distant
"""
import cv2
import numpy
import numpy as np
import socket
import time
from math import sqrt
#from serveur import Serveur
#from controle import servo_dir

UDP_SERVER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT_UDP = 45655

class Image:
    """
	La classe Image représente une image et permet de réaliser les
	opérations de contrôle du robot nécessaire pour qu'il suive
	la ligne.
	Elle contient comme attributs de classe :
	- tailleImageY :    La hauteur de l'image
	- tailleImageX :    La largeur de l'image (calculée en fct de la hauteur)
	- QUANTIFICATION :  Nombre de couleurs avec l'image est quantifiée
	- RAPPORT_SEUIL :   Rapport pixels blancs / noirs idéal pour seuiller l'img
	"""
    tailleImageX = 50 # longueur de pixel horizontal

    def __init__(self, image):
        self._image=image
        ## Lire l'image (pour ImageClasseTest)
        ##self._image = cv2.imread(image)
        # Binarisation
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        # Pour la classe video
        self.traitement()
        
    def traitement(self):    
        #Verifie si l'image est surex ou non
        isSurex=self.isSurex()
        if(isSurex): 
            print("Is surex")
            block = 501 #int(len(self._image))+1 #501
            #Floutage
            self._image = cv2.blur(self._image, (7, 7))
            # Seuillage
            self._image = cv2.adaptiveThreshold(self._image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,block,25) #40 #cv2.ADAPTIVE_THRESH_GAUSSIAN_C
            # Transformations morphologiques
            kernel = numpy.ones((2, 2), numpy.uint8)
            #self._image = cv2.morphologyEx(self._imag, cv2.MORPH_CLOSE, kernel)
            self._image = cv2.dilate(self._image, kernel, iterations = 7) #5
            self._image = cv2.erode(self._image, kernel, iterations = 7) #15
            #resize pour obtenir une video homogène (non obligatoire)
            self.resizeImage()          
            # Calcule l'angle
            self._image = self.calculer_angle(self._image, 1, 1)  
        else:
            print("Not surex")
            block = int(self.tailleImageX*self.resizeImage()/8)+1
            # Seuillage
            self._image = cv2.adaptiveThreshold(self._image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,block,25)
            # Calcule l'angle
            self._image = self.calculer_angle(self._image, 2, 1)  

    def isSurex(self):
        # Detection de la surexposition
        # Seuillage de la partie "Surex", partie de couleur blanche (pix>220)
        # Compare le nbr de non-zero retrouvé l'image seuillé
        return 0 != cv2.countNonZero(cv2.threshold(self._image, 220, 255, cv2.THRESH_BINARY)[1])
    
    def resizeImage(self):
        # Pixelliser en x taille pixels
        tailleImageY = len(self._image) * self.tailleImageX / len(self._image[0])
        self._image = cv2.resize(self._image, (self.tailleImageX, int(tailleImageY)))
        return tailleImageY
    
    def send(self, img=None):
        """
        Envoyer l'image courante (ou passée en paramètre) sur le serveur UDP
		"""
        if img is None:
            UDP_SERVER.sendto(self._image.tobytes(), (Serveur.IP_CONNECTED, PORT_UDP))
        else:
            UDP_SERVER.sendto(img.tobytes(), (Serveur.IP_CONNECTED, PORT_UDP))
          
    def calculer_angle(self, img, nbRec, tRec):
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
        img = cv2.bitwise_not(img)
        size = len(img)
        ligne_split = int(size/nbRec)
        rect = (0, 0, 0)
        
        for i in range(1,nbRec+1):
            contours, hierarchy = cv2.findContours(img[ligne_split*(i-1):ligne_split*i], cv2.RETR_EXTERNAL, 2)
            if contours:
                selec=None
                if contours is not None and len(contours) > 0:
                    selec = max(contours, key=cv2.contourArea)
                rect = cv2.minAreaRect(selec)
                (cx, cy), size, angle = rect
                rect = (cx, cy+ligne_split*(i-1)), size, angle
                box = np.int0(cv2.boxPoints(rect))
                img = cv2.drawContours(img, [box], 0, 127, tRec)
                #self.send(img)
                
                shift = 0
                angle = 0
                colsort = lambda a, b=0 : a[a[: , b].argsort()]
                box2 = colsort(box, 1)
                (h1, h2), (b1, b2) = colsort(box2[0:2]), colsort(box2[2:4])
                mhx, mhy = (h1[0] + (h2[0] - h1[0]) / 2, h1[1] + (h2[1] - h1[1]) / 2)
                mbx, mby = (b1[0] + (b2[0] - b1[0]) / 2, b1[1] + (b2[1] - b1[1]) / 2)
                xmax = len(img[0])
                ymax = len(img)  
                if mhx - mbx != 0:
                    a = (mhy - mby) / (mhx - mbx)
                    if numpy.abs(a) < 50 and numpy.abs(a) > 0.01:
                        angle = numpy.arctan(a) * 180 / numpy.pi + 90
                        b = cy - a * cx
                        xprime, _ = (ymax - b) / a, ymax
                        if a > 0:
                            angle = 180 - angle
                    else:
                        xprime = mbx
                else:
                    xprime = mbx
                shift = int(100 * (2 * xprime / xmax - 1))
                print (shift, angle)            
        return (img) 
    
    def seuiller_shift_angle(self, shift, angle):
        """
		Si le shift ou l'angle est insignifiant, on ne fait rien.
		"""
        print(angle)
        if abs(shift) < 30:
            shift = 0
        if abs(angle) < 35:
            angle = 0
        return (shift, angle)
    
    def analyserVirage(self):
        """
		Changer la direction selon le décallage et l'angle de la ligne.
		"""
        shift, angle = self.seuiller_shift_angle(*self.shift_angle())
        txt = "{} -> ".format((shift, angle))
        if shift != 0:
            angle = int(sqrt(10 * (abs(shift) - 19)) + 10) * numpy.sign(shift)
            txt += " shift de {}".format(angle)
            servo_dir.angle(angle)
            time.sleep(0.001)
        elif angle != 0:
            txt += " angle de {}".format(angle)
            servo_dir.angle(angle // 2)
            time.sleep(0.25)
        else:
            servo_dir.angle(0)
        print(txt)
        
    def isFin(self):
        # Detection d'une ligne
        # Seuillage de la ligne noire (pix<40)
        # Compare le nbr de non-zero retrouvé l'image seuillé
        return 0 == cv2.countNonZero(cv2.threshold(self._image, 40, 255, cv2.THRESH_BINARY_INV)[1])

    def getImage(self):
        return self._image