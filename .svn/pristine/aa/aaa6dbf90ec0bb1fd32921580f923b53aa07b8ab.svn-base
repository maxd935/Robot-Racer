"""
Le module table table_decision comporte la fonction prendre_decision
qui donne en fonction de la perception de l'environnement la direction
que doit prendre le robot.

Attributes
----------
SEUIL : int
    Cet attribut correspond au seuil qui définit la limite  pour laquelle
    une valeur est considérée comme nulle si inférieure, ou inchangée sinon.

"""


def prendre_decision(top, mid, bottom, mat):
    """ Prise de décision du robot selon sa perception.

    table_decision correspond à un ensemble de condition-action bien définies
    et qui définissent le comportement du robot selon sa perception de l'
    environnement.

    Parameters
    ----------
    top : array
        Tableau des positions des / de la valeur(s) maximale(s)
        de la ligne du haut
    mid : array
        Tableau des positions des / de la valeur(s) maximale(s)
        de la ligne du haut
    bottom : array
        Tableau des positions des / de la valeur(s) maximale(s)
        de la ligne du haut
    mat : ndarray
        Matrice de taille 3x3 originale

    Returns
    -------
    angle : int
        L'angle des roues que devra prendre le robot.
    message : str
        Le message correspondant à l'angle choisi
    """
    if 0 in bottom:
        if 0 in mid:
            if 0 in top:
                return (-33, "GGG")
            elif 1 in top:
                return (5, "GGM")
            elif 2 in top:
                return (15, "GGD")
            elif len(top) == 0:
                return (-42, "GG")
        elif 1 in mid:
            if 0 in top:
                return (-15, "GMG")
            elif 1 in top:
                return (0, "GMM")
            elif 2 in top:
                return (5, "GMD")
            elif len(top) == 0:
                return (15, "GM")
        elif 2 in mid:
            if 0 in top:
                return (-10, "GDG")
            elif 1 in top:
                return (5, "GDM")
            elif 2 in top:
                return (36, "GDD")
            elif len(top) == 0:
                return (43, "GD")
        elif len(mid) == 0:
            if 0 in top:
                return (-10, "!GxG")
            elif 1 in top:
                return (0, "!GxM")
            elif 2 in top:
                return (15, "!GxD")
            elif len(top) == 0:
                return (-46, "Gxx")
    if 1 in bottom:
        if 0 in mid:
            if 0 in top:
                return (-22, "MGG")
            elif 1 in top:
                return (0, "MGM")
            elif 2 in top:
                return (0, "MMD")
            elif len(top) == 0:
                return (-40, "MG")
        elif 1 in mid:
            if 0 in top:
                return (-10, "MMG")
            elif 1 in top:
                return (0, "MMM")
            elif 2 in top:
                return (10, "MMD")
            elif len(top) == 0:
                return (0, "MM")
        elif 2 in mid:
            if 0 in top:
                return (0, "!MDG")
            elif 1 in top:
                return (0, "MDM")
            elif 2 in top:
                return (22, "MDD")
            elif len(top) == 0:
                return (40, "MD")
        elif len(mid) == 0:
            if 0 in top:
                return (-10, "!MxG")
            elif 1 in top:
                return (0, "!MxM")
            elif 2 in top:
                return (10, "!GxD")
            elif len(top) == 0:
                return (0, "!Mxx")
    if 2 in bottom:
        if 0 in mid:
            if 0 in top:
                return (-36, "DGG")
            elif 1 in top:
                return (-10, "!DGM")
            elif 2 in top:
                return (15, "!DGD")
            elif len(top) == 0:
                return (-43, "DG")
        elif 1 in mid:
            if 0 in top:
                return (-15, "DMD")
            elif 1 in top:
                return (0, "DMM")
            elif 2 in top:
                return (10, "DMD")
            elif len(top) == 0:
                return (-15, "DM")
        elif 2 in mid:
            if 0 in top:
                return (-10, "DDG")
            elif 1 in top:
                return (-4, "DDM")
            elif 2 in top:
                return (33, "DDD")
            elif len(top) == 0:
                return (42, "DD")
        elif len(mid) == 0:
            if 0 in top:
                return (-15, "!DxG")
            elif 1 in top:
                return (-5, "!DxM")
            elif 2 in top:
                return (15, "!DxD")
            elif len(top) == 0:
                return (46, "Dxx")
    elif len(bottom) == 0:
        if 0 in mid:
            if 0 in top:
                return (-36, "xGG")
            elif 1 in top:
                return (0, "xGM")
            elif 2 in top:
                return (30, "xGD")
            elif len(top) == 0:
                return (-45, "xGx")
        elif 1 in mid:
            if 0 in top:
                return (-15, "xMD")
            elif 1 in top:
                return (0, "xMM")
            elif 2 in top:
                return (15, "xMD")
            elif len(top) == 0:
                return (0, "!xMx")
        elif 2 in mid:
            if 0 in top:
                return (-30, "xDG")
            elif 1 in top:
                return (0, "xDM")
            elif 2 in top:
                return (15, "xDD")
            elif len(top) == 0:
                return (45, "xDx")
        elif len(mid) == 0:
            if 0 in top:
                return (-15, "xxG")
            elif 1 in top:
                return (0, "!xxM")
            elif 2 in top:
                return (15, "!xxD")
            elif len(top) == 0:
                return (0, "Vide")

    return (0, "Fail")
