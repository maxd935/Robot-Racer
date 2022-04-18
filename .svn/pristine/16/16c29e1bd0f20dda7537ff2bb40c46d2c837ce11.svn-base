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

    img_inutile, contours, hierarchy = cv2.findContours(
        cv2.threshold(img_ori, 60, 255, cv2.THRESH_BINARY_INV)[1],
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    imageContours = np.zeros_like(img_ori)
    imageContours = cv2.drawContours(imageContours, contours, -1, 255, 1)

    cv2.imshow("equalized", img_ori)
    cv2.imshow("intermediaire", imageContours)

    perimMax = cv2.arcLength(contours[0], True)
    contoursMax = contours[0]

    for i in contours:
        perim = cv2.arcLength(i, True)
        if perim > perimMax:
            perimMax = perim
            contoursMax = i

    rect = cv2.minAreaRect(contoursMax)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    imageContours = cv2.drawContours(imageContours, [box], 0, 127, 3)

    return imageContours

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
