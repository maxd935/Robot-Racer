"""
DCMoteur
"""

import RPi.GPIO as GPIO
from config import get as conf
from .AbstractMoteur import AbstractMoteur


class DCMoteur(AbstractMoteur):

    """
    La classe DCMoteur représente un moteur DC

    Attributes
    ----------
    _pin_negatif : int
        Pin sur le Raspberry correspondant à un des fils du moteur
    _pin_positif : int
        Pin sur le Raspberry correspondant à l'autre fil du moteur
    _sens : bool
        Vrai = avant, Faux = arrière
    _changement_sens : bool
        Vrai = Changé de sens récemment, il va falloir bientôt actualiser le
        sens, Faux = Rien de spécial.

    """

    def __init__(self, canal, pin_negatif, pin_positif):
        super().__init__(0, 4095, canal)
        if conf("debug.controle"):
            print("DCMoteur: créé : ", self)
        self._pin_negatif = pin_negatif
        self._pin_positif = pin_positif
        self._sens = True
        self._changement_sens = True
        GPIO.setup(self._pin_negatif, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pin_positif, GPIO.OUT, initial=GPIO.LOW)

    def inverser(self):
        """
        Inverser le sens du moteur

        Notes
        -----
        Le sens du moteur est inversé *logiquement*, mais il ne changera de
        sens réellement qu'a l'appel de la fonction `run()`.
        """
        if conf("debug.controle"):
            print("DCMoteur ", self, ": Inversion de sens ")
        self._sens = not self._sens
        self._changement_sens = True

    def stop(self):
        """ Arrêter le moteur """
        GPIO.output(self._pin_negatif, GPIO.LOW)
        GPIO.output(self._pin_positif, GPIO.LOW)
        self._changement_sens = True

    def freiner(self):
        """ Arrêt en mettant le moteur en position dynamo """
        GPIO.output(self._pin_negatif, GPIO.HIGH)
        GPIO.output(self._pin_positif, GPIO.HIGH)

    def run(self, pourcentage=conf("controle.moteur.regime_courant")):
        """
        Démarrer le moteur.

        Attributes
        ----------
        pourcentage : int
            Pourcentage compris entre 0 et 100 définissant la puissance désirée
        """
        if type(pourcentage) is str:
            print("pourcentage = ", pourcentage)
            pourcentage = int(pourcentage)
        if self._changement_sens:
            GPIO.output(self._pin_negatif, GPIO.LOW if self._sens else GPIO.HIGH)
            GPIO.output(self._pin_positif, GPIO.HIGH if self._sens else GPIO.LOW)
            self._changement_sens = False

        self.charge = pourcentage


class GroupeDCMoteur:
    """
    Groupe de moteurs
    Cette classe est un container pour les DC moteurs afin d'executer
    une fonction sur les deux moteurs à la fois.

    Attributes
    ----------
    _moteurs : iterable
        Liste des moteurs sur lesquels on veut appliquer par la suite des fcts.

    """

    def __init__(self, *moteurs):
        self._moteurs = moteurs

    def do(self, func, *args, **params):
        """
        Execute une méthode sur tous les moteurs de self._moteurs
        """
        return [getattr(obj, func)(*args, **params) for obj in self._moteurs]
