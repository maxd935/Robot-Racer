# coding=UTF-8


"""
    ServoMoteur
"""

from .AbstractMoteur import AbstractMoteur
from config import get as conf


class Servomoteur(AbstractMoteur):

    """
    ATTRIBUTES

    angle_initial    (private)
    angle_correction    (private)
    angle_min    (private)
    angle_max    (private)

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
        self.calibrer()

    def angle(self, angle):
        """ Regle un angle compris entre -45 et 45 degrés

        calcul de la charge :
          etendue = SERVO_MAX - SERVO_MIN
          degre = etendue / 180
          pwm = SERVO_MIN + etendue/2 + degre * angle
          res = (pwm - SERVO_MIN) / etendue

        @param int angle : L'angle en degré
        """

        if conf("debug.controle"):
            print("Servomoteur ", self, ": ", angle, "°")
        if angle > self._angle_max:
            angle = self._angle_max
        elif angle < self._angle_min:
            angle = self._angle_min

        nouvelle_charge = 50 + (angle - self._angle_correction) / 1.8
        self.charge = nouvelle_charge

    def calibrer(self):
        """ Calibration des servos """
        self.angle(self._angle_initial)
