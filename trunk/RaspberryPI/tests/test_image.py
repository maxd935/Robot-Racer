import pytest
from os import listdir
from os.path import exists, abspath, dirname, basename
from image import Image
from simple_image import SimpleImage
import cv2
from numpy import array

ASSETS_DIR = dirname(abspath(__file__)) + "/assets/"


def getFilesInDir(dir, filtre="", split=False):
    """
    Renvoie une liste de tous les fichiers dans un dossier de assets
    et comportant filtre dans leur nom de fichier.

    Par exemple, on a le repertoire
    |+ ./tests/assets/surex/
    |    | test1.jpg
    |    | test2.png
    |    | test3.jpg
    |    | sous_dir/

    getFilesInDir("surex", "jpg")
    renvoie ["./tests/assets/surex/test1.jpg", "./tests/assets/surex/test3.jpg"]
    """
    if not exists(ASSETS_DIR + dir):
        return list()
    res = list(map(lambda f: ASSETS_DIR + dir + "/" + f,
               filter(lambda x: filtre in x, listdir(ASSETS_DIR + dir))))
    res.sort()
    if not split:
        return res
    else:
        return [(filename, basename(filename).split(",")[0:split])
                for filename in res]


@pytest.fixture
def file(filename):
    """ Cette fixture convertit le nom de fichier en classe Image """
    return Image(cv2.imread(filename))


@pytest.fixture
def image(file):
    """ Cette fixture convertit le filename en classe Image prétraitée """
    file.preTraitement()
    return file


@pytest.fixture
def contour(image):
    """
    Cette fixture convertit le filename en classe Image prétraitée et
    retourne l'image et le meilleur contour trouvé.
    """
    _, contours, _ = cv2.findContours(image._image_thresh, cv2.RETR_CCOMP,
                                      cv2.CHAIN_APPROX_SIMPLE)
    return image, max(contours, key=cv2.contourArea)


@pytest.mark.parametrize("filename", getFilesInDir("isSurex"))
def test_surex(file):   # OK
    """ Test le jeu d'image surexposées """
    assert file.isSurex()


@pytest.mark.parametrize("filename", getFilesInDir("isNotSurex"))
def test_not_surex(file):   # OK
    """ Test le jeu d'image non surexposées """
    assert not file.isSurex()


@pytest.mark.parametrize("filename", getFilesInDir("isFin"))
def test_fin(file):   # OK
    """ Test le jeu d'image décrivant un scénario de fin """
    assert file.isFin()


@pytest.mark.parametrize("filename", getFilesInDir("isNotFin"))
def test_not_fin(file):   # OK
    """ Test le jeu d'image ne décrivant pas un scénario de fin """
    assert not file.isFin()


@pytest.mark.parametrize("filename", getFilesInDir("surex"))
def test_preTraitementSurex(file):   # OK
    file.preTraitementSurex()
    assert file._image_thresh is not None


@pytest.mark.parametrize("filename", getFilesInDir("nonsurex"))
def test_preTraitementPasSurex(file):   # Fail : pixellisation.png
    file.preTraitementPasSurex()
    assert file._image_thresh is not None


@pytest.mark.parametrize("filename,res", getFilesInDir("get3x3", split=3))
def test_get3x3(image, res):
    res = [[int(i)] if i != '' else [] for i in res]
    assert (array(SimpleImage(image.get3x3()).max_lines())
            == array(res)).all()


@pytest.mark.parametrize("filename,res", getFilesInDir("shift_angle", split=2))
def test_shift_angle(image, res):
    """ Vérifie le shift et l'angle des images """
    res = [int(i) if i != '' else [] for i in res]
    shift, angle = image.shift_angle()
    assert [int(shift), int(angle)] == res


@pytest.mark.parametrize("filename,res", getFilesInDir("hough", split=2))
def test_approx_droite_hough(contour, res):
    im, cont = contour
    res = [int(i) if i != 'None' else None for i in res]
    assert (array(im.approx_droite_hough(cont)).astype(int) == array(res)).all()


@pytest.mark.parametrize("filename,res", getFilesInDir("rect", split=3))
def test_approx_droite_rect(contour, res):
    im, cont = contour
    res_m, res_p, res_centered = [int(i) if i != 'None' else None for i in res]
    (m, p), centered = im.approx_droite_rect(cont)
    assert ((m == res_m if m is None else int(m) == res_m)
            and (p == res_p if p is None else int(p) == res_p)
            and (centered == res_centered if m is None else int(centered) == res_centered))
