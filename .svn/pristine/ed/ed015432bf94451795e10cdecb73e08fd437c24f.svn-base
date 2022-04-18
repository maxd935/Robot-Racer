import pytest
from os import listdir
from os.path import exists
from image import Image
import cv2

ASSETS_DIR = "./tests/assets/"


def getFilesInDir(dir, filtre=""):
    """
    Renvoie une liste de tous les fichiers dans un dossier de assets
    et comportant filtre dans leur nom de fichier.

    Par exemple, on a le repertoire
    + ./tests/assets/surex/
        | test1.jpg
        | test2.png
        | test3.jpg
        | sous_dir/

    getFilesInDir("surex", "jpg")
    renvoie ["./tests/assets/surex/test1.jpg",
             "./tests/assets/surex/test3.jpg"]
    """
    if not exists(ASSETS_DIR + dir):
        return list()
    return list(map(lambda f: ASSETS_DIR + dir + "/" + f,
                    filter(lambda x: filtre in x, listdir(ASSETS_DIR + dir))))


@pytest.mark.parametrize("filename", getFilesInDir("surex"))
def test_surex(filename):   # OK
    """ Test le jeu d'image surexposées """
    assert Image(cv2.imread(filename)).isSurex() is True


@pytest.mark.parametrize("filename", getFilesInDir("nonsurex"))
def test_not_surex(filename):   # OK
    """ Test le jeu d'image non surexposées """
    assert Image(cv2.imread(filename)).isSurex() is False


@pytest.mark.parametrize("filename", getFilesInDir("isfin"))
def test_fin(filename):   # OK
    """ Test le jeu d'image ne décrivant pas un scénario de fin """
    assert Image(cv2.imread(filename)).isFin() is True


@pytest.mark.parametrize("filename", getFilesInDir("isnotfin"))
def test_not_fin(filename):   # OK
    """ Test le jeu d'image décrivant un scénario de fin """
    assert Image(cv2.imread(filename)).isFin() is False


@pytest.mark.parametrize("filename", getFilesInDir("surex"))
def test_preTraitementSurex(filename):   # OK
    f = Image(cv2.imread(filename))
    f.preTraitementSurex()
    assert f._image_thresh is not None


@pytest.mark.parametrize("filename", getFilesInDir("nonsurex"))
def test_preTraitementPasSurex(filename):   # Fail : pixellisation.png
    f = Image(cv2.imread(filename))
    f.preTraitementPasSurex()
    assert f._image_thresh is not None


@pytest.mark.parametrize("filename,res", [
    ("1.png", (37, 0)),
    ("2.png", (0, 0)),
    ("3.png", (62, 0)),
    ("4.png", (-62, 0)),
    ("5.jpg", (22, 0)),
    ("6.jpg", (0, 0)),
    ("7.jpg", (-13, 0)),
    ("8.jpg", (23, 0)),
    ("9.png", (23, 0)),
    ("10.jpg", (40, 0)),
    ("11.jpg", (40, 142.0443181212587))
    ])
def test_shift_angle(filename, res):   # OK
    f = Image(cv2.imread("./tests/assets/shift_angle/"+filename))
    if(f.isSurex()):
        f.preTraitementSurex()
    else:
        f.preTraitementPasSurex()
    assert f.shift_angle() == res


@pytest.mark.parametrize("filename,res", [
    ("1.png", (None, None)),
    ("2.png", (None, None)),
    ("3.png", (None, None)),
    ("4.png", (None, None)),
    ("5.jpg", [208, None]),
    ("6.jpg", [-2.75, 692.25]),
    ("7.jpg", [401, None]),
    ("8.jpg", [31.6, -6496.6]),
    ("9.png", [33., -6794.]),
    ("10.jpg", [1.60674157, -738.29213483]),
    ("11.jpg", [1.28571429, -521.28571429])
    ])
def test_approx_droite_hough(filename, res):   # ???
    f = Image(cv2.imread("./tests/assets/hough/"+filename))
    if(f.isSurex()):
        f.preTraitementSurex()
    else:
        f.preTraitementPasSurex()
    # Contours
    img = f._image_thresh
    _, contours, _ = cv2.findContours(img, cv2.RETR_CCOMP,
                                      cv2.CHAIN_APPROX_SIMPLE)
    best_contours = max(contours, key=cv2.contourArea)
    assert f.approx_droite_hough(best_contours) == res


@pytest.mark.parametrize("filename,res", [
    ("1.png", ((219.5, None), True)),
    ("2.png", ((158.5, None), True)),
    ("3.png", ((260.5, None), False)),
    ("4.png", ((60.49999237060547, None), False)),
    ("5.jpg", ((285.0, None), True)),
    ("6.jpg", ((320.0, None), True)),
    ("7.jpg", ((277.5, None), True)),
    ("8.jpg", ((285.5, None), True)),
    ("9.png", ((286.0, None), True)),
    ("10.jpg", ((449.0, None), True)),
    ("11.jpg", ((1.2819843342036554, -335.0561357702351), False))
    ])
def test_approx_droite_rect(filename, res):   # OK
    f = Image(cv2.imread("./tests/assets/rect/"+filename))
    if(f.isSurex()):
        f.preTraitementSurex()
    else:
        f.preTraitementPasSurex()
    # Contours
    img = f._image_thresh
    _, contours, _ = cv2.findContours(img, cv2.RETR_CCOMP,
                                      cv2.CHAIN_APPROX_SIMPLE)
    best_contours = max(contours, key=cv2.contourArea)
    assert f.approx_droite_rect(best_contours) == res
