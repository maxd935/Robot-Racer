from .DCMoteur import DCMoteur, GroupeDCMoteur
from .Servomoteur import Servomoteur
from .AbstractMoteur import AbstractMoteur
from config import get as conf
from RPi.GPIO import setmode, setwarnings, BOARD

setmode(BOARD)
setwarnings(False)
AbstractMoteur.pwm.set_pwm_freq(conf("controle.pwm_frequence"))


moteur1 = DCMoteur(conf("controle.moteur.gauche.channel"),
                   *conf("controle.moteur.gauche.pins"))

moteur2 = DCMoteur(conf("controle.moteur.droit.channel"),
                   *conf("controle.moteur.droit.pins"))

servo_x = Servomoteur(conf("controle.servo.camera.X.initial"),
                      conf("controle.servo.camera.X.correction"),
                      conf("controle.servo.camera.X.min"),
                      conf("controle.servo.camera.X.max"),
                      conf("controle.servo.camera.X.channel"))

servo_y = Servomoteur(conf("controle.servo.camera.Y.initial"),
                      conf("controle.servo.camera.Y.correction"),
                      conf("controle.servo.camera.Y.min"),
                      conf("controle.servo.camera.Y.max"),
                      conf("controle.servo.camera.Y.channel"))

servo_dir = Servomoteur(conf("controle.servo.direction.initial"),
                        conf("controle.servo.direction.correction"),
                        conf("controle.servo.direction.min"),
                        conf("controle.servo.direction.max"),
                        conf("controle.servo.direction.channel"))

moteur = GroupeDCMoteur(moteur1, moteur2)
