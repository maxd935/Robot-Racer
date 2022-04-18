"""
Le module util comprend toutes les fonctions
n'ayant pas de dépendance au reste du code et assez
abstraite
"""
from math import sqrt, atan, pi as PI
from numpy import polyfit, concatenate, sum


def points_to_droite(A, B):
    """
    Convertir deux points en équation de droite

    Parameters
    ----------
    A : tuple of ints
        Point A
    B : tuple of ints
        Point B

    Returns
    -------
    m : float
        Pente de la droite
    p : float
        Ordonnée à l'origine

    Notes
    -----
    retourne le tuple (m, p) décrivant la droite y = m*x + p
    * Si la droite est horizontale (y = cte), m = 0 et p = cte
    * Si la droite est verticale (x = cte), m = cte et p = None
    """
    (Ax, Ay), (Bx, By) = A, B
    ordonnee_origine = None
    if By > Ay:
        return points_to_droite(B, A)
    if Bx - Ax == 0:
        coef = Ax
    else:
        coef = (By - Ay) / (Bx - Ax)
        if coef > 50:
            coef = Ax
        elif abs(coef) < 0.02:
            coef = 0
            ordonnee_origine = Ay
        else:
            ordonnee_origine = Ay - coef * Ax
    return coef, ordonnee_origine


def droite_to_angle(m, p):
    """
    Calcul de l'angle de la droite par rapport à l'axe des abcisses

    Parameters
    ----------
    m : float
        Pente de la droite
    p : float
        Ordonnée à l'origine

    Returns
    -------
    float
        Angle compris entre -90 et 90 degrés
    """
    if p is None or m > 20:
        return 90
    elif m == 0:
        return 0
    else:
        angle = atan(m) * 180 / PI
        return (-90 if m < 0 else 90) - angle
        if m < 0:
            return - 90 - angle
        else:
            return 90 - angle


def affine(A, B):
    """
    Créé une fonction affine à partir de deux points donnés.

    Parameters
    ----------
    A : tuple of float
        Point A
    B : tuple of float
        Point B

    Returns
    -------
    lambda x
        Une fonction lambda qui prend `x` en paramètre et renvoie f(x)
    """
    (ax, ay), (bx, by) = A, B
    coef = (by - ay) / (bx - ax)
    ori = ay - coef * ax
    return lambda x: coef * x + ori


def parabole(A, B, C):
    """
    Créé une fonction polynome de degré 2 passant par les points A, B et C

    Parameters
    ----------
    A : tuple of float
        Point A
    B : tuple of float
        Point B
    B : tuple of float
        Point C

    Returns
    -------
    lambda x
        Une fonction lambda qui prend `x` en paramètre et renvoie f(x)
    """
    (ax, ay), (bx, by), (cx, cy) = A, B, C
    a = (cy - ay)/((cx - ax)*(cx - bx)) - (by - ay)/((bx - ax)*(cx - bx))
    b = (by - ay) / (bx - ax) - a * (bx + ax)
    c = ay - a * (ax**2) - b * ax
    return lambda x: a*(x**2) + b*x + c


def parabole_symetrique(A, B, C):
    """
    Créé une fonction polynome de degré 2 passant par les points A, B et C
    sur le domaine des réels positifs.
    On a la relation suivante pour les négatifs : f(-x) = -f(x)


    Parameters
    ----------
    A : tuple of float
        Point A
    B : tuple of float
        Point B
    B : tuple of float
        Point C

    Returns
    -------
    lambda x
        Une fonction lambda qui prend `x` en paramètre et renvoie f(x)
    """
    func = parabole(A, B, C)
    return lambda a: -func(-a) if a < 0 else func(a)


def predict(hist, deg=2, length=3):
    """
    Créé une fonction polynome de degré 2 passant par les points A, B et C
    sur le domaine des réels positifs.
    On a la relation suivante pour les négatifs : f(-x) = -f(x)


    Parameters
    ----------
    hist : ndarray
        Données
    deg : int
        Degré du polynome
    length : int
        Nombre de points pris dans `hist` à partir de la fin

    Returns
    -------
    int
        L'estimation du prochain point

    Notes
    -----
    Le paramètre hist doit avoir au moins 2 colonnes, une pour les
    x et l'autre pour les y. Il doit comporter au moins deg + 1 lignes.
    """
    hist = hist[-length:, ]
    res = polyfit(hist[:, 0], hist[:, 1], deg)
    res = concatenate((res, range(deg, -1, -1))).reshape((deg + 1, 2), order="F")
    return int(sum([a * ((hist[-1][0] + 1) ** n) for a, n in res]))


# Trier un tableau a selon une colonne d'indice b, par défaut égal à 0
colsort = lambda a, b=0: a[a[:, b].argsort()]

# Calcul la norme entre deux points (x, y)
norme = lambda a, b: sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
shift_corner = parabole_symetrique((90, 160), (0, 125), (80, 145))
