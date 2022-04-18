import cv2
import numpy as np


# relevee3.avi      PASS    BIEN
# flash_baisse.avi  FAIL
# flashreleve.avi   FAIL
# penchee2          PASS    MOYEN


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
    img_ori = cv2.equalizeHist(img_ori)
    img_inutile, contours, hierarchy = cv2.findContours(
        cv2.threshold(img_ori, 60, 255, cv2.THRESH_BINARY_INV)[1],  # 100
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    imageContours = np.zeros_like(img_ori)
    imageContours = cv2.drawContours(imageContours, contours, -1, 255, 1)
    imageContours = cv2.GaussianBlur(imageContours, (9, 9), 0)  # 13
    # imageContours = cv2.dilate(imageContours, np.ones((9, 9), np.uint8))

    cv2.imshow("equalized", img_ori)
    cv2.imshow("intermediaire", imageContours)

    imageLigne = np.zeros_like(img_ori)
    longueur_min = 1
    gap = 150
    lines = cv2.HoughLinesP(imageContours, 1, np.pi / 180, 180,
                            longueur_min, gap)

    if lines is None:
        return imageContours
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(imageLigne, (x1, y1), (x2, y2), 127, 4)

    return imageLigne

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
