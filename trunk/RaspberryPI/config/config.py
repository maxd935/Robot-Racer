"""
Ce module contient la classe config qui permet charger
des fichiers de configuration au format JSON.

Notes
-----
Tous les fichiers commençant par *local* seront automatiquement chargé
et les valeurs contenues dans le fichier local écraseront les valeurs du
fichier DEFAULT_CONFIG.

Attributes
----------
CONFIG_PATH : str
    dossier contenant les fichiers .json
DEFAULT_CONFIG : str
    nom du fichier .json de configuration par défaut.
"""
from json import load, loads as parse
from jsonmerge import merge
from os import listdir
from os.path import abspath, dirname
from sys import argv

# CONFIG_PATH = "./config/"
CONFIG_PATH = dirname(abspath(__file__)) + "/"
DEFAULT_CONFIG = 'default.json'


class Config:
    """
    Permet de charger des fichiers de configuration

    Atributes
    ----------
    _config : dict
        Contient la configuration actuelle
    """

    def __init__(self, fichiers_supplementaires=list()):
        self._config = parse("{}")
        self.ajouter(DEFAULT_CONFIG)

        self.loadAll(list(
            filter(lambda fich: fich.startswith("local"), listdir(CONFIG_PATH))
        ))
        self.loadAll(argv[1:])


    def loadAll(self, fichiers_supplementaires):
        """
        Charger un lot de fichiers

        Attributes
        ----------
        fichiers_supplementaires : iterable of str
            Fichiers à ajouter à la configuration actuelle.
        """
        for fich in fichiers_supplementaires:
            self.ajouter(fich)

    def ajouter(self, file=None):
        """
        Ajouter un fichier JSON à la configuration actuelle

        Attributes
        ----------
        file : iterable of str
            Fichier à ajouter à la configuration actuelle (en écrasant les vals)
        """
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
        Récupère la valeur de la clé.
        La clé est au format key.subkey.subsubkey.

        Attributes
        ----------
        key : str
            la clé

        Returns
        -------
        str or int or float or bool or list or dict or None
            La valeur de la clé ou None si elle n'existe pas.
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
