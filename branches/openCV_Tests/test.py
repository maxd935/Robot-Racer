import cv2
import sys
import numpy

tailleImage = (6, 6)
tailleFenetre = (600, 600)
secondPointY = 0.6


def traiterImage(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                      # Conversion B&W
    ret, img_binary = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)  # Seuillage
    return img_binary

def afficherImage(image):
    cv2.namedWindow( "fenetreImage", cv2.WINDOW_NORMAL);    # Création de la fenêtre
    cv2.imshow('fenetreImage',image)                        # Affichage de l'image dans la fenêtre
    cv2.resizeWindow('fenetreImage', tailleFenetre)         # Agrandissement de la fenêtre            

def resizeImage(image):
    return cv2.resize(image, tailleImage)        # Pixelliser en taille x taille pixels

def trouver_milieu(ligne):
    longueur = len(ligne)
    start = None
    end = None

    for i in range(0, longueur):
        if start is None:
            if ligne[i] == 0:
                start = i
        elif end is None:
            if ligne[i] == 255:
                end = i
        else:
            break
    
    return int(start + (end - start) / 2) if start and end else -1

def trouverAngle(image):
    ymax = len(image) - 1
    ligne_index = int(ymax * (1 - secondPointY))
    
    mil_bottom = trouver_milieu(image[ymax])
    
    mil_dist = -1
    while mil_dist == -1:
        mil_dist = trouver_milieu(image[ligne_index])
        ligne_index -= 1
    
    image[ymax][mil_bottom] = 127
    image[ligne_index][mil_dist] = 127
    
    angle = numpy.arctan((mil_dist - mil_bottom)/(ymax - ligne_index)) * 180/numpy.pi

    return image, angle
    

def lancerCapture():
    cap = cv2.VideoCapture(0)
    while(True):
        imageOriginale = cv2.imread("plan.jpg", cv2.IMREAD_COLOR);
        """
        ret, imageOriginale = cap.read()            # Récuperer le flux
        if ret is False :                           # Si jamais il y a un erreur
            sys.exit(1)                             # On sort
        """

        imageTraitee = traiterImage(resizeImage(imageOriginale)) # On traite l'image

        imageTraitee, angle = trouverAngle(imageTraitee)
        
        print("Angle : ", angle)
        
        afficherImage(imageTraitee)                 # On l'affiche
        
        if cv2.waitKey(1) & 0xFF == ord('q'):       # On doit appuyer sur "q" pour quitter
            break

    # Libération des ressources
    cap.release()
    cv2.destroyAllWindows()

# C'est parti !
lancerCapture()
