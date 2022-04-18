# coding=UTF-8


"""
    AbstractMoteur
"""

import Adafruit_PCA9685 as PCA9685
from time import sleep
from threading import Thread, Lock


class AbstractMoteur:
    """
    ATTRIBUTES

    canal    (private)
    rapport_cyclique_min    (private)
    rapport_cyclique_max    (private)
    charge    (private)

    pwm    (static)
    verrou    (static)
    """
    verrou = Lock()
    pwm = PCA9685.PCA9685()

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
        """ Getter pour la derniere charge utilisee """
        return self._charge

    @charge.setter
    def charge(self, pourcentage):
        """ Définit le pourcentage de charge du moteur

        @param int pourcentage :
        @return void   :
        """
        print("@", self._canal, "\t", int(pourcentage), "%")

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
        def __init__(self, rapport, canal, attente=0):
            super().__init__()
            self._attente = attente
            self._rapport = rapport
            self._canal = canal

        def run(self):
            if self._attente > 0:
                sleep(self._attente)

            AbstractMoteur.verrou.acquire()
            print("@", self._canal, "\tset_pwm(", self._canal, ", ",
                  0, ", ", self._rapport, ")")
            AbstractMoteur.pwm.set_pwm(self._canal, 0, self._rapport)
            AbstractMoteur.verrou.release()
