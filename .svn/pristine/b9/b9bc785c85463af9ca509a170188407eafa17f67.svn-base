import cv2
import numpy as np

tailleImage = (320, 240)
tailleFenetre = (600, 600)
speed = 10000

cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)
img = cv2.imread("plan.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, tailleImage)
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

done = False
size = np.size(img)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

while(not done):
    dilated = cv2.dilate(img, element)
    img = dilated.copy()
    print("dilated")
    cv2.imshow('fenetreImage', dilated)
    cv2.waitKey(speed)

    if cv2.countNonZero(img) == size:
        done = True

print("Fini !")
while True:
    cv2.imshow('fenetreImage', img)
    if cv2.waitKey(1) == ord('q'):
        break

# Libération des ressources
cv2.destroyAllWindows()
