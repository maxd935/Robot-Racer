import cv2
from serveur import Serveur
from ImageClass import Image

tailleImage = (32, 24)
tailleFenetre = (600, 600)
pourcentage_split = 0.5


class Robot:
	"""
	La classe robot représente le robot dans son ensemble.
	"""
	CAMERA_DEVICE = "/dev/video0"

	def __init__(self):
		self._cap = cv2.VideoCapture(self.CAMERA_DEVICE)
		self._video_on = False

	def start_video(self):
		print("start video ", self._video_on)
		while self._video_on:
			print("frame")
			ret, img = self._cap.read()      # Récuperer le flux
			if ret is False:                 # Si jamais il y a un erreur
				print("Impossible de joindre la caméra")
				exit(1)
			image = Image(img)
			#image.send()
			image.analyserVirage()

	def start_serveur(self):
		try:
			serveur = Serveur(self)
			serveur.start()
			serveur.join()
		except (KeyboardInterrupt, InterruptedError):
			print("Arrêt du serveur")
		finally:
			del(serveur)

	def __del__(self):
		# Libération des ressources
		pass


robot = Robot()
robot.start_serveur()
