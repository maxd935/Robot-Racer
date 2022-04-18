"""
Ce module contient la classe config qui permet charger
des fichiers de configuration au format JSON.
"""
from json import load, loads as parse
from jsonmerge import merge
from os import listdir
from sys import argv

CONFIG_PATH = "./config/"
DEFAULT_CONFIG = 'default.json'


class Config:
    """
    Permet de charger des fichiers de configuration

    Attribut d'instance :
    - config : Contient la configuration actuelle
    """

    def __init__(self, fichiers_supplementaires=list()):
        self._config = parse("{}")
        self.ajouter(DEFAULT_CONFIG)

        self.loadAll(list(
            filter(lambda fich: fich.startswith("local"), listdir(CONFIG_PATH))
        ))
        self.loadAll(argv[1:])


    def loadAll(self, fichiers_supplementaires):
        """Charger un lot de fichiers"""
        for fich in fichiers_supplementaires:
            self.ajouter(fich)

    def ajouter(self, file=None):
        """ Ajouter un fichier JSON à la configuration actuelle"""
        if file is None:
            return
        try:
            with open(CONFIG_PATH + file, 'r') as fichier:
                self._config = merge(self._config, load(fichier))
                print("Configuration :\"", file, "\" chargé")
        except (OSError, ValueError) as err:
            print("Erreur lors de la lecture de {0} ({1})".format(file, err))

    def get(self, key):
        """
        Récupère la valeur de la clé
        La clé est au format key.subkey.subsubkey.

        Retourne la valeur de la clé ou None si elle n'existe pas.
        """
        data = self._config
        try:
            for k in key.split("."):
                data = data[k]
        except KeyError:
            print("Attention, une mauvaise clé a été utilisée : ", key)
            return None
        return data

    def __getattr__(self, name):
        """ Raccourcis pour get """
        attr = self.get(name.replace("__", "."))
        if attr is not None:
            return attr
        else:
            print(name, "n'est pas un paramètre valide.")
