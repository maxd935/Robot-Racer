import cv2
import numpy as np
import time

cv2.namedWindow("video", cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', (640, 480))
cv2.moveWindow('video', 0, 0)


def shift_angle(img_ori):
    img_ori = cv2.cvtColor(img_ori, cv2.COLOR_RGB2GRAY)
    img_ori = cv2.threshold(img_ori, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    im2, contours, hierarchy = cv2.findContours(img_ori, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    selec = None
    if contours is not None and len(contours) > 0:
        selec = max(contours, key=cv2.contourArea)

    (cx, cy), (height, width), angle = rect = cv2.minAreaRect(selec)
    b2, b1, h1, h2 = box = np.int0(cv2.boxPoints(rect))
    img_ori = cv2.drawContours(img_ori, [box], 0, 127, 1)

    shift = 0
    angle = rect[2]

    mhx, mhy = mh = (h1[0] + (h2[0] - h1[0]) / 2,
          h1[1] + (h2[1] - h1[1]) / 2)
    mbx, mby = mb = (b1[0] + (b2[0] - b1[0]) / 2,
          b1[1] + (b2[1] - b1[1]) / 2)

    a = (mhy - mby) / (mhx - mbx)

    angle = np.arctan(a) * 180 / np.pi + 90

    if np.abs(angle % 90) > 2.:
        xmax = len(img_ori[0])
        ymax = len(img_ori)
        b = cy - a * cx

        xprime, yprime = (ymax - b) / a, ymax

        shift = int(100 * (2 * xprime / xmax - 1))

        print("angle = ", angle)
        print("xmax = ", xmax)
        print("ymax = ", ymax)
        print("center = ", rect[0])
        print("y = ", a, "*x + ", b)
        print("(x', y') = ", (xprime, yprime))
        print("shift = ", shift)

        cv2.line(img_ori, (int(cx), int(cy)), (int(xprime), int(yprime)), 200, 1)
        cv2.imshow("video", img_ori)
        cv2.waitKey(0)

    cv2.imshow("video", img_ori)
    cv2.waitKey(0)

    print((int(shift), int(angle)), angle, " et ", np.abs(angle % 90) > 2.)
    return (int(shift), int(angle))


frame = cv2.imread("binary_sens3.png")
frame = cv2.resize(frame, (44, 33))
shift, angle = shift_angle(frame)
cv2.destroyAllWindows()
