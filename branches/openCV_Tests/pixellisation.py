import cv2
import sys
import numpy
from matplotlib import pyplot as plt

tailleImage = (32, 24)
tailleFenetre = (600, 600)
secondPointY = 0.6
quantification = 3

def traiterImage(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                      # Conversion B&W
    #img_quantifie = numpy.round(img_gray*(quantification/255))*(255/quantification)                      # Conversion B&W
    #ret, img_binary = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)  # Seuillage
    return img_gray

def afficherImage(image):
    cv2.namedWindow( "fenetreImage", cv2.WINDOW_NORMAL);    # Création de la fenêtre
    cv2.imshow('fenetreImage',image)                        # Affichage de l'image dans la fenêtre
    cv2.resizeWindow('fenetreImage', tailleFenetre)         # Agrandissement de la fenêtre

def resizeImage(image):
    return cv2.resize(image, tailleImage)        # Pixelliser en taille x taille pixels


def lancerCapture():
    cap = cv2.VideoCapture(0)

    imageOriginale = cv2.imread("plan.jpg", cv2.IMREAD_COLOR);
    """
    ret, imageOriginale = cap.read()            # Récuperer le flux
    if ret is False :                           # Si jamais il y a un erreur
        sys.exit(1)                             # On sort
    """

    imageTraitee = traiterImage(resizeImage(imageOriginale)) # On traite l'image

    # Valeur du milieu
    # idx = numpy.where(ligne == 0)[0].ravel()  # Tableau des index des pixels = 0

    # Somme des éléments de k à n
    # somme_idx = (idx[0] * ( 1 - idx[0]) + idx[-1] * ( 1 + idx[-1])) / 2
    # if somme_idx == tab.sum()
    # numpy.median(numpy.where(ligne == 0)[0].ravel())


    afficherImage(imageTraitee)                 # On l'affiche

    cv2.waitKey(0)

    # Libération des ressources
    cap.release()
    cv2.destroyAllWindows()

# C'est parti !
lancerCapture()
