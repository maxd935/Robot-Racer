from numpy import sum, array, max, delete
from re import search, IGNORECASE


cols = "Left|Center|Right"
rows = "Top|Mid|Bottom"

ar_cols = cols.split("|")
ar_rows = rows.split("|")
cr = cols + "|" + rows


class SimpleImage:
    """
    Examples
    --------

    maxTopIsLeft : retourne vrai si la valeur max de la ligne
                   du haut est à droite
    maxRightIsBottom : retourne vrai si la valeur max de la
                       colonne de droite est en bas

    bigBottomIsRight : retourne vrai si la valeur en bas à
                       droite est supérieure a la somme de en bas à
                       gauche et en bas au centre

    leftBiggerThanRight : retour vrai si la somme de la colonne de droite est
                          supérieure à la somme de la colonne de gauche.
    topBiggerThanBottom : retour vrai si la somme de la colonne du haut est
                          supérieure à la somme de la colonne du bas.

    topRight : retourne la valeur en haut à droite
    midRight : retourne la valeur au milieu à droite
    bottomCenter : retourne la valeur en bas au centre
    """

    def __init__(self, mat):
        self.mat = mat

    def __getattr__(self, name):
        """
        Lorsque qu'on appelle *SimpleImage.attribut*, cette méthode est
        appellée avec attribut comme name.
        Cette fonction génère "dynamiquement" les attributs demandés.
        """
        x = search("^max(" + cr + ")Is(" + cr + ")$", name)
        if x and len(x.groups()) == 2:
            return self.max_is_(*x.groups())

        x = search("^max(" + cr + ")IsNot(" + cr + ")$", name)
        if x and len(x.groups()) == 2:
            return not self.max_is_(*x.groups())

        x = search("^big(" + rows + ")Is(" + cols + ")$", name)
        if x and len(x.groups()) == 2:
            return self.big_is_(*x.groups())

        x = search("^big(" + rows + ")IsNot(" + cols + ")$", name)
        if x and len(x.groups()) == 2:
            return not self.big_is_(*x.groups())

        x = search("^(" + cr + ")BiggerThan(" + cr + ")$", name, IGNORECASE)
        if x and len(x.groups()) == 2:
            return self._BiggerThan_(*x.groups())

        x = search("^(" + cr + ")NotBiggerThan(" + cr + ")$", name, IGNORECASE)
        if x and len(x.groups()) == 2:
            return not self._BiggerThan_(*x.groups())

        x = search("^only(" + cr + ")(" + cr + ")$", name)
        if x and len(x.groups()) == 2:
            return self.only_(x.groups())

        x = search("^(" + cr + ")(" + cr + ")$", name, IGNORECASE)
        if x and len(x.groups()) == 2:
            g = x.group(1)
            return self.mat[self.parseNames(g[0].upper() + g[1:], x.group(2))]

        raise AttributeError("Attribut Non Trouvé (Simple Image)")

    def max_is_(self, row, col):
        """
        Fonction pour l'attribut de type maxTopIsLeft ou maxRightIsBottom
        """
        return self.nameToIndice(col) in self.max(self.nameToIndices(row))

    def only_(self, coord):
        """
        Fonction pour l'attribut de type onlyTopRight
        """
        y, x = self.parseNames(*coord)
        return (delete(self.mat.ravel(), 3 * y + x) < 10).all()

    def big_is_(self, row, col):
        """
        Fonction pour l'attribut de type bigBottomIsRight
        """
        row, col = self.parseNames(row, col)
        if col == 0:
            somme = self.mat[row, 1] + self.mat[row, 2]
        elif col == 1:
            somme = self.mat[row, 0] + self.mat[row, 2]
        elif col == 2:
            somme = self.mat[row, 0] + self.mat[row, 1]
        return self.mat[row, col] > somme

    def _BiggerThan_(self, name1, name2):
        """
        Fonction pour l'attribut de type topBiggerThanBottom
        ou leftBiggerThanRight
        """
        u = self.nameToIndices(name1[0].upper() + name1[1:])
        v = self.nameToIndices(name2)
        return sum(self.mat[u]) > sum(self.mat[v])

    def max(self, i):
        """
        Recherche les indices des éléments max dans un tableau

        Parameters
        ----------
        i : array
            Le vecteur de taille 3 dont on veut chercher le(s) max

        Returns
        -------
        int or None
            None si toutes les cases sont identiques, ou un vecteur des
            positions des indices max
        """
        if (self.mat[i] == self.mat[i][0]).all():
            return list()
        else:
            return array([0, 1, 2])[(self.mat[i] == max(self.mat[i]))]

    def max_lines(self):
        """
        Calcul le vecteur des maximums sur chaque ligne de la matrice

        Returns
        -------
        int or None
            None si toutes les cases sont identiques, ou un vecteur des
            positions des indices max
        """
        return [
            self.max((0, slice(None, None, None))),
            self.max((1, slice(None, None, None))),
            self.max((2, slice(None, None, None)))
        ]

    def parseName(self, name):
        """ Parse un nom de case (ex : topRight) """
        a, b = [i for i, e in enumerate(name) if e.isupper()]
        return self.parseNames(name[a:b], name[b:])

    def parseNames(self, a, b):
        """
        Transforme un nom de case complet (ligne, col) en
        indice de tableau
        """
        a = self.nameToIndices(a)
        b = self.nameToIndices(b)
        return (a[0] if b[0] == slice(None, None, None) else b[0],
                a[1] if b[1] == slice(None, None, None) else b[1])

    def nameToIndice(self, name):
        """ Transforme un nom de case en indice (entier) de tableau """
        try:
            return ar_cols.index(name)
        except ValueError:
            pass
        try:
            return ar_rows.index(name)
        except ValueError:
            pass

    def nameToIndices(self, name):
        """ Transforme un nom de case en indice (slice) de tableau """
        try:
            return (slice(None, None, None), ar_cols.index(name))
        except ValueError:
            pass
        try:
            return (ar_rows.index(name), slice(None, None, None))
        except ValueError:
            pass
