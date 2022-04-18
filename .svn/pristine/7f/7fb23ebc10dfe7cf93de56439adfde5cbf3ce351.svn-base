from ImageClass import Image
import cv2


def calculer_seuil_test(file_name):
    img = Image(file_name)
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', (640, 480))
    cv2.moveWindow('img', 480, 0)
    cv2.imshow("img", img.getImage())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return "Fini \n"


print(calculer_seuil_test("surex2modif.jpg"))       # 85

#print(calculer_seuil_test("vue_cam_1.jpg"))      # 85

print(calculer_seuil_test("surex2modif2.jpg"))      # 85

#print(calculer_seuil_test("surex.jpg"))      # -1
