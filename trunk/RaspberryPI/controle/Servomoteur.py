# coding=UTF-8


"""
    ServoMoteur
"""

from .AbstractMoteur import AbstractMoteur
from config import get as conf


class Servomoteur(AbstractMoteur):
    """
    Représentation d' un servomoteur.

    Attributes
    ----------
    _angle_min : int
        angle minimal autorisé par le servo
    _angle_max : int
        angle maximal autorisé par le servo
    _angle_correction : int
        angle dit de *correction* car il permet d'ajuster le 0 avec le 0 de la
        réalité et raisonner par la suite avec des angles relatifs.
    _angle_initial : int
        angle pris par le servo à son initialisation.
    _angle_courant : int
        angle courant du servo

    Notes
    -----
    Les angles sont compris entre -90 et 90 degrés.
    """

    def __init__(self, initial, correction, angle_min, angle_max, canal):
        super().__init__(conf("controle.servo.periode_min"),
                         conf("controle.servo.periode_max"), canal)
        if conf("debug.controle"):
            print("Servomoteur: créé : ", self)
        self._angle_min = angle_min
        self._angle_max = angle_max
        self._angle_correction = correction
        self._angle_initial = initial
        self._angle_courant = self._angle_initial
        self.calibrer()

    def angle(self, angle=None):
        """
        Regle l'angle du servo compris entre _angle_min et _angle_max

        Parameters
        ----------
        angle : int or None
            L'angle en degré. Si none, ne change rien : agit comme un getter

        Returns
        -------
        int
            L'angle courant après changement si il y a eu changement

        Notes
        -----
        calcul de la charge :
          etendue = SERVO_MAX - SERVO_MIN
          degre = etendue / 180
          pwm = SERVO_MIN + etendue/2 + degre * angle
          res = (pwm - SERVO_MIN) / etendue
        """
        if angle is None:
            return self._angle_courant

        if conf("debug.controle"):
            print("Servomoteur ", self, ": ", angle, "°")
        if angle > self._angle_max:
            angle = self._angle_max
        elif angle < self._angle_min:
            angle = self._angle_min

        self._angle_courant = angle

        nouvelle_charge = 50 + (angle - self._angle_correction) / 1.8
        self.charge = nouvelle_charge
        return nouvelle_charge

    def adjust_angle(self, angle):
        """
        Règle l'angle relativement à l'angle courant

        Parameters
        ----------
        angle : int
            L'angle en degré
        """
        self.angle(angle + self._angle_courant)

    def calibrer(self):
        """
        Calibration - Initialisation du servomoteur
        """
        self._angle_courant = self._angle_initial
        self.angle(self._angle_initial)
