import cv2
from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from sys import argv

INET_ADDR = "127.0.0.1"
PORT = 45655 if len(argv) <= 1 else argv[1]
WIDTH = 160
HEIGHT = 120
FPS = 20

sock = socket(AF_INET, SOCK_DGRAM)
timesleep = 1 / FPS

quit = False
try:
    while not quit:

        cap = cv2.VideoCapture("relevee3.avi")
        if not cap.isOpened():
            print("Erreur bus")

        while True:
            ret, frame = cap.read()
            if not ret:
                cv2.VideoCapture.set(cap, cv2.CAP_PROP_POS_AVI_RATIO, 0)
                print("Redémarrage vidéo")
                continue
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            img = cv2.resize(img, (WIDTH, HEIGHT))
            ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)

            sock.sendto(img.tobytes(), (INET_ADDR, PORT))

            sleep(timesleep)
        cap.release()
except KeyboardInterrupt:
    print("stop")
    cap.release()
