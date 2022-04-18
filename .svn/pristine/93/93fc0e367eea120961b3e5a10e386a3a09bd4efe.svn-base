import cv2
import numpy as np
import time

cv2.namedWindow("video", cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', (640, 480))
cv2.moveWindow('video', 0, 0)


def findTreshHold(img_ori):
    size = np.size(img_ori)
    for tresh in range(10, 200, 5):
        ret, img = cv2.threshold(img_ori, tresh, 255, cv2.THRESH_BINARY_INV)
        if cv2.countNonZero(img) / size > 0.15:
            return tresh
    print("fail")
    return -1


def shift_angle(img_ori):
    img_ori = cv2.cvtColor(img_ori, cv2.COLOR_RGB2GRAY)
    img_ori = cv2.threshold(img_ori, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cv2.imshow("video", img_ori)
    im2, contours, hierarchy = cv2.findContours(img_ori, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    selec = None
    if contours is not None and len(contours) > 0:
        selec = max(contours, key=cv2.contourArea)

    (cx, cy), (height, width), angle = rect = cv2.minAreaRect(selec)
    box = np.int0(cv2.boxPoints(rect))
    img_ori = cv2.drawContours(img_ori, [box], 0, 127, 1)

    # print(box)
    # cv2.imshow("video", img_ori)
    # cv2.waitKey(0)

    shift = 0
    angle = 0

    colsort = lambda a, b=0 : a[a[: , b].argsort()]

    # print(np.array(box))
    # b2 = np.array([[1,4],[3,1]])
    # b2.sort(axis=1)
    # print(b2)
    box2 = colsort(box, 1)
    # print(colsort(box2[0:2]))
    # print(colsort(box2[2:4]))
    (h1, h2), (b1, b2) = colsort(box2[0:2]), colsort(box2[2:4])

    # print(b1, b2, h1, h2)
    # cv2.waitKey(0)

    mhx, mhy = (h1[0] + (h2[0] - h1[0]) / 2,
                h1[1] + (h2[1] - h1[1]) / 2)
    mbx, mby = (b1[0] + (b2[0] - b1[0]) / 2,
                b1[1] + (b2[1] - b1[1]) / 2)

    a = (mhy - mby) / (mhx - mbx)
    # print(a)
    if np.abs(a) < 50 and np.abs(a) > 0.01:
        angle = np.arctan(a) * 180 / np.pi + 90
        xmax = len(img_ori[0])
        ymax = len(img_ori)
        b = cy - a * cx

        xprime, yprime = (ymax - b) / a, ymax

        shift = int(100 * (2 * xprime / xmax - 1))
        print(angle)
        cv2.line(img_ori, (int(cx), int(cy)), (int(xprime), int(yprime)), 200, 1)
        if a > 0:
            angle = 180 - angle
    else:
        angle = 0

    cv2.imshow("video", img_ori)

    # print((shift, angle), "( angle=" , angle, ", ", np.abs(angle % 90) > 2., ")")
    return (shift, angle)


def seuiller_shift_angle(shift, angle):
    if np.abs(shift) < 15:
        # print("Shift NULL")
        shift = 0
    if np.abs(angle) < 30:
        angle = 0
    return (shift, angle)


cap = cv2.VideoCapture("../../openCV_Tests/video/relevee3.avi")
if not cap.isOpened():
    print("Erreur bus")
while True:
    # Capture each frame of webcam video
    ret, frame = cap.read()
    if not ret:
        cv2.VideoCapture.set(cap, cv2.CAP_PROP_POS_AVI_RATIO, 0)
        print("Redémarrage vidéo")
        continue

    frame = cv2.resize(frame, (44, 33))
    frame = cv2.flip(frame, 1)
    shift, angle = seuiller_shift_angle(*shift_angle(frame))
    print("Tourner : ", angle)
    # if angle != 0:
    #     print("angle ", angle)
    # elif shift != 0:
    #     print("shift ", angle)
    # else:
    #     print("rien")
    time.sleep(0.02)
    if cv2.waitKey(3000) == ord('q'):
        quit = True
        break

cap.release()
cv2.destroyAllWindows()
