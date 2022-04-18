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
from math import sqrt
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
        self._video_on = False
        self._turning = False
        self._turning_compteur = False
        self._flag = False
        self._last_image = None
        self._last_image_ok = True
        self._stop_compteur = None

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

            ret, img = self._cap.read()      # Récuperer le flux
            if ret is False:                 # Si jamais il y a un erreur
                print("Impossible de joindre la caméra")
                exit(1)
            image = Image(img)
            image.send(Serveur.VIDEO_SOCKET)
            if analyser_virage:
                self.analyser(image)
                if self._flag is True:
                    image.log("PriseDeVirage")


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
        if abs(self._turning) <= 1:
            self._turning = False

        if self._turning is not False:
            if self._boucle_fin is False:
                # Premiere fois qu'on ne trouve pas de ligne
                self._boucle_fin_pas = servo_dir.angle() / (3 / 0.1)
                self._boucle_fin_compteur = servo_dir.angle()
                self._boucle_fin = True
            else:
                self._boucle_fin_compteur = self._boucle_fin_compteur - self._boucle_fin_pas
                servo_dir.angle(self._boucle_fin_compteur)
                if abs(self._boucle_fin_compteur) < 1:
                    self._turning = False
            print("STEP : ", self._boucle_fin_compteur)
            sleep(0.1)
        else:
            mtn = clock_gettime(CLOCK_MONOTONIC)
            if not self._stop_compteur:
                self._stop_compteur = mtn
            elif mtn + 3 < clock_gettime(CLOCK_MONOTONIC):
                moteur.do("stop")
                self._turning = False
            sleep(conf("image.long_sleep"))
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

    def analyserVirageEnCours(self, shift, angle):
        txt = ""
        adjust, rotationRoues, temps = None, None, 0

        delta_shift, delta_angle = None, None
        if self._last_image and self._last_image.shift is not None:
            delta_shift = abs(self._last_image.shift) - abs(shift)
            delta_angle = self._last_image.angle - angle
            txt += " delta={}".format((delta_shift, int(delta_angle)))

        if delta_shift is not None and delta_shift > 60 and abs(shift) < 500:
            # Saut de shift 380 à 200
            txt += " (rapprochement)"
            rotationRoues = self._turning
            temps = conf("image.short_sleep")

        elif sign(shift) == sign(self._turning) and abs(shift) > 90:
            # On va dépasser la ligne bientôt !
            if self._last_image_ok:
                # Aller (on va la dépasser)
                txt += " dépassement de ligne, grosse rectification"
                rotationRoues = self._turning
                adjust = True
                temps = conf("image.short_sleep")
            else:
                # Retour (on l'a dépassée et elle réapparait)
                txt += " retour de la ligne"
                rotationRoues = angle_transf(angle)
                temps = conf("image.short_sleep")

        elif delta_shift is not None and delta_shift < -30:
            # Saut de shift 200 à 300 --> on risque de le perdre !
            txt += " (éloignement)"
            correction = affine((-30, 10), (200, 30))(abs(delta_shift))
            rotationRoues = -sign(self._turning) * correction
            adjust = True
            temps = conf("image.short_sleep")

        elif(delta_angle is not None and (angle == 0
             or (delta_angle > 5 and sign(delta_angle) == sign(self._turning)))
             or (delta_shift is not None and delta_shift < -30
             and self._turning - angle > 10)):
            txt += "->VIRAGE FINIII"
            self._turning = False
            adjust, rotationRoues, temps, txt2 = self.analyserVirageNormal(
                shift, angle
            )
            txt += "<Normal>" + txt2
        elif abs(shift) > 100:
            if delta_shift is not None and (abs(delta_shift) < 20
                                            or delta_shift > 0):
                rotationRoues = None
                txt += "shift stable..."
            else:
                rotationRoues = sign(shift) * shift_transf(abs(shift))
                txt += " shift en tournage de {}".format(int(angle))
            adjust = True
            temps = conf("image.short_sleep")
        elif angle != 0:
            txt += " angle en tournage"
            if not self._last_image_ok:
                rotationRoues = 0
            else:
                rotationRoues = 5 * sign(angle)
                adjust = True
            temps = conf("image.long_sleep")

        return adjust, rotationRoues, temps, txt

    def analyserVirageNormal(self, shift, angle):
        txt = ""
        adjust, rotationRoues, temps = None, None, 0

        delta_shift = None
        if self._last_image and self._last_image.shift is not None:
            delta_shift = abs(self._last_image.shift) - abs(shift)
            txt += " delta={}".format(delta_shift)

        if angle != 0 and not self._turning:
            txt += " Début de virage (turning={})".format(int(angle))
            self._flag = True
            self._turning = angle
            adjust, rotationRoues, temps, txt2 = self.analyserVirageEnCours(
                shift, angle
            )
            txt += "<Virage>" + txt2
        elif shift != 0:
            rotationRoues = simple_shift_transf(shift)
            if self._last_image_ok is False:
                rotationRoues = rotationRoues * 2
                txt += " (x2)"
            elif((abs(shift) > 80 and delta_shift and delta_shift < 3)
                 or (abs(shift) > 50 and delta_shift and delta_shift < 15)):
                rotationRoues = rotationRoues // 2
                txt += " (/2)"
            txt += " shift simple"
            temps = conf("image.short_sleep")
        elif angle != 0:
            txt += " angle simple"
            rotationRoues = angle_transf(angle)
            temps = conf("image.long_sleep")
        else:
            angle = 0

        return adjust, rotationRoues, temps, txt

    def analyserVirage(self, image):
        """
        Changer la direction selon le décallage et l'angle de la ligne.
        """
        resultat_analyse = image.shift_angle()

        if resultat_analyse is None:
            if conf("debug.image.analyse"):
                print("analyse virage failed")
            image.log("analyseVirageFailure")
            return

        txt = "{} -> ".format(around(resultat_analyse).astype(int))

        if resultat_analyse[1] > 90:
            if conf("debug.image.analyse"):
                print("angle too large")
            image.log("angleTooLarge")
            return

        shift, angle = seuiller_shift_angle(*resultat_analyse)

        txt += "{} -> ".format(around((shift, angle)).astype(int))

        if self._turning is not False:
            txt += " (turning=True) "
            adjust, rotationRoues, temps, txt2 = self.analyserVirageEnCours(shift, angle)
        else:
            txt += " (turning=False) "
            adjust, rotationRoues, temps, txt2 = self.analyserVirageNormal(shift, angle)

        txt += txt2

        if rotationRoues is not None:
            txt += " : {} de {}".format(
                "rectification" if adjust else "angle",
                int(rotationRoues)
            )
            if adjust:
                servo_dir.adjust_angle(rotationRoues)
            else:
                servo_dir.angle(rotationRoues)
        if temps is not None:
            txt += "({} s)".format(temps)
            sleep(temps)

        if conf("debug.image"):
            print(txt)

    def __del__(self):
        # Libération des ressources
        pass


robot = Robot()
robot.start_serveur()
