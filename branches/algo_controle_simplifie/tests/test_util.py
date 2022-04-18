import pytest
from numpy import array
from util import (
    colsort,
    norme,
    points_to_droite,
    droite_to_angle
)


@pytest.mark.parametrize("A,B,res", [
        # A(x,y)  B(x,y)  (m, p) pour y = m*x + p
        ((0, 0), (2, 2), (1., 0.)),
        ((2, 2), (0, 0), (1., 0.)),
        ((0, 3), (3, 0), (-1., 3.)),
        ((1, 0), (2, 2), (2., -2.)),
        ((2, 0), (2, 6), (2., None)),
        ((0, 0), (0, 10), (0., None)),
        ((0, 4), (1, 4), (0., 4.)),
        ((0, -5), (10, -5), (0., -5)),
])
def test_points_to_droite(A, B, res):
    """ Test de la création de droite (ax+b) à partir de points (x,y) """
    assert points_to_droite(A, B) == res


@pytest.mark.parametrize("tableau,axe,res", [
        (array([[1, 2], [3, -1], [0, 1]]), 0, array([[0, 1], [1, 2], [3, -1]])),
        (array([[1, 2], [3, -1], [0, 1]]), 1, array([[3, -1], [0, 1], [1, 2]]))
])
def test_colsort(tableau, axe, res):
    """ Test du tri croissant sur une colonne """
    assert (colsort(tableau, axe) == res).all()


@pytest.mark.parametrize("A,B,res", [
    ((10, 10), (11, 10), 1.),
    ((10, 10), (9, 10), 1.),
    ((10, 10), (10, 11), 1.),
    ((10, 10), (10, 9), 1.),
    ((1, 1), (0, 0), 2 ** 0.5),
])
def test_norme(A, B, res):
    """ Test du tri croissant sur une colonne """
    assert norme(A, B) == res


@pytest.mark.parametrize("A,B,res", [
    (0, 0, 0),
    (1, 0, 45),
    (0.5, 0, 63),
    (0, None, 90),
    (-1, 0, -45),
    (-0.5, 0, -63)
])
def test_droite_to_angle(A, B, res):
    """ Test du tri croissant sur une colonne """
    assert int(droite_to_angle(A, B)) == res
