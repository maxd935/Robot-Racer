"""
Le module robot contient la classe Robot, qu'il instancie et
initie en lançant le serveur.
"""
from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from serveur import Serveur
from image import Image
from time import clock_gettime, CLOCK_MONOTONIC, sleep
from config import get as conf
from controle import servo_dir, moteur
from simple_image import SimpleImage
from table_decision import prendre_decision


class Robot:
    """
    La classe robot représente l'agent *robot* dans son ensemble.

    Parameters
    ----------
    _cap : VideoCapture
        Classe de OpenCV servant à lire le flux de la caméra.
    _video_on : bool
        Flag permettant de stopper le thread de capture vidéo.
    _stop_compteur : float or None
        Dernière fois que le robot à vu la ligne si il ne la voit plus, où
        None si il voit la ligne.
    _fps_counter : float
        Garde l'heure afin de calculer le temps entre qui s'écoule entre
        deux images.
    """

    def __init__(self):
        self._cap = VideoCapture(conf("robot.device"))
        self._cap.set(CAP_PROP_FRAME_HEIGHT, conf("robot.capture.height"))
        self._cap.set(CAP_PROP_FRAME_WIDTH, conf("robot.capture.width"))
        self.init_vars()

    def init_vars(self):
        """
        Réinitialisation des variables *_fps_counter*, *_video_on*
        et *_stop_compteur*
        """
        self._fps_counter = clock_gettime(CLOCK_MONOTONIC)
        self._video_on = False
        self._stop_compteur = None

    def start_video(self, analyser_virage=True):
        """
        La méthode start_video lance une boucle qui, tant que la variable
        d'instance privée video_on est vraie, lit une image, et lance
        son analyse grâce au module ImageClass.

        Parameters
        ----------
        analyser_virage : bool
            On réalise l'analyse du virage et on active l'autonomie du robot
            si `analyser_virage` est _True_, sinon on envoi juste l'image
            au client connecté sans rien faire.

        Returns
        ------
        void

        Notes
        -----
        Il est recommandé d'exécuter cette fonction en parallèle afin de ne pas
        bloquer le programme.
        """

        if conf("debug.general"):
            print("start video ", self._video_on)

        while self._video_on:
            if conf("debug.FPS"):
                heure = clock_gettime(CLOCK_MONOTONIC)
                print(1 / (heure - self._fps_counter), "FPS")
                self._fps_counter = heure
            image = Image(self.lire_image())
            image.send(Serveur.VIDEO_SOCKET)
            if analyser_virage:
                self.analyser(image)

        moteur.do("stop")

    def lire_image(self):
        """
        Lit une image depuis le flux vidéo

        Returns
        ------
        ndarray
            L'image lue
        """
        ret, img = self._cap.read()      # Récuperer le flux
        if ret is False:                 # Si jamais il y a un erreur
            exit("Impossible de joindre la caméra")
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
            for i in range(conf("network.reboot_time")):
                print("Redémarrage dans", 5 - i, "secondes")
                sleep(1)
            self.start_serveur()
        except (KeyboardInterrupt, InterruptedError):
            print("Arrêt du serveur")

    def actionOnFin(self, temps_max=conf('robot.wait_before_stop')):
        """
        Action à effectuer lorsque la voiture ne détecte pas de ligne.

        Parameters
        ----------
        temps_max : float
            Temps en secondes avant arrêt total

        Returns
        -------
        void
            Rien.

        Notes
        -----
        Logique : On laisse le robot pendant un certain temps encore rouler
        afin de lui laisser une petite chance de retrouver la ligne.
        Ce temps passé, on arrête le robot.
        """

        maintenant = clock_gettime(CLOCK_MONOTONIC)

        if self._stop_compteur is None:
            self._stop_compteur = maintenant
        elif self._stop_compteur + temps_max > maintenant:
            if conf('debug.general'):
                print("Il reste ",
                      temps_max + 1 - maintenant + self._stop_compteur)
        else:
            if conf('debug.general'):
                print("Arrêt du moteur")
            moteur.do("stop")

        if conf("debug.general"):
            print("Pas de ligne détéctée")

    def analyser(self, image):
        """
        Analyse d'image et prise de décision

        Parameters
        ----------
        image: Image
            L'image non-traitée

        Returns
        -------
        void
            Rien.
        """
        if image.isFin():
            if conf("debug.image.log"):
                image.log("isfin")
            self.actionOnFin()
        else:
            self._stop_compteur = None
            if image.isSurex():
                if conf("debug.image.surex"):
                    print("Is surex")
                if conf("debug.image.log"):
                    image.log("surex")

                image.preTraitementSurex()
            else:
                if conf("debug.image.surex"):
                    print("Not surex")
                image.preTraitementPasSurex()

            mat = SimpleImage(image.get3x3())
            angle, msg_log = prendre_decision(*mat.max_lines(), mat.mat)

            servo_dir.angle(angle)

            if conf("debug.image.log"):
                print("[{}] -> {}\t- image : {}".format(
                    msg_log, angle, image.log("MaxV3")
                ))

            moteur.do("run")

    def __del__(self):
        # Libération des ressources
        pass


if __name__ == '__main__':
    robot = Robot()
    robot.start_serveur()
