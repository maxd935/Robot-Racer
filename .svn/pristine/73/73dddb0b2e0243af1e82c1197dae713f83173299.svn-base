"""
Le module ImageClass contient uniquement la classe Image, avec
la configuration du serveur UDP qui reçoit les images (le client).
"""
import cv2
import numpy as np
from time import sleep
from math import sqrt, atan, pi as PI
from controle import servo_dir, moteur
from datetime import datetime as dt
from config import get as conf
from serveur import Serveur
from os.path import exists
from os import makedirs as mkdir
from util import colsort, norme, points_to_droite, seuiller_shift_angle,\
	calcul_angle, distance, milieu_vert, findLignInColumn
from Rch_exceptions.Rch_Errors import NothingInColumnError as NICE


class Image:
	"""
	La classe Image représente une image et permet de réaliser les
	opérations de contrôle du robot nécessaire pour qu'il suive
	la ligne.
	Elle contient comme attributs de classe :
	- tailleImageY :    La hauteur de l'image
	- tailleImageX :    La largeur de l'image (calculée en fct de la hauteur)

	Et comme attributs privés :
	- image :       Image originale en nuances de gris et recadrée
	- image_thresh  Image seuillée
	"""
	POS_ROBOT = (conf("robot.capture.height")*(1-conf("image.ROI")) *
		conf("robot.distance"), conf("robot.capture.width")/2)
	MULT = -45 / calcul_angle(POS_ROBOT, (conf("robot.capture.height") *
	                                      (1-conf("image.ROI")) - 1, 0))

	def __init__(self, image):
		ignore = int(conf("image.ROI") * len(image))
		self._image = image[ignore:len(image)]
		self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)

	def isFin(self):
		"""
		Détecter la présence d'une ligne
		Seuillage de la ligne noire (pix<50)
		Compare le nbr de non-zero retrouvé l'image seuillé
		"""
		return 100 > cv2.countNonZero(cv2.threshold(
			self._image,
			conf("image.seuil.fin"), 255,
			cv2.THRESH_BINARY_INV)[1]
		                              )

	def isSurex(self):
		"""
		Détecter si une image est en surexposition ou non.

		Seuillage de la partie "Surex", partie de couleur blanche (pix>220)
		Compare le nbr de non-zero retrouvé l'image seuillé

		Renvoie True si l'image est en surexposition, False sinon.
		"""
		return 0 != cv2.countNonZero(cv2.threshold(
			self._image,
			conf("image.seuil.surex"), 255,
			cv2.THRESH_BINARY)[1])

	def log(self, categorie=None, img=None):
		if img is None:
			img = self._image
		path = "./log/" + (categorie + "/") if categorie is not None else ""
		filename = str(dt.isoformat(dt.now())) + ".png"
		if not exists(path):
			mkdir(path)
		cv2.imwrite(path + filename, img)
		sleep(1)

	def analyser(self):
		""" Logique de l'analyse d'image """
		if self.isFin():
			moteur.do("stop")
			self.log("fin")
			if conf("debug.general"):
				print("Pas de ligne détéctée")
		else:
			moteur.do("run")
		if self.isSurex():  # Pré-traitement
			if conf("debug.image.surex"):
				print("Is surex")
			self.log("surex")
			self.preTraitementSurex()
		else:
			if conf("debug.image.surex"):
				print("Not surex")
			self.preTraitementPasSurex()

		self.analyserVirage()

	def preTraitementSurex(self):
		img = cv2.blur(self._image, (7, 7))
		img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
		                            cv2.THRESH_BINARY_INV, 501, 25)
		# Transformations morphologiques
		kernel = np.ones((2, 2), np.uint8)
		img = cv2.erode(img, kernel, iterations=7)
		img = cv2.dilate(img, kernel, iterations=7)
		self._image_thresh = img

	def preTraitementPasSurex(self):
		cv2.medianBlur(self._image, int(len(self._image[0]) / 12.5),
		               dst=self._image)
		_, self._image_thresh = cv2.threshold(
			self._image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
		)

	def send(self, img=None):
		"""
		Envoyer l'image courante (ou passée en paramètre) sur le serveur UDP
		"""
		if Serveur.VIDEO_SOCKET is None:
			if conf("debug.network"):
				print("NO VIDEO SOCKET")
			return
		if img is None:
			img = self._image

		res, jpg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY),
		                                      conf("image.jpg_quality")])
		Serveur.VIDEO_SOCKET.sendall(
			int(jpg.size).to_bytes(4, 'big', signed=True)
			+ jpg.tobytes()
		)

	def shift_angle(self):
		"""
		Trouver le décallage et l'angle de la ligne.
		Angle : Angle que forme la ligne avec l'axe vertical.
				Est compris entre -90 et 90°.
		Décallage : décallage de la ligne par rapport au centre bas de l'image.
					Il est en pourcentage et oscille autour de 0% (peut
					dont être négatif)
		Par exemple :
		+----------+---------+
		|                |  ||
		|               /  / |
		|             /  /   |
		|            |  |    |
		+----------+--+-------+
				   |  |
			   milieu |
					  décallage de +10%

		"""
		# Contours
		img = self._image_thresh
		_, contours, _ = cv2.findContours(img, cv2.RETR_CCOMP,
		                                  cv2.CHAIN_APPROX_SIMPLE)

		if contours is None or len(contours) == 0:
			if conf("debug.image.analyse"):
				print("Image.shift_angle : Pas de contours trouvé")
			return None

		best_contours = max(contours, key=cv2.contourArea)

		(m, p), estCentree = self.approx_droite_rect(best_contours)
		xbottom = None
		if p is None:
			keepRect = False
			if not estCentree:
				m2, p2 = self.approx_droite_hough(best_contours)
				if p2 is not None:
					if conf("debug.image.angle_fct"):
						print("USE HUGH de hough")
					m, p = m2, p2
				else:
					keepRect = True
			if keepRect or estCentree:
				xbottom = m
				angle = 0

		if xbottom is None:
			angle = atan(m) * 180 / PI + 90 if m != 0 else 90
			xbottom = (len(img) - p) / m if m != 0 else m

		shift = int(100 * (2 * xbottom / len(img[0]) - 1))

		return (shift, angle)

	def approx_droite_hough(self, contours):
		"""
		Approximer la droite avec la transformée de Hough
		"""
		img_contours = np.zeros_like(self._image)
		img_contours = cv2.drawContours(img_contours, [contours], -1, 255, 2)

		# Suppression du contour des bordures
		padding = conf("image.padding_width")
		img_contours[:, :padding] = 0
		img_contours[:, -padding:] = 0
		img_contours[:padding, :] = 0
		img_contours[-padding:, :] = 0

		lines = cv2.HoughLinesP(img_contours, 1, np.pi / 180, 100,
		                        minLineLength=20, maxLineGap=20)

		res = list()
		if lines is not None:
			for line in lines:
				x1, y1, x2, y2 = line[0]
				# cv2.line(img, (x1, y1), (x2, y2), 127, 4)
				res.append(points_to_droite((x1, y1), (x2, y2)))

		# selection de la ligne la plus v
		if len(res) == 0:
			return None, None
		res = np.array(res)
		return res[res[:, 0] == res[:, 0].max()][0]

	def approx_droite_rect(self, contours):
		"""
		Calculer l'équation de la droite qui approche la ligne.
		Renvoie un tuple (param, estAuCentre), avec
		- param : un tuple (m, p) pour la droite d'equation y = m*x + p.
		  si la droite est de la forme x = constante, m = constante et p = None
		- estAuCentre : bool vrai si le centre du rectangle est à 50% autour du
		  centre de l'image
		"""
		(cx, cy), (height, width), angle = rect = cv2.minAreaRect(contours)

		# estAuCentre
		imY, imX = len(self._image) // 2, len(self._image[0]) // 2
		estAuCentre = True
		if cx > imX + imX // 2 or cx < imX - imX // 2:
			estAuCentre = False
		elif cy > imY + imY // 2 or cy < imY - imY // 2:
			estAuCentre = False
		if angle == 0.0:
			return (cx, None), estAuCentre

		box = np.int0(cv2.boxPoints(rect))

		box2 = colsort(box, 1)
		(h1, h2), (b1, b2) = colsort(box2[0:2]), colsort(box2[2:4])

		if norme(h1, h2) > norme(h2, b2):
			if h2[1] > h1[1]:
				h1, b2 = b2, h1
			elif h1[1] > h2[1]:
				b1, h2 = h2, b1

		mhx, mhy = (h1[0] + (h2[0] - h1[0]) / 2,
		            h1[1] + (h2[1] - h1[1]) / 2)
		mbx, mby = (b1[0] + (b2[0] - b1[0]) / 2,
		            b1[1] + (b2[1] - b1[1]) / 2)

		# draw = self._image_thresh.copy()
		# cv2.drawContours(draw, [box], 0, 127, 3)
		# cv2.line(draw, (int(mbx), int(mby)), (int(mhx), int(mhy)), 127)
		# self.send(draw)

		ret = points_to_droite((mbx, mby), (mhx, mhy))
		return ret, estAuCentre

	def analyserVirage(self):
		"""
		Changer la direction selon le décallage et l'angle de la ligne.
		"""
		resultat_analyse = self.shift_angle()
		txt = "{} -> ".format(np.around(resultat_analyse).astype(int))

		if resultat_analyse is None:
			if conf("debug.image.analyse"):
				print("analyse virage failed")
			self.log("analyseVirageFailure")
			return

		if resultat_analyse[1] > 90:
			if conf("debug.image.analyse"):
				print("angle too large")
			self.log("angleTooLarge")
			return

		shift, angle = seuiller_shift_angle(*resultat_analyse)



		if (angle < 0):
			direction = "gauche"
		elif (angle>0):
			direction = "droite"

		try :
			finLigne = findLignInColumn(self._image_thresh, direction)
			rotation = calcul_angle(self.POS_ROBOT, finLigne)
			temps_sleep = conf("robot.normal_sleep")
			if (abs(shift) > 80) :
				rotation *= self.MULT
				temps_sleep /= 2
			servo_dir.angle(rotation)
			sleep(temps_sleep)
		except (NICE, NameError) :
		# NameError <=> angle == 0 donc direction n'est pas défini
		# NICE      <=> la ligne ne sort pas de l'image
			txt += "{} -> ".format(np.around((shift, angle)).astype(int))
			if shift != 0:
				angle = int(sqrt(10 * (abs(shift) - 19)) + 10) * np.sign(shift)
				txt += " shift de {}".format(int(angle))
				servo_dir.angle(angle)
				sleep(conf("image.short_sleep"))
			elif angle != 0:
				txt += " angle de {}".format(int(angle))
				servo_dir.angle(angle // 2)
				sleep(conf("image.long_sleep"))
			else:
				servo_dir.angle(0)

			if conf("debug.image"):
				print(txt)
