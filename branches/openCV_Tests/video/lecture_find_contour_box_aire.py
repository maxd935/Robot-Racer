import cv2
import numpy as np


# relevee3.avi      PASS
# flash_baisse.avi  PASS
# flashreleve.avi   FAIL
# penchee2          PASS



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


def findTreshHold(img_ori):
    size = np.size(img_ori)
    for tresh in range(10, 200, 5):
        ret, img = cv2.threshold(img_ori, tresh, 255, cv2.THRESH_BINARY_INV)
        if cv2.countNonZero(img) / size > 0.15:
            return tresh
    print("fail")
    return -1


def traite(img_ori):
    img_ori = cv2.cvtColor(img_ori, cv2.COLOR_RGB2GRAY)
    # img_ori = cv2.equalizeHist(img_ori)
    img_ori = cv2.threshold(img_ori, findTreshHold(img_ori), 255, cv2.THRESH_BINARY_INV)[1]
    im2, contours, hierarchy = cv2.findContours(img_ori, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    selec = None
    if contours is not None and len(contours) > 0:
        selec = max(contours, key=cv2.contourArea)

    imageContours = np.zeros_like(img_ori)
    imageContours = cv2.drawContours(imageContours, contours, -1, 255, 1)

    cv2.imshow("equalized", img_ori)
    cv2.imshow("intermediaire", imageContours)

    rect = cv2.minAreaRect(selec)
    if np.abs(rect[2] % 90) > 2.:
        # Calcul détaillé :
        #
        # a = np.tan((90 + rect[2]) * np.pi / 180)
        # cx = rect[0][0]
        # cy = rect[0][1]
        # b = cy - a * cx
        # yprime = ymax
        # xprime = (ymax - b) / a
        #
        # shift = (xprime - xmax / 2) * 100 / xmax
        # print(shift)
        # cv2.line(imageContours, (int(cx), int(cy)), (int(xprime), int(yprime)), 127, 5)
        angle = np.tan((90 + rect[2]) * np.pi / 180)
        xmax = len(img_ori[0])
        shift = int((((len(img_ori) - (rect[0][1] - angle * rect[0][0])) / angle) - xmax / 2) * 100 / xmax)
        print(shift)

    box = cv2.boxPoints(rect)
    box = np.int0(box)
    imageContours = cv2.drawContours(imageContours, [box], 0, 127, 3)

    return imageContours

quit = False
while not quit:

    cap = cv2.VideoCapture("relevee3.avi")
    if not cap.isOpened():
        print("Erreur bus")

    while True:
        # Capture each frame of webcam video
        ret, frame = cap.read()
        cv2.imshow("video", frame)
        cv2.imshow("traite", traite(frame))
        if cv2.waitKey(50) == ord('q'):
            quit = True
            break

    cap.release()

cap.release()
cv2.destroyAllWindows()
