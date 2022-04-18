from .Algo_rch_milieu_ligne import reco_milieu_ligne as rml
from .Algo_rch_milieu_ligne import reco_milieu_colonne as rmc

maxAngleFront = 5 # Maybe récup dans Classe Constantes


def analyse(cam) :
	ht, lg = cam.shape
	ht -= 1
	lg -= 1
	pts = dict()

	# ON CHERCHE LA LIGNE EN BAS DE L'IMAGE
	try :
		pts[0] = rml (cam,ht)
	except (NoLignError) :
		# ON NE LA TROUVE PAS
		# ON LA CHERCHE UN PEU PLUS HAUT
		try :
			pts[0] = rml (cam,int(3*ht/4))
		except (NoLignError) :
			print("stop")

	# ON LA TROUVE ON LA CHERCHE A NV AU MILIEU DE L'IMAGE
	try :
		pts[1] = rml (cam,int(ht/2))
		pts[2] = rml (cam,0)
	except (NoLignError):
		# ON NE LA TROUVE PAS
		# ON LA CHERCHE SUR LES COTES
		try :
			pts[pts.__len__()] = rmc (cam, 0)
		except (NoColumnError) :
			try :
				pts[pts.__len__()] = rmc (cam, lg)
			except (NoColumnError) :
				print("stop")
