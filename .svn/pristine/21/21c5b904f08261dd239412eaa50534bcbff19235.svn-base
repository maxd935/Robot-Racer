# coding=UTF-8


"""
    DCMoteur
"""

import RPi.GPIO as GPIO
from .AbstractMoteur import AbstractMoteur


class DCMoteur(AbstractMoteur):

    """
    ATTRIBUTES



    pin_negatif    (private)
    pin_positif    (private)
    sens    (private)
    changement_sens    (private)

    """

    def __init__(self, canal, pin_negatif, pin_positif):
        super().__init__(0, 4095, canal)
        self._pin_negatif = pin_negatif
        self._pin_positif = pin_positif
        self._sens = True
        self._changement_sens = True
        GPIO.setup(self._pin_negatif, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin_positif, GPIO.OUT, initial=GPIO.LOW)

    def inverser(self):
        """ Inverser le sens du moteur """
        self._sens = not self._sens
        self._changement_sens = True

    def stop(self):
        """ Arrêter le moteur """
        GPIO.output(self._pin_negatif, GPIO.LOW)
        GPIO.output(self._pin_positif, GPIO.LOW)

    def freiner(self):
        """ Arrêt en mettant le moteur en position dynamo """
        GPIO.output(self._pin_negatif, GPIO.HIGH)
        GPIO.output(self._pin_positif, GPIO.HIGH)

    def run(self):
        """ Mettre à pleine puissance le moteur """
        if self._changement_sens:
            GPIO.output(self._pin_negatif, GPIO.LOW if self._sens else GPIO.HIGH)
            GPIO.output(self._pin_positif, GPIO.HIGH if self._sens else GPIO.LOW)
            self._changement_sens = False

        self.charge = 35


class GroupeDCMoteur:
    """
    Groupe de moteurs

    ATTRIBUTES


    moteurs    (private)

    """

    def __init__(self, *moteurs):
        self._moteurs = moteurs

    def do(self, func, *args, **params):
        """ Execute une méthode sur tous les moteurs """
        return [getattr(obj, func)(*args, *params) for obj in self._moteurs]
