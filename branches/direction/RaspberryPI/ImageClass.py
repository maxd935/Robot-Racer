import cv2
import numpy
import socket
import time
from serveur import Serveur
from controle import servo_dir

 
class Image:
    UDP_SERVER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tailleImageY = 33                     # longueur de pixel horizontal
    tailleImageX = tailleImageY * 4 // 3  # longueur de pixel horizontal
    QUANTIFICATION = 3                    # 3 couleurs Blanc Gris Noir
    PORT_UDP = 45655
    RAPPORT_SEUIL = 0.20

    def __init__(self, image):
        self._image = self.resizeImage(image)
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)

    def calculSeuil(self):      # calculer seuil initial
        list = numpy.unique(self._image, return_counts=True)
        # return List de tableau: 1 niveaux de gris;2 List des quantité
        if((list[1][1] < list[1][0]) and (list[1][1] < list[1][2])):
            return list[0][1]               # Seuil optimal
        else:
            return -1

    def resizeImage(self, image):
        return cv2.resize(image, (self.tailleImageX, self.tailleImageY))
        # Pixelliser en taille x taille pixels

    def isSurex(self):
        surex = False
        for i in self._image[0]:
            if i > 200:
                surex = True
        return surex

    def send(self, img=None):
        if img is None:
            Image.UDP_SERVER.sendto(self._image.tobytes(), (Serveur.IP_CONNECTED, Image.PORT_UDP))
        else:
            Image.UDP_SERVER.sendto(img.tobytes(), (Serveur.IP_CONNECTED, Image.PORT_UDP))

    def findTreshHold(self):
        size = numpy.size(self._image)
        for tresh in range(10, 200, 5):
            ret, img = cv2.threshold(self._image, tresh, 255, cv2.THRESH_BINARY_INV)
            if cv2.countNonZero(img) / size > self.RAPPORT_SEUIL:
                return tresh
        print("fail")
        return -1

    def shift_angle(self):
        # tresh_trouve = self.findTreshHold()
        # if tresh_trouve == -1:
        #     return (0, 0)

        img_ori = cv2.threshold(self._image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        im2, contours, hierarchy = cv2.findContours(img_ori, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        selec = None
        if contours is not None and len(contours) > 0:
            selec = max(contours, key=cv2.contourArea)

        (cx, cy), (height, width), angle = rect = cv2.minAreaRect(selec)
        box = numpy.int0(cv2.boxPoints(rect))
        img_ori = cv2.drawContours(img_ori, [box], 0, 127, 1)

        shift = 0
        angle = 0

        colsort = lambda a, b=0 : a[a[: , b].argsort()]
        box2 = colsort(box, 1)
        (h1, h2), (b1, b2) = colsort(box2[0:2]), colsort(box2[2:4])

        mhx, mhy = (h1[0] + (h2[0] - h1[0]) / 2,
                    h1[1] + (h2[1] - h1[1]) / 2)
        mbx, mby = (b1[0] + (b2[0] - b1[0]) / 2,
                    b1[1] + (b2[1] - b1[1]) / 2)

        a = (mhy - mby) / (mhx - mbx)

        if numpy.abs(a) < 50 and numpy.abs(a) > 0.01:
            angle = numpy.arctan(a) * 180 / numpy.pi + 90
            xmax = len(img_ori[0])
            ymax = len(img_ori)
            b = cy - a * cx

            xprime, yprime = (ymax - b) / a, ymax
            shift = int(100 * (2 * xprime / xmax - 1))

            if a > 0:
                angle = 180 - angle
        else:
            angle = 0

        return (shift, angle)

    def seuiller_shift_angle(self, shift, angle):
        if numpy.abs(shift) < 15:
            shift = 0
        if numpy.abs(angle) < 45:
            angle = 0
        return (shift, angle)

    def analyserVirage(self):
        shift, angle = self.seuiller_shift_angle(*self.shift_angle())
        print(shift, angle)
        if shift != 0:
            print("shift ", angle)
            servo_dir.angle(-shift // 2)
        elif angle != 0:
            print("angle ", angle)
            servo_dir.angle(-angle // 2)
        else:
            servo_dir.angle(0)
        time.sleep(0.1)
