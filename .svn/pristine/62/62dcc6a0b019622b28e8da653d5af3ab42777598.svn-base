import cv2
import numpy as np


# relevee3.avi      PASS    BIEN
# flash_baisse.avi  PASS    MOYEN
# flashreleve.avi   FAIL
# penchee2          PASS


cap = cv2.VideoCapture("relevee3.avi")
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
    img_ori = cv2.threshold(img_ori, 100, 255, cv2.THRESH_BINARY_INV)[1]
    img_ori = cv2.GaussianBlur(img_ori, (9, 9), 0)
    imageContours = np.zeros_like(img_ori)
    imageContours = cv2.Canny(img_ori, 0, 170)
    imageContours = cv2.dilate(imageContours, np.ones((9, 9), np.uint8))

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
