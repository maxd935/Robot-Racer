from math import sqrt, atan, pi as PI

def rect_to_points(X, Y, box2):
    """
    Trouve les 2 points se tranvant au milleu des cotés les plus petits.
    """
    (h1, h2), (b1, b2) = colsort(box2[0:2]), colsort(box2[2:4])
    if norme(h1, h2) > norme(h2, b2):
         if h2[1] > h1[1]:
             h1, b2 = b2, h1
         elif h1[1] > h2[1]:
             b1, h2 = h2, b1
    mhx, mhy = (h1[0] + (h2[0] - h1[0]) / 2, h1[1] + (h2[1] - h1[1]) / 2)
    mbx, mby = (b1[0] + (b2[0] - b1[0]) / 2, b1[1] + (b2[1] - b1[1]) / 2)
     
    mbx -= X/2
    mhx -= X/2
    mby = Y-mby
    mhy = Y-mhy
    
    A = (mhx, mhy)
    B = (mbx, mby)
    return (A, B)

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
    if Bx > Ax:
        return points_to_droite(B, A)
    if Bx - Ax == 0:
        coef = Ax
    elif By - Ay == 0:
        coef = 0
        ordonnee_origine = Ay
    else:
        coef = (By - Ay) / (Bx - Ax)
        ordonnee_origine = Ay - coef * Ax
    return coef, ordonnee_origine

def droite_to_angle(m, p):
    """ Calcul de l'angle de la droite par rapport à l'axe des abcisses """
    if m != 0 and p is not None:
        return atan(1/m)*180/PI     
    else: return 0

# Trier un tableau a selon une colonne d'indice b, par défaut égal à 0
colsort = lambda a, b=0: a[a[:, b].argsort()]

# Calcul la norme entre deux points (x, y)
norme = lambda a, b: sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)