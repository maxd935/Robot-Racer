import cv2

cap = cv2.VideoCapture("/dev/video2")
if not cap.isOpened():
    print("Erreur bus")

out = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc(*'MJPG'), 20, (640, 480), 1)

while(True):
     # Capture each frame of webcam video
     ret, frame = cap.read()
     cv2.imshow("Video", frame)
     out.write(cv2.resize(frame, (640, 480)))
     if cv2.waitKey(1) &0XFF == ord('q'):
         break
         
cap.release()
out.release()
cv2.destroyAllWindows()
