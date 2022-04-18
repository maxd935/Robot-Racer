"""
AbstractMoteur
"""

from Adafruit_PCA9685 import PCA9685
from time import sleep
from threading import Thread, Lock
from config import get as conf


class AbstractMoteur:
    """
    La classe AbstractMoteur représente un tout moteur que l'on cherche à
    contrôler par PWM et branché sur la carte PCA9685.


    Attributes
    ----------
    canal : int
        Canal du PWM sur la PCA9685
    rapport_cyclique_min : int
        Nombre de division minimale sur une résolution de 4096
    rapport_cyclique_max : int
        Nombre de division maximale sur une résolution de 4096
    charge : int
        Charge en pourcentage compris entre 0 et 100
    pwm : PCA9685
        Carte PCA9685
    verrou : Lock
        Verrou permettant l'exclusivité d'un thread sur la PCA9685
    """
    verrou = Lock()
    pwm = PCA9685()

    def __init__(self,
                 rapport_cyclique_min,
                 rapport_cyclique_max,
                 canal):
        self._rapport_cyclique_min = rapport_cyclique_min
        self._rapport_cyclique_max = rapport_cyclique_max
        self._canal = canal
        self._charge = None

    @property
    def charge(self):
        """ Getter pour la dernière charge utilisée """
        return self._charge

    @charge.setter
    def charge(self, pourcentage):
        """
        Définit une nouvelle charge pour le moteur.

        Parameters
        ----------
        pourcentage : int
            Nouvelle charge compris entre 0 et 100

        Returns
        ------
        void
            Rien.
        """
        if pourcentage > 100:
            pourcentage = 100
        elif pourcentage < 0:
            pourcentage = 0
        else:
            pourcentage = int(pourcentage)

        if self._charge is not pourcentage:
            self._charge = pourcentage
            etendue = self._rapport_cyclique_max - self._rapport_cyclique_min
            rapport_cyclique = int(self._rapport_cyclique_min + etendue * pourcentage / 100)

            AbstractMoteur.Launcher(rapport_cyclique, self._canal).start()

    class Launcher(Thread):
        """
        La clase Launcher sert exclusivement à lancer des actions sur la
        carte PWM9685.

        Attributes
        ----------
        _attente : int
            Attente en seconde avant de lancer
        _rapport : int
            Nouveau rapport compris entre 0 et 4096
        _canal : int
            Canal sur lequel définir le rapport

        """
        def __init__(self, rapport, canal, attente=0):
            super().__init__()
            self._attente = attente
            self._rapport = rapport
            self._canal = canal

        def run(self):
            """ Méthode héritée de Thread """
            if self._attente > 0:
                sleep(self._attente)

            AbstractMoteur.verrou.acquire()
            if conf("debug.controle"):
                print("@", self._canal, "\tset_pwm(", self._canal, ", ",
                      0, ", ", self._rapport, ")")
            AbstractMoteur.pwm.set_pwm(self._canal, 0, self._rapport)
            AbstractMoteur.verrou.release()
