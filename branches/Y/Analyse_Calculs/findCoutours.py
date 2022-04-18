import cv2

cam = cv2.imread("ressources/vue_cam_1.jpg", cv2.IMREAD_GRAYSCALE)
a, cam = cv2.threshold(cam, 127, 255, cv2.THRESH_BINARY)  # a == ? / Tous les bits sont 0 ou 255

cntr,hrcy = cv2.findContours(cam,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

print (cntr)

cv2.namedWindow("namedWindow", cv2.WINDOW_NORMAL)
cv2.imshow("namedWindow", cam)
cv2.waitKey(0)