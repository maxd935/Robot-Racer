"""
Visionnage du temps d'execution d'une fonction pour un grand nombre
d'itérations et de taille d'image pour une image fournie.

Exemple d'utilisation :

    Signature de la fonction :
        @benchmark("PI ou PC", "image_filename.jpg")
        fonction_a_verifier(image (dnarray), autres arguments)

    Execution :
        fonction_a_verifier(autres arguments)
"""

import cv2
import time


# Nombre d'executions identiques avec meme taille et meme nombre d'iterations
NB_SAME_PI = 3
# Tailles de l'image à essayer
IMG_SIZES_PI = [(320, 240), (160, 120), (80, 60), (40, 30), (20, 15)]
# Nombre d'itérations à esayer
NB_ITERATIONS_PI = [10, 50, 100, 200]

NB_SAME_PC = 3
IMG_SIZES_PC = [(640, 480), (320, 240), (160, 120), (80, 60), (40, 30), (20, 15)]
NB_ITERATIONS_PC = [10, 100, 300, 1000]


def benchmark(type, img):
    def with_type(func):

        def with_timer(*args, **kargs):
            if type == "PI":
                sizes = IMG_SIZES_PI
                iters = NB_ITERATIONS_PI
                same = NB_SAME_PI
            else:
                sizes = IMG_SIZES_PC
                iters = NB_ITERATIONS_PC
                same = NB_SAME_PC

            img_read = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

            for size in sizes:
                img_test = cv2.resize(img_read, size)
                size_x, size_y = size
                for j in iters:
                    for i in range(0, same):
                        start_time = time.time_ns()
                        func(img_test, *args, **kargs)
                        elapsed_time = time.time_ns() - start_time
                        print(size_x, "\t", size_y, "\t",
                              j, "\t", "{}"
                              .format(elapsed_time * 1e-6)
                              .replace(".", ","))
            return 0
        return with_timer
    return with_type
