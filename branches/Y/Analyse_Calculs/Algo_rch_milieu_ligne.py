import cv2

nom_image = "ressources/vue_cam_1.jpg"
cam = cv2.imread(nom_image, cv2.IMREAD_GRAYSCALE)

# PRE-TRAITEMENT
# Taille de l'image de base
htCam, lgCam = cam.shape

ratioDivImage = 8
lg = int(lgCam / ratioDivImage)
ht = int(htCam / ratioDivImage)

cam = cv2.resize(cam, (lg, ht))
a, cam = cv2.threshold(cam, 127, 255, cv2.THRESH_BINARY)  # a == ? / Tous les bits sont 0 ou 255

# Showing image
cv2.namedWindow("namedWindow", cv2.WINDOW_NORMAL)
cv2.imshow("namedWindow", cam)
cv2.waitKey(0)
"""print("lg : " + str(lg) + "\tht : " + str(ht) + "\n")"""
print(cam.shape)

lg -= 1
ht -= 1

l0 = {}  # ligne 0


def milieu_vert(haut, bas, col) :
	return (haut + bas) / 2, col

def reco_milieu_colonne(img, col) :
	lim_h = None
	lim_b = None
	milieu = int(img.shape[0] / 2)
	h = milieu - 1
	b = milieu + 1
	hauteur = img.shape[0] - 1

	if (img[milieu][col] == 0) :  # LE PIXEL DU MILIEU EST NOIR
		while (lim_h is None or lim_b is None) :
			if (lim_h is None) :
				if (h < 0 or img[h][col] == 255) :
					lim_h = h + 1
				else :
					h -= 1
			if (lim_b is None) :
				if (b > hauteur or img[b][col] == 255) :
					lim_b = b - 1
				else :
					b += 1

	else :  # LE PIXEL DU MILIEU N'EST PAS NOIR
		while (lim_h is None and lim_b is None and h >= 0 and b < hauteur) :  # TROUVE DE QUEL COTE EST LA LIGNE
			if (img[h][col] == 0) :
				lim_b = h
			elif (img[b][col] == 0) :
				lim_h = b
			else :
				h -= 1
				b += 1

		# SI LA LIGNE N'A PAS ETE TROUVEE
		if (lim_h is None and lim_b is None) :
			raise NoColumnError

		# SI LA LIGNE A ETE TROUVEE EN HAUT, CHERCHE LA LIMITE
		while (lim_h is None) :
			if (h < 0 or img[h][col] == 255) :
				lim_h = h + 1
			else :
				h -= 1

		# SI LA LIGNE A ETE TROUVEE EN BAS, CHERCHE LA LIMITE
		while (lim_b is None) :
			if (b > hauteur or img[b][col] == 255) :
				lim_b = b - 1
			else :
				b += 1

	return milieu_vert(lim_h, lim_b, col)


# Renvoie une cood pour les calculs d'angles, pas besoin d'int
def milieu_hor(ligne, gauche, droite) :
	return ligne, (gauche + droite) / 2

def reco_milieu_ligne(img, ligne) :
	lim_g = None
	lim_d = None
	milieu = int(img.shape[1] / 2)
	g = milieu - 1
	d = milieu + 1
	longueur = img.shape[1] - 1

	if (img[ligne][milieu] == 0) :  # LE PIXEL DU MILIEU EST NOIR
		while (lim_g is None or lim_d is None) :
			if (lim_g is None) :
				if (img[ligne][g] == 255 or g < 0) :
					lim_g = g + 1
				else :
					g -= 1
			if (lim_d is None) :
				if (img[ligne][d] == 255 or d > longueur) :
					lim_d = d - 1
				else :
					d += 1

	else :  # LE PIXEL DU MILIEU N'EST PAS NOIR
		while (lim_g is None and lim_d is None and g >= 0 and d < longueur) :  # TROUVE DE QUEL COTE EST LA LIGNE
			if (img[ligne][g] == 0) :
				lim_d = g
			elif (img[ligne][d] == 0) :
				lim_g = d
			else :
				g -= 1
				d += 1

		# SI LA LIGNE N'A PAS ETE TROUVEE
		if (lim_g is None and lim_d is None) :
			raise NoLignError

		# SI LA LIGNE A ETE TROUVEE A GAUCHE, CHERCHE LA LIMITE
		while (lim_g is None) :
			if (img[ligne][g] == 255 or g < 0) :
				lim_g = g + 1
			else :
				g -= 1

		# SI LA LIGNE A ETE TROUVEE A DROITE, CHERCHE LA LIMITE
		while (lim_d is None) :
			if (img[ligne][d] == 255 or d > longueur) :
				lim_d = d - 1
			else :
				d += 1

	return milieu_hor(ligne, lim_g, lim_d)


# Test reco_milieu_ligne sur première et derniere lignes
"""print("On cherche les coordonnées du milieu de la ligne noire à une hauteur de 0")
if (ratioDivImage == 3) :
	if (nom_image == "vue_cam_1.jpg") :
		print("print(reco_milieu_ligne(cam,0)) is supposed to print (0,86.5)")
	elif (nom_image == "vue_cam_2.jpg") :
		print("print(reco_milieu_ligne(cam,0)) is supposed to print (0,126.5)")
	elif (nom_image == "test_vue_cam_coin.jpg") :
		print("Résultat prévisible : IndexError out of bounds")
	print("-> " + str(reco_milieu_ligne(cam, 0)))

	if (nom_image == "vue_cam_1.jpg") :
		print("print(reco_milieu_ligne(cam,ht)) is supposed to print (159,75)")
	elif (nom_image == "vue_cam_2.jpg") :
		print("print(reco_milieu_ligne(cam,ht)) is supposed to print (159,90.5)")
print("-> " + str(reco_milieu_ligne(cam, ht)))"""

"""print ("1 : " + str(reco_milieu_colonne(cam,14)))
print ("2 : " + str(reco_milieu_colonne(cam,42)))
print ("3 : " + str(reco_milieu_ligne(cam,6)))
print ("4 : " + str(reco_milieu_ligne(cam,51)))
"""