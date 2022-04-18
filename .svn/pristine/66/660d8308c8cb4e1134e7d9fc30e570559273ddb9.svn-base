from math import sqrt, atan, pi as PI

point1 = (0, 5)
point2 = (15, 5)
point3 = (15, 0)


def distance(pt1, pt2) :
	b, a = pt1
	y, x = pt2
	return sqrt((y - b) ** 2 + (x - a) ** 2)


def angle(pt1, pt2) :
	b, a = pt1
	y, x = pt2

	if (pt1 == pt2) :  # Même point
		return 0  # Pourrait renvoyer une erreur
	elif (b == y) :  # Même ligne => angle -90° ou 90°
		if a < x :
			return 90
		elif a > x :
			return -90
	elif (a == x) :  # Même colonne => angle 0°
		return 0
	elif (b < y) :
		angle(pt2, pt1)
	elif (b > y) :
		# Création triangle rectangle
		pt3 = y, a
		op = distance(pt2, pt3)
		adj = distance(pt1, pt3)
		ang = atan(op / adj)
		return ang * 180 / PI
