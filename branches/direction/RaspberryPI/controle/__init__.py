from .DCMoteur import DCMoteur, GroupeDCMoteur
from .Servomoteur import Servomoteur
from .AbstractMoteur import AbstractMoteur
from .Configuration import *
from RPi.GPIO import setmode, setwarnings, BOARD

setmode(BOARD)
setwarnings(False)
AbstractMoteur.pwm.set_pwm_freq(PWM_FREQUENCE)


moteur1 = DCMoteur(DC_MOTOR_L_CHANNEL, MOTEUR_GAUCHE_PIN1, MOTEUR_GAUCHE_PIN2)
moteur2 = DCMoteur(DC_MOTOR_R_CHANNEL, MOTEUR_DROIT_PIN1, MOTEUR_DROIT_PIN2)

servo_x = Servomoteur(X_CAMERA_INITIAL,
                      X_CAMERA_CORRECTION,
                      X_CAMERA_MIN,
                      X_CAMERA_MAX,
                      X_CAMERA_CHANNEL)

servo_y = Servomoteur(Y_CAMERA_INITIAL,
                      Y_CAMERA_CORRECTION,
                      Y_CAMERA_MIN,
                      Y_CAMERA_MAX,
                      Y_CAMERA_CHANNEL)

servo_dir = Servomoteur(DIRECTION_INITIAL,
                        DIRECTION_CORRECTION,
                        DIRECTION_MIN,
                        DIRECTION_MAX,
                        DIRECTION_CHANNEL)

moteur = GroupeDCMoteur(moteur1, moteur2)

