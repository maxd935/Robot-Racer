import cv2
import numpy as np


# relevee3.avi      PASS
# flash_baisse.avi  PASS
# flashreleve.avi   FAIL
# penchee2          PASS


cap = cv2.VideoCapture("flash_baisse.avi")
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


def traite(img_ori):
    img_ori = cv2.cvtColor(img_ori, cv2.COLOR_RGB2GRAY)
    # img_ori = cv2.equalizeHist(img_ori)

    img_bin = cv2.threshold(img_ori, 80, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow("intermediaire", img_bin)

    size = np.size(img_ori)
    skel = np.zeros(img_ori.shape, np.uint8)
    done = False
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    while(not done):
        eroded = cv2.erode(img_bin, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img_bin, temp)
        skel = cv2.bitwise_or(skel, temp)
        img_bin = eroded.copy()

        zeros = size - cv2.countNonZero(img_bin)
        if zeros == size:
            done = True

    cv2.imshow("equalized", img_ori)

    return skel

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
