import cv2
import numpy as np
import time

NB_ITERATIONS = [10, 100, 300, 1000]
IMG_SIZES = [
    (640, 480),
    (320, 240),
    (160, 120),
    (80, 60),
    (40, 30),
    (20, 15)
]

tailleImage = (64, 48)


def skeletize(img):
    skeleton = np.zeros(img.shape, np.uint8)
    eroded = np.zeros(img.shape, np.uint8)
    temp = np.zeros(img.shape, np.uint8)

    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    while(True):
        cv2.erode(img, element, eroded)
        cv2.dilate(eroded, element, temp)
        cv2.subtract(img, temp, temp)
        cv2.bitwise_or(skeleton, temp, skeleton)
        img, eroded = eroded, img  # Swap instead of copy

        if cv2.countNonZero(img) == 0:
            return skeleton


def dowith_iteration(iteration, img, size):
    start_time = time.time_ns()
    for i in range(0, iteration):
        skeletize(img.copy())
    elapsed_time = time.time_ns() - start_time
    print(size, "\t", iteration, "\t",
          "{}".format(elapsed_time * 1e-6).replace(".", ","))


def dowith_imgsize(img_size):
    img = cv2.imread("plan.jpg", cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, img_size)
    ret, img = cv2.threshold(img, 0, 255,
                             cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    for i in NB_ITERATIONS:
        dowith_iteration(i, img, img_size)
        dowith_iteration(i, img, img_size)
        dowith_iteration(i, img, img_size)


for size in IMG_SIZES:
    dowith_imgsize(size)
