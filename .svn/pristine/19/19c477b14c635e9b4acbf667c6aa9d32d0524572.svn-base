"""
Le module robot contient la classe Robot, qu'il instancie et
initie en lançant le serveur.
"""
from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from serveur import Serveur
from image import Image
from time import clock_gettime, CLOCK_MONOTONIC, sleep
from config import get as conf


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
        self._video_on = False

    def start_video(self, analyser_virage=False):
        """
        La méthode start_video lance une boucle qui, tant que la variable
        d'instance privée video_on est vraie, lit une image, et lance
        son analyse grâce au module ImageClass.
        Il est recommandé d'exécuter cette fonction en parallèle afin de ne pas
        bloquer le programme.
        """

        if conf("debug.general"):
            print("start video ", self._video_on)

        while self._video_on:
            if conf("debug.FPS"):
                heure = clock_gettime(CLOCK_MONOTONIC)
                print(1 / (heure - self.fps_counter), "FPS")
                self.fps_counter = heure

            ret, img = self._cap.read()      # Récuperer le flux
            if ret is False:                 # Si jamais il y a un erreur
                print("Impossible de joindre la caméra")
                exit(1)
            image = Image(img)
            image.send()
            if analyser_virage:
                image.analyser()


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
        except (KeyboardInterrupt, InterruptedError):
            print("Arrêt du serveur")
        finally:
            del(serveur)

    def __del__(self):
        # Libération des ressources
        pass


robot = Robot()
robot.start_serveur()
