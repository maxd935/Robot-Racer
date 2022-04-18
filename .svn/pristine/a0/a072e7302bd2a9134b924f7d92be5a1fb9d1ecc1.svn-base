from config import get as conf
from math import sqrt, atan, pi as PI, inf

def points_to_droite(A, B):
    """
    Convertir deux points en équation de droite
    - A, B : deux tupes (x, y)

    retourne le tuple (m, p) décrivant la droite y = m*x + p
    - Si la droite est horizontale (y = cte), m = 0 et p = cte
    - Si la droite est verticale (x = cte), m = cte et p = None
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


def seuiller_shift_angle(shift, angle):
    """ Si le shift ou l'angle est insignifiant, on ne fait rien. """
    if abs(shift) < conf("image.min_shift"):
        shift = 0
    if abs(angle) < conf("image.min_angle"):
        angle = 0
    return (shift, angle)


def droite_to_angle(m, p):
    """ Calcul de l'angle de la droite par rapport à l'axe des abcisses """
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
    """ Retourne la fonction affine que représente la droite AB """
    (ax, ay), (bx, by) = A, B
    coef = (by - ay) / (bx - ax)
    ori = ay - coef * ax
    return lambda x: coef * x + ori


def parabole(A, B, C):
    """ Retourne le polynome de degré 2 passant par les points A, B et C """
    (ax, ay), (bx, by), (cx, cy) = A, B, C
    a = (cy - ay)/((cx - ax)*(cx - bx)) - (by - ay)/((bx - ax)*(cx - bx))
    b = (by - ay) / (bx - ax) - a * (bx + ax)
    c = ay - a * (ax**2) - b * ax
    return lambda x: a*(x**2) + b*x + c

def parabole_symetrique(A, B, C):
    """ Parabole sur [0, +inf] symétrique : f(x) == -f(-x) """
    func = parabole(A, B, C)
    return lambda a: -func(-a) if a < 0 else func(a)

# Trier un tableau a selon une colonne d'indice b, par défaut égal à 0
colsort = lambda a, b=0: a[a[:, b].argsort()]

# Calcul la norme entre deux points (x, y)
norme = lambda a, b: sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

# Calcul de la parabole transformant un angle calculé en "réel"
angle_transf = parabole_symetrique((10, 0), (70, 25), (90, 40))
shift_transf = parabole_symetrique((100, 10), (300, 15), (1000, 25))
simple_shift_transf = parabole_symetrique((0, 10), (20, 20), (100, 45))
shift_corner = parabole_symetrique((90, 160), (0, 125), (80, 145))
