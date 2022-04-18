import cv2

tailleImage = (320, 240)
tailleFenetre = (600, 600)
speed = 10000

cv2.namedWindow("fenetreImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow('fenetreImage', tailleFenetre)
img = cv2.imread("plan.jpg", cv2.IMREAD_GRAYSCALE)
eroded = cv2.imread("eroded.png", cv2.IMREAD_GRAYSCALE)
dilated = cv2.imread("dilated.png", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, tailleImage)
eroded = cv2.resize(eroded, tailleImage)
dilated = cv2.resize(dilated, tailleImage)
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

subtracted = cv2.subtract(img, dilated)
print("Fini !")
while True:
    cv2.imshow('fenetreImage', subtracted)
    if cv2.waitKey(1) == ord('q'):
        break

# Libération des ressources
cv2.destroyAllWindows()
