"""
Le module robot contient la classe Robot, qu'il instancie et
initie en lançant le serveur.
"""
from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from serveur import Serveur
from image import Image
from time import clock_gettime, CLOCK_MONOTONIC, sleep
from config import get as conf
from numpy import sign, around
from controle import servo_dir, moteur
from util import (
    seuiller_shift_angle,
    affine,
    angle_transf,
    shift_transf,
    simple_shift_transf
)
from time import clock_gettime, CLOCK_MONOTONIC, sleep


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
        self.fps_counter = 0
        self._video_on = False
        self._stop_compteur = None
        self._last_image_ok = False
        self._historique = list()

    def start_video(self, analyser_virage=True):
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
                exit(1)
            image = Image(self.lire_image())
            image.send(Serveur.VIDEO_SOCKET)
            if analyser_virage:
                self.analyser(image)
                # image.log("PriseDeVirage")

    def lire_image(self):
        ret, img = self._cap.read()      # Récuperer le flux
        if ret is False:                 # Si jamais il y a un erreur
            print("Impossible de joindre la caméra")
        return img

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
        if conf("debug.general"):
            print("Pas de ligne détéctée")

    def analyser(self, image):
        """ Logique de l'analyse d'image """
        if image.isFin():
            image.log("isfin")
            self._last_image_ok = False
            self.actionOnFin()
        else:
            self._boucle_fin = False
            self._stop_compteur = None
            moteur.do("run")
            if image.isSurex():  # Pré-traitement
                if conf("debug.image.surex"):
                    print("Is surex")
                image.log("surex")
                image.preTraitementSurex()
            else:
                if conf("debug.image.surex"):
                    print("Not surex")
                image.preTraitementPasSurex()

            self.analyserVirage(image)
            self._last_image = image
            self._last_image_ok = True

    def analyserVirage(self, image):
        """
        Changer la direction selon le décallage et l'angle de la ligne.
        """
        # image.log("PriseDeVirage")
        resultat_analyse = image.shift_angle()

        if resultat_analyse is None:
            if conf("debug.image.analyse"):
                print("analyse virage failed")
            image.log("analyseVirageFailure")
            return

        if resultat_analyse[1] > 90:
            if conf("debug.image.analyse"):
                print("angle too large")
            image.log("angleTooLarge")
            return

        shift, angle = resultat_analyse

        if len(self._historique) == 0:
            self._historique.append((shift, angle, 0))

        old_shift, old_angle, action = self._historique[-1]
        ashift, aangle = abs(shift), abs(angle)
        sshift, sangle = sign(shift), sign(angle)
        dshift, dangle = abs(old_shift - shift), abs(old_angle - angle)
        enRapprochement = (sign(old_shift) == sshift and ashift
                           < abs(old_shift)) or old_shift == shift
        amelioration = abs(old_shift) - abs(shift)

        txt = "{} {}-> ".format(around((shift, angle)).astype(int), (amelioration, enRapprochement))

        self._historique.append((shift, angle, servo_dir.angle()))

        if ashift < 35:
            shift = 0
        if angle < 50:
            angle = 0

        if shift != 0:
            txt += "shift "
            if amelioration < -50:
                txt += "amélioration "
                servo_dir.angle(shift // 2)
            elif not enRapprochement:
                txt += "en rapprochement "
                servo_dir.adjust_angle(10 * sshift)
                # sleep(0.05)
        elif angle != 0:
            txt += "angle !"
            servo_dir.angle(35 * sangle)
            # sleep(0.2)
        else:
            servo_dir.angle(0)


        if conf("debug.image"):
            print(txt)

    def __del__(self):
        # Libération des ressources
        pass


robot = Robot()
robot.start_serveur()
