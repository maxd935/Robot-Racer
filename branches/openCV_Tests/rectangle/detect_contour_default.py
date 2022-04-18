import cv2
import numpy as np

tailleImage = (64, 48)
tailleFenetre = (600, 600)
secondPointY = 0.6
quantification = 255

cap = cv2.VideoCapture(0)
cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)

# C'est parti !
img = cv2.imread("img.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, tailleImage)
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, 2)
cnt = contours[0]
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
img2 = cv2.drawContours(img, [box], 0, 127, 1)

cv2.imshow('fenetreImage', img2)
cv2.waitKey(0)

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
