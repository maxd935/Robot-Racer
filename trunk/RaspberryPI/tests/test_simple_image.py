import pytest
from simple_image import SimpleImage
from numpy import array

data_1 = SimpleImage(array([
    [0.5, 80, 10],
    [1, 9, 60],
    [12, 6, 5]
]))

data_2 = SimpleImage(array([
    [0, 0, 0],
    [1, 9, 9],
    [5, 4, 3]
]))

data_3 = SimpleImage(array([
    [0, 0, 0],
    [1, 9, 9],
    [0, 0, 0]
]))

data_4 = SimpleImage(array([
    [0, 0, 100],
    [1, 9, 9],
    [0, 0, 0]
]))

data_5 = SimpleImage(array([
    [0, 0, 0],
    [1, 9, 9],
    [20, 0, 0]
]))


def test_not__():
    assert data_1.LeftNotBiggerThanLeft
    assert not data_1.CenterNotBiggerThanLeft

    assert not data_1.maxTopIsNotCenter
    assert data_1.maxTopIsNotLeft

    assert not data_1.bigBottomIsNotLeft
    assert data_1.bigBottomIsNotRight

def test_only__():
    assert data_5.onlyBottomLeft
    assert not data_5.onlyTopLeft
    assert not data_5.onlyBottomRight
    assert not data_5.onlyMidCenter

    assert data_4.onlyTopRight
    assert not data_4.onlyTopLeft
    assert not data_4.onlyBottomRight
    assert not data_4.onlyMidCenter


def test_vertical__bigger_than__():
    assert not data_1.LeftBiggerThanLeft
    assert not data_1.LeftBiggerThanCenter
    assert not data_1.LeftBiggerThanRight

    assert data_1.CenterBiggerThanLeft
    assert not data_1.CenterBiggerThanCenter
    assert data_1.CenterBiggerThanRight

    assert data_1.RightBiggerThanLeft
    assert not data_1.RightBiggerThanCenter
    assert not data_1.RightBiggerThanRight

    assert data_3.RightBiggerThanLeft
    assert not data_3.RightBiggerThanCenter
    assert not data_3.RightBiggerThanRight


def test_horizontal__bigger_than__():
    assert not data_1.TopBiggerThanTop
    assert data_1.TopBiggerThanMid
    assert data_1.TopBiggerThanBottom

    assert not data_1.MidBiggerThanTop
    assert not data_1.MidBiggerThanMid
    assert data_1.MidBiggerThanBottom

    assert not data_1.BottomBiggerThanTop
    assert not data_1.BottomBiggerThanMid
    assert not data_1.BottomBiggerThanBottom


def test_values_position():
    assert data_1.topLeft == 0.5
    assert data_1.topCenter == 80
    assert data_1.topRight == 10
    assert data_1.midLeft == 1
    assert data_1.midCenter == 9
    assert data_1.midRight == 60
    assert data_1.bottomLeft == 12
    assert data_1.bottomCenter == 6
    assert data_1.bottomRight == 5
    assert data_1.TopLeft == 0.5
    assert data_1.TopCenter == 80
    assert data_1.TopRight == 10
    assert data_1.MidLeft == 1
    assert data_1.MidCenter == 9
    assert data_1.MidRight == 60
    assert data_1.BottomLeft == 12
    assert data_1.BottomCenter == 6
    assert data_1.BottomRight == 5


def test_horizontal_max__is__():
    assert data_1.maxTopIsCenter
    assert not data_1.maxTopIsLeft
    assert not data_1.maxTopIsRight

    assert data_1.maxMidIsRight
    assert not data_1.maxMidIsLeft
    assert not data_1.maxMidIsCenter

    assert data_1.maxBottomIsLeft
    assert not data_1.maxBottomIsRight
    assert not data_1.maxBottomIsCenter

    assert not data_2.maxTopIsCenter
    assert not data_2.maxTopIsLeft
    assert not data_2.maxTopIsRight

    assert data_2.maxMidIsRight
    assert not data_2.maxMidIsLeft
    assert data_2.maxMidIsCenter


def test_vertical_max__is__():
    assert data_1.maxRightIsMid
    assert not data_1.maxRightIsTop
    assert not data_1.maxRightIsBottom

    assert data_1.maxCenterIsTop
    assert not data_1.maxCenterIsBottom
    assert not data_1.maxCenterIsMid

    assert data_1.maxLeftIsBottom
    assert not data_1.maxLeftIsTop
    assert not data_1.maxLeftIsMid


def test_big__is__():
    assert not data_1.bigTopIsLeft
    assert not data_1.bigTopIsRight
    assert data_1.bigTopIsCenter

    assert not data_1.bigMidIsLeft
    assert data_1.bigMidIsRight
    assert not data_1.bigMidIsCenter

    assert data_1.bigBottomIsLeft
    assert not data_1.bigBottomIsRight
    assert not data_1.bigBottomIsCenter

    assert not data_2.bigBottomIsLeft
    assert not data_2.bigBottomIsRight
    assert not data_2.bigBottomIsCenter

    assert not data_2.bigTopIsLeft
    assert not data_2.bigTopIsRight
    assert not data_2.bigTopIsCenter
