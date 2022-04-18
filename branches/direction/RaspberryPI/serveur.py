import socket
from threading import Thread
from controle import moteur

PORT = 12345


class Serveur(Thread):
    """
    La classe Serveur créé un serveur TCP et permet de recevoir une
    connexion à la fois. Il attend ensuite une commande provenant de cette
    connexion, et l'execute.
    Liste des commandes :
    - start     Démarre la voiture
    - stop      Arrête la voiture
    """
    IP_CONNECTED = ""

    def __init__(self, robot, portNo=PORT):
        super().__init__()
        self.setDaemon(True)  # Le thread s'arrête en même temps que le process
        self._robot = robot
        self._sock = socket.socket()
        self._sock.bind(("", portNo))
        self._sock.listen()
        self._analyse = None

    def run(self):
        """
        La méthode run est appelée lorsque le thread est démarré en appelant
        la méthode start().
        Le serveur commence à attendre en boucle une nouvelle connexion.
        Lorsqu'une connexion est arrivée, on attend des instructions.
        Lorsque la connexion est rompue, on attend une prochaine connexion.
        """
        while True:
            print("En attente d'une connexion...")
            conn, (addr, port) = self._sock.accept()  # bloquant
            Serveur.IP_CONNECTED = addr
            print("Nouvelle connexion de ", addr)
            while True:
                recu = conn.recv(1024).strip()  # bloquant
                if not recu:
                    print("\t  Au revoir !")
                    break
                else:
                    self.do(recu)

    def do(self, packet):
        """ Execute l'action selon les données du paquet. """
        if packet == b'start' and not self._robot._video_on:
            moteur.do("run")
            self._robot._video_on = True
            Thread(target=self._robot.start_video).start()

        elif packet == b'stop':
            moteur.do("stop")
            self._robot._video_on = False
            print("STOP")
        else:
            print("Commande non reconnue : ", packet)

    def __del__(self):
        self._sock.close()
