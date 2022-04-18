"""
Le module robot contient la classe Robot, qu'il instancie et
initie en lançant le serveur.
"""
from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from serveur import Serveur
from image import Image
from time import clock_gettime, CLOCK_MONOTONIC, sleep
from config import get as conf
from math import floor, ceil
from controle import servo_dir, servo_x, moteur


class Robot:
    """
    La classe robot représente le robot dans son ensemble,
    avec comme paramètre :

    - CAMERA_DEVICE     : fichier correspondant à la caméra branchée

    Attributs d'instance :
    - cap           (VideoCapture) source du flux vidéo
    - video_on      flag permettant de stopper le thread de capture vidéo
    """
    CAMERA_DEVICE = "/dev/video0"
    fps_counter = clock_gettime(CLOCK_MONOTONIC)

    def __init__(self):
        self._cap = VideoCapture(conf("robot.device"))
        self._cap.set(CAP_PROP_FRAME_HEIGHT, conf("robot.capture.height"))
        self._cap.set(CAP_PROP_FRAME_WIDTH, conf("robot.capture.width"))
        self.init_vars()

    def init_vars(self):
        self.old_rotation = 0
        self._stop_compteur = None
        self._video_on = False
        self._flag = False
        
    def start_serveur(self):
        """
        Cette méthode créé un serveur (thread) avec le module serveur,le lance,
        et le join (thread actuel mis en pause jusqu'a terminaison du thread
        serveur).
        """
        try:
            serveur = Serveur(self)
            serveur.start()
            serveur.join()
            del(serveur)
        except OSError:
            print("Impossible de démarrer, il faut attendre...")
            for i in range(5):
                print("Redémarrage dans", 5 - i, "secondes")
                sleep(1)
            self.start_serveur()
        except (KeyboardInterrupt, InterruptedError):
            print("Arrêt du serveur")

    def start_video(self):
        """
        La méthode start_video lance une boucle qui, tant que la variable
        d'instance privée video_on est vraie, lit une image, et lance
        son analyse grâce au module ImageClass.
        Il est recommandé d'exécuter cette fonction en parallèle afin de ne pas
        bloquer le programme.
        """
        while self._video_on:
            ret, image = self._cap.read()      # Récuperer le flux
            if ret is False:                 # Si jamais il y a un erreur
                print("Impossible de joindre la caméra")
            image = Image(image)
            self.analyser(image)

    def analyser(self, image):
        """ Logique de l'analyse d'image """
        if image.isFin():
            image.send(Serveur.VIDEO_SOCKET)
            self.actionOnFin()
        else: 
            image.Traitement()  # Pré-traitement
            image.send(Serveur.VIDEO_SOCKET, image._image_thresh)
            self.analyserVirage(image)
            moteur.do("run")
    
    def actionOnFin(self):
        """
        Action à effectuer lorsque la voiture ne détecte pas de ligne.

        Logique :
        - Si le robot était en train de tourner :
            - Si les roues sont tournées :
                On continue à rouler en réduisant l'angle des roues
        - Sinon on s'arrête
        """

        mtn = clock_gettime(CLOCK_MONOTONIC)
        if not self._stop_compteur:
            self._stop_compteur = mtn
        elif mtn + 2 < clock_gettime(CLOCK_MONOTONIC):
            moteur.do("stop")

    def analyserVirage(self, image, withCamera = True):
        """
        Changer la direction selon le décallage et l'angle de la ligne.
        """
        resultat = image.shift_angle()
        shift, angle = resultat[0]
        shiftangle = (shift/10)+(angle/2)
        
        rotation = (shiftangle-servo_x.angle()+self.old_rotation)/2
        rotation = floor(rotation) if shift>=0 else ceil(rotation)
        self.old_rotation = rotation
        
        if withCamera:
            rotation_camera = -(rotation + servo_x.angle())/2
            rotation_camera = floor(rotation_camera) if shift>=0 else ceil(rotation_camera)
            if (abs(rotation_camera)>20):
                if rotation_camera+servo_x.angle()<-35: servo_x.angle(-35)
                elif rotation_camera+servo_x.angle()>35: servo_x.angle(35)
                else: servo_x.adjust_angle(rotation_camera)
                #sleep(0.01)
        servo_dir.angle(rotation)
       
robot = Robot()
robot.start_serveur()
