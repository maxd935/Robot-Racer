import cv2
import numpy as np


# relevee3.avi      PASS
# flash_baisse.avi  PASS
# flashreleve.avi   FAIL
# penchee2          PASS


cap = cv2.VideoCapture("relevee2.avi")
if not cap.isOpened():
    print("Erreur bus")


cv2.namedWindow("video", cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', (640, 480))
cv2.moveWindow('video', 0, 0)

cv2.namedWindow("traite", cv2.WINDOW_NORMAL)
cv2.resizeWindow('traite', (640, 480))
cv2.moveWindow('traite', 640, 0)

cv2.namedWindow("intermediaire", cv2.WINDOW_NORMAL)
cv2.resizeWindow('intermediaire', (640, 480))
cv2.moveWindow('intermediaire', 0, 480)

cv2.namedWindow("equalized", cv2.WINDOW_NORMAL)
cv2.resizeWindow('equalized', (640, 480))
cv2.moveWindow('equalized', 640, 480)


def traite(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # img_ori = cv2.equalizeHist(img_ori)
    img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow("intermediaire", img)

    size = len(img)
    ligne_split = int(size * 0.5)
    rect0 = (0, 0, 0)
    rect1 = (0, 0, 0)

    im2, contours, hierarchy = cv2.findContours(img[0:ligne_split], cv2.RETR_CCOMP, 2)


    selec = None
    if contours is not None and len(contours) > 0:
        selec = max(contours, key=cv2.contourArea)

    if selec is not None:
        rect0 = cv2.minAreaRect(selec)
        box = np.int0(cv2.boxPoints(rect0))
        img = cv2.drawContours(img, [box], 0, 127, 3)

    im2, contours, hierarchy = cv2.findContours(img[ligne_split:size], cv2.RETR_CCOMP, 2)

    selec = None
    if contours is not None and len(contours) > 0:
        selec = max(contours, key=cv2.contourArea)
    if selec is not None:
        rect1 = cv2.minAreaRect(selec)
        (cx, cy), size, angle = rect1
        rect1 = (cx, cy + ligne_split), size, angle
        box = np.int0(cv2.boxPoints(rect1))
        img = cv2.drawContours(img, [box], 0, 127, 3)


    cv2.imshow("equalized", img)
    return img

quit = False
while not quit:
    while True:
        # Capture each frame of webcam video
        ret, frame = cap.read()
        cv2.imshow("video", frame)
        cv2.imshow("traite", traite(frame))
        if cv2.waitKey(50) == ord('q'):
            quit = True
            break

cap.release()
cv2.destroyAllWindows()
