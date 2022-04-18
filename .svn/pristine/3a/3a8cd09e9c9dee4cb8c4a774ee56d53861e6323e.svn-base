from config import get as conf
from math import sqrt, acos, pi as PI
from Rch_exceptions.Rch_Errors import NothingInColumnError as NICE


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


# Trier un tableau a selon une colonne d'indice b, par défaut égal à 0
colsort = lambda a, b=0: a[a[:, b].argsort()]

# Calcul la norme entre deux points (x, y)
norme = lambda a, b: sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def findLignInColumn(img, col) :
	col = 0 if (col == "gauche") else img.shape[1]-1
	lim_h = None
	lim_b = None
	milieu = int(img.shape[0] / 2)
	h = milieu - 1
	b = milieu + 1
	hauteur = img.shape[0] - 1

	if (img[milieu][col] == 255) :  # LE PIXEL DU MILIEU EST BLANC
		while (lim_h is None or lim_b is None) :
			if (lim_h is None) :
				if (h < 0 or img[h][col] == 0) :
					lim_h = h + 1
				else :
					h -= 1
			if (lim_b is None) :
				if (b > hauteur or img[b][col] == 0) :
					lim_b = b - 1
				else :
					b += 1

	else :  # LE PIXEL DU MILIEU N'EST PAS BLANC
		# TROUVE DE QUEL COTE EST LA LIGNE
		while (lim_h is None and lim_b is None and h >= 0 and b < hauteur) :
			if (img[h][col] == 255) :
				lim_b = h
			elif (img[b][col] == 255) :
				lim_h = b
			else :
				h -= 1
				b += 1

		# SI LA LIGNE N'A PAS ETE TROUVEE
		if (lim_h is None and lim_b is None) :
			raise NICE

		# SI LA LIGNE A ETE TROUVEE EN HAUT, CHERCHE LA LIMITE
		while (lim_h is None) :
			if (h < 0 or img[h][col] == 0) :
				lim_h = h + 1
			else :
				h -= 1

		# SI LA LIGNE A ETE TROUVEE EN BAS, CHERCHE LA LIMITE
		while (lim_b is None) :
			if (b > hauteur or img[b][col] == 0) :
				lim_b = b - 1
			else :
				b += 1

	return milieu_vert(lim_h, lim_b, col)



def milieu_vert(haut, bas, col) :
	return (haut + bas) / 2, col


def distance(pt1, pt2) :
	b, a = pt1
	y, x = pt2
	return sqrt((y - b) ** 2 + (x - a) ** 2)


def calcul_angle(base, pt2) :
	b, a = base
	y, x = pt2

	axe = (b-1, a)
	op  = distance(pt2, axe)
	adj = distance(base, axe)
	pt1_pt2 = distance(base, pt2)
	ang = acos ( (adj**2 + pt1_pt2**2 - op**2) / (2*adj*pt1_pt2) )
	# Passage en degrés
	ang *= 180/PI
	if (ang > 90) :
		ang -= 90
	if (x < a) :
		ang = -ang
	return ang
