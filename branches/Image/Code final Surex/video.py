import cv2
from ImageClass import Image
import time


class Video:

    FPS = 20

    def __init__(self, video):
        cv2.namedWindow("video", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('video', (640, 480))
        cv2.moveWindow('video', 500, 0)
        self.FILENAME = video

    def lecture(self):
        quit = False
        try:
            while not quit:
                cap = cv2.VideoCapture(self.FILENAME)
                if not cap.isOpened():      # Verifacation du constructeur VideoCapture
                    print("Erreur bus")

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        # not Ret = True => Fin Video
                        # Remettre la video du debut
                        cv2.VideoCapture.set(cap, cv2.CAP_PROP_POS_AVI_RATIO, 0)
                        print("\n*****Redémarrage vidéo*****\n")
                        print("Attente 3 secondes")
                        time.sleep(3)
                        continue

                    # Traitement de l'image
                    img = Image(frame)
                    #img.resizeImage()
                    # if img.isFin():
                    #     pass    # Commande Controle arretez moteur
                    ## if img.isSurex():
                    #     pass    # Commande Traitement ImageSurex
                    # img.traitement()
                    ##if not img.isFin() and not img.isSurex():
                        ##img.traitement()

                    cv2.imshow("video", img.getImage())


    


                    print("\n*****Pres q pour quitter*****\n")
                    if cv2.waitKey(int(1000 * (1 / self.FPS))) == ord("q"):
                        cv2.destroyAllWindows()
                        quit = True                        
                        break

            cap.release()

        except KeyboardInterrupt:
            print("stop")
            cap.release()


# Test 
#Attention chemin des videos 
Video("flash_baisse.avi").lecture()
Video("flash2.avi").lecture()
Video("flashreleve.avi").lecture()
Video("penchee1.avi").lecture()
Video("penchee2.avi").lecture()
Video("relevee3.avi").lecture()
