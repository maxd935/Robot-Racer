import cv2

FPS = 20
FILENAME = "relevee3.avi"

cv2.namedWindow("video", cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', (640, 480))
cv2.moveWindow('video', 0, 0)

quit = False
try:
    while not quit:

        cap = cv2.VideoCapture(FILENAME)
        if not cap.isOpened():
            print("Erreur bus")

        while True:
            ret, frame = cap.read()
            if not ret:
                cv2.VideoCapture.set(cap, cv2.CAP_PROP_POS_AVI_RATIO, 0)
                print("Redémarrage vidéo")
                continue
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            # Traitement img

            cv2.imshow("video", img)

            if cv2.waitKey(int(1000 * (1 / FPS))) == ord("q"):
                quit = True
                break

        cap.release()

except KeyboardInterrupt:
    print("stop")
    cap.release()
