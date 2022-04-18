from ImageClass import Image
import cv2


def traitement_test(file_name):
    img = Image(file_name)
    img.resizeImage()
    if not img.isFin() and not img.isSurex():
        img.traitement()
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', (640, 480))
    cv2.moveWindow('img', 480, 0)
    cv2.imshow("img", img.getImage())
    print(file_name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return "Fini \n"


traitement_test("img.jpg")

traitement_test("noLigne.jpg")

traitement_test("vue_cam_1.jpg")

traitement_test("surex.jpg")

traitement_test("newLigne/cam_haute_17.jpg")
traitement_test("newLigne/cam_haute_16.jpg") # Surex
traitement_test("newLigne/cam_haute_15.jpg") # Surex
traitement_test("newLigne/cam_haute_14.jpg") # Surex
traitement_test("newLigne/cam_haute_13.jpg")
traitement_test("newLigne/cam_haute_12.jpg")
traitement_test("newLigne/cam_haute_11.jpg")
traitement_test("newLigne/cam_haute_10.jpg")
traitement_test("newLigne/cam_haute_9.jpg")
traitement_test("newLigne/cam_haute_8.jpg") # Fin
traitement_test("newLigne/cam_haute_7.jpg")
traitement_test("newLigne/cam_haute_6.jpg")
traitement_test("newLigne/cam_haute_5.jpg") # ??
traitement_test("newLigne/cam_haute_4.jpg") # Surex
traitement_test("newLigne/cam_haute_3.jpg") # Surex
traitement_test("newLigne/cam_haute_2.jpg")
traitement_test("newLigne/cam_haute_1.jpg") # Surex
