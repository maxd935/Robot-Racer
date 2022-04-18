from image import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt


img = Image(cv2.imread("./assets/testAire/6.png"))


def test1():

    if(img.isSurex()):
        img.preTraitementSurex()
    else:
        img.preTraitementPasSurex()

    f = img._image_thresh


    # Coupe en 6 partie l'image afin d'analyser le image

    # Image couper au milieu a Gauche
    imMG = cv2.getRectSubPix(f,
                        (int(np.shape(f)[1]/3), int(np.shape(f)[0]/3)),
                        (int(np.shape(f)[1]/6), int(np.shape(f)[0]/2)))

    # Image couper au milieu a Droite
    imMD = cv2.getRectSubPix(f,
                        (int(np.shape(f)[1]/3), int(np.shape(f)[0]/3)),
                        (int(5*np.shape(f)[1]/6), int(np.shape(f)[0]/2)))

    # Image couper au milieu au Centre
    imM1 = cv2.getRectSubPix(f,
                        (int(np.shape(f)[1]/3), int(np.shape(f)[0]/3)),
                        (int(np.shape(f)[1]/2), int(np.shape(f)[0]/2)))



    # Image couper au en Bas au Centre
    imM0 = cv2.getRectSubPix(f,
                        (int(np.shape(f)[1]/3), int(np.shape(f)[0]/3)),
                        (int(np.shape(f)[1]/2), int(3*np.shape(f)[0]/4)))

    # Image couper en Bas a Gauche
    imG = cv2.getRectSubPix(f,
                        (int(np.shape(f)[1]/3), int(np.shape(f)[0]/3)),
                        (int(np.shape(f)[1]/6), int(3*np.shape(f)[0]/4)))

    # Image couper en Bas a Droite
    imD = cv2.getRectSubPix(f,
                        (int(np.shape(f)[1]/3), int(np.shape(f)[0]/3)),
                        (int(5*np.shape(f)[1]/6), int(3*np.shape(f)[0]/4)))


    nbrMG = cv2.countNonZero(cv2.threshold(imMG,125, 255, cv2.THRESH_BINARY)[1])
    nbrMD = cv2.countNonZero(cv2.threshold(imMD,125, 255, cv2.THRESH_BINARY)[1])
    #print(nbrMG, " ", nbrMD)

    nbrG = cv2.countNonZero(cv2.threshold(imG,125, 255, cv2.THRESH_BINARY)[1])
    nbrD = cv2.countNonZero(cv2.threshold(imD,125, 255, cv2.THRESH_BINARY)[1])
    #print(nbrG, " ", nbrD)

    nbrM0 = cv2.countNonZero(cv2.threshold(imM0,125, 255, cv2.THRESH_BINARY)[1])
    nbrM1 = cv2.countNonZero(cv2.threshold(imM1,125, 255, cv2.THRESH_BINARY)[1])
    #print(nbrG, " ", nbrD)


    # Calcul en pourcentage
    nMG = int((nbrMG*100)/ (np.shape(imMG)[0]*np.shape(imMG)[1]))
    nMD = int((nbrMD*100)/ (np.shape(imMD)[0]*np.shape(imMG)[1]))
    print(nMG, " ", nMD)

    nG = int((nbrG*100)/ (np.shape(imG)[0]*np.shape(imG)[1]))
    nD = int((nbrD*100)/ (np.shape(imD)[0]*np.shape(imG)[1]))
    print(nG, " ", nD)

    nM0 = int((nbrM0*100)/ (np.shape(imM0)[0]*np.shape(imM0)[1]))
    nM1 = int((nbrM1*100)/ (np.shape(imM1)[0]*np.shape(imM1)[1]))
    print(nM0, " ", nM1)

    if nM0 < 10:
        """
        Dans le cas ou le centre du Bas est Vide, la ligne est en diagonale
        (Si on a une ligne Horizontale, cela ne fonctionne plus :(  )
        Si la ligne est presente sur le milieu a droite ou a Gauche
            la voiture doit continuer tout droit pour ratrapper la ligne
        Sinon la ligne se trouve dans un coin en bas de l'image
            la voiture doit fortement Tourner du coté ou il appercoit la ligne jusqu'a
            retrouver la ligne
        """

        if nMG or nMD > 40:  # Si on detecte +de 20% de la ligne sur la partie du mileu sur un cote
            pass   # Go tout droit

        else:       # Sinon le centre du bas est Vide et la ligne n'est pas majoritaire sur le milieu
            pass  # Go fort du cote ou il y a la ligne

    else:  # La voiture est bien au centre de la ligne
        if nD or nG < 15:  # Leger debordement sur le cote de la ligne non significatif
            pass  # Tout droit

        else:  # Debordement conséquent sur un des cotés
            pass  # Calcul normal utilise dans la v1


    cv2.imshow("Tresh", f)
    cv2.imshow("imG", imG)
    cv2.imshow("imD", imD)
    cv2.imshow("imMG", imMG)
    cv2.imshow("imMD", imMD)
    cv2.imshow("imM0", imM0)
    cv2.imshow("imM1", imM1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test2():


    equ = cv2.equalizeHist(img._image)
    res = np.hstack((img._image, equ))
    cv2.imshow("res", res)
    cv2.imshow("equ", equ)


    """
    hist, bins = np.histogram(img._image, 256, [0, 256])
    print(1)
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    print(2)
    plt.hist(img._image, 256, [0, 256])
    print(3)
    plt.xlim([0, 256])
    plt.legend(('cdf', 'histogram'), loc='upper left')
    print(4)
    cv2.imshow("plt", cdf)
    cv2.imshow("img", hist)
    """
    cv2.waitKey(0)
    cv2.destroyAllWindows()


test1()
#test2()
