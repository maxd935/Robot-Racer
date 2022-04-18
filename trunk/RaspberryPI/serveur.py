"""
Le module serveur contient uniquement la classe Serveur
et sa configuration.
"""
from socket import socket, create_connection
from threading import Thread
from controle import moteur, servo_dir
from time import sleep
from config import get as conf


class Serveur(Thread):
    """
    La classe Serveur créé un serveur TCP et permet de recevoir une
    connexion à la fois. Il attend ensuite une commande provenant de cette
    connexion, et l'execute.

    Liste des commandes :
    * start                                 Démarre la voiture
    * stop                                  Arrête la voiture
    * direction_[a|s|r]_[gg|g|s|d|dd]       Diriger manuellement le robot

    Attributes
    ----------
    robot : Robot
        Lien vers l'objet Robot
    direction : bool
        sens de marche du robot (True = avancer, False = Reculer)
    sock : socket
        socket du serveur recevant les commandes
    pad : bool
        True si on est en train d'utiliser le pad, False sinon
    VIDEO_SOCKET : socket
        socket pour envoyer la vidéo au client connecté

    """
    VIDEO_SOCKET = None

    def __init__(self, robot, portNo=conf("network.port.main")):
        super().__init__()
        self.setDaemon(True)  # Le thread s'arrête en même temps que le process
        self._robot = robot
        self._direction = True  # True : avancer, False : reculer
        self._sock = socket()
        self._sock.bind(("", portNo))
        self._sock.listen()
        self._pad = False

    def run(self):
        """
        La méthode run est appelée lorsque le thread est démarré en appelant
        la méthode start().
        Le serveur commence à attendre en boucle une nouvelle connexion.
        Lorsqu'une connexion est arrivée, on attend des instructions.
        Lorsque la connexion est rompue, on attend une prochaine connexion.
        """
        while True:
            if conf("debug.network"):
                print("En attente d'une connexion...")

            conn, (ip, port) = self._sock.accept()  # bloquant

            if conf("debug.network"):
                print("Nouvelle connexion de ", ip)

            while Serveur.VIDEO_SOCKET is None:
                print("On va se co au streaming")
                try:
                    Serveur.VIDEO_SOCKET = create_connection(
                        (ip, conf("network.port.stream"))
                    )
                except ConnectionRefusedError:
                    Serveur.VIDEO_SOCKET = None
                    if conf("debug.network"):
                        print("En attente de la création du serveur client")
                    sleep(0.2)

            while True:
                recu = conn.recv(1024).strip()  # bloquant
                if not recu:
                    break
                else:
                    self.do(recu)

            if conf("debug.network"):
                print("\t  Au revoir !")
            Serveur.VIDEO_SOCKET.close()
            Serveur.VIDEO_SOCKET = None

    def do(self, packet):
        """
        Execute l'action selon les données du paquet :

        Parameters
        ----------
        packet : str
            données du paquet.

        Returns
        -------
        void
            Rien.

        Notes
        -----
        Paquets :
        * start     :   Mettre la boucle d'analyse en position True
                        Lancer l'analyse dans un nouveau thread
        * stop      :   Arrêter le robot
                        Arrêter la boucle d'analyse
        * direction_* :  Ordres de contrôle manuel du robot
        """
        if packet == b'start':
            self._robot.init_vars()
            self.lancer_video(True)
            if conf("debug.network"):
                print("Commande START reçue")

        elif packet == b'stop':
            self._robot._video_on = False
            self._pad = False
            if conf("debug.network"):
                print("Commande STOP reçue")

            moteur.do("stop")

        elif packet[:9] == b'direction':
            if conf("debug.network"):
                print("Commande de direction :\"", packet[10:], "\"reçue")

            self.pad_control(packet[10:])
            if self._pad is False:
                self.lancer_video(False)
            self._pad = True
        else:
            print("Commande non reconnue : ", packet)

    def lancer_video(self, avecAnalyse):
        """
        Lancer le thread qui récupère / analyse / envoi la vidéo
        Si il en existe un déjà, on le termine et on en relance un
        avec l'argument passé en paramètre.

        Parameters
        ----------
        avecAnalyse : bool
            Analyser l'image (et auto-controller le robot)

        Returns
        -------
        void
            Rien.
        """
        if self._robot._video_on or self._pad:
            self._pad = False
            self._robot._video_on = False
            sleep(0.5)

        self._robot._video_on = True
        Thread(target=self._robot.start_video, args=(avecAnalyse,)).start()

    def pad_control(self, packet):
        """
        Commandes du control manuel du client


        Parameters
        ----------
        packet : str
            données du paquet.

        Notes
        -----
        |packet = [a|s|r]_[gg|g|s|d|dd]
        |    avec :  a = avancer
        |            s = stop
        |            r = reculer
        |            gg ou g = tourner roues au max à gauche ou un peu à gauche
        |            dd ou d = tourner roues au max à droite ou un peu à droite
        """
        petit_angle = 22
        grand_angle = 45

        # Contrôle avant / arrière
        if packet[0] == ord('a'):
            if not self._direction:
                # moteur.do("stop")
                moteur.do("inverser")
                self._direction = True
            moteur.do("run")
        elif packet[0] == ord('s'):
            moteur.do("stop")
        elif packet[0] == ord('r'):
            if self._direction:
                # moteur.do("stop")
                moteur.do("inverser")
                self._direction = False
            moteur.do("run")

        # Contrôle de la direction
        if packet[2:] == b's':
            servo_dir.angle(0)
        elif packet[2:] == b'g':
            servo_dir.angle(-petit_angle)
        elif packet[2:] == b'gg':
            servo_dir.angle(-grand_angle)
        elif packet[2:] == b'd':
            servo_dir.angle(petit_angle)
        elif packet[2:] == b'dd':
            servo_dir.angle(grand_angle)

    def __del__(self):
        self._sock.close()
