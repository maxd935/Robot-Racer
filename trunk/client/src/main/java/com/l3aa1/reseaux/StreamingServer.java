package com.l3aa1.reseaux;

import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;

import javax.imageio.ImageIO;

import com.l3aa1.definition.Constantes;
import com.l3aa1.definition.EtatConnexion;
import com.l3aa1.definition.StatutRobot;
import com.l3aa1.interfaceGraphique.Console;
import com.l3aa1.interfaceGraphique.LecteurImage;
import com.l3aa1.interfaceGraphique.VoyantsPanel;

/**
 * StreamingServer
 * 
 * La classe StreamingServer créé un serveur TCP sur l'ordinateur courant
 * et permet de recevoir des trames contenant des images JPG.
 * 
 * Le pattern Singleton est utilisé pour cette classe.
 */
public class StreamingServer {
	/**
	 * Instance de {@link StreamingServer}
	 */
	private static final StreamingServer instance = new StreamingServer();
	
	/**
	 * Socket serveur du client pour le streaming et 
	 * qui permet de détécter la déconnexion du robot.
	 */
	private ServerSocket socket;

	/**
	 * Constructeur :
	 * Création de la socket, et nommage de cette socket.
	 */
	public StreamingServer() {
		try {
			socket = new ServerSocket(Constantes.PORT_UDP_LOCAL);
			socket.setReuseAddress(true);
			System.out.println("socket cree : " + socket.getLocalPort());
		} catch (SocketException e) {
			System.err.println("Impossible de créer la socket UDP : " + e.getMessage());
		} catch (IOException e) {
			System.err.println("Impossible de créer la socket TCP : " + e.getMessage());
		}
	}
	
	/**
	 * Boucle infinie qui écoute les connexions entrantes.
	 * Pas de multi thread / fork ici : uniquement une connexion 
	 * traitée à la fois.
	 */
	public void ecouter() {
		try {
			while(true) {
				Socket robot = socket.accept();
				Console.write("Robot (" + robot.getInetAddress()
							  + ") connecté au serveur vidéo");
				attendreImages(new DataInputStream(robot.getInputStream()));
			}
		} catch (IOException e) {
			Console.write("Erreur StreamingServer.ecouter()" + e.getMessage());
		}
	}
	
	/**
	 * On attend que le robot envoie des trames au format :
	 * <pre>
	 * +----------+------------------------------+
	 * | int size | byte[size] image_jpg_binaire |
	 * +----------+------------------------------+
	 * </pre>
	 * 
	 * @param buffer l'InputStream du robot
	 */
	private void attendreImages(DataInputStream buffer) {
		while(true) {
			try {
				LecteurImage.setImage(
					ImageIO.read(new ByteArrayInputStream(
							buffer.readNBytes(buffer.readInt())
					))
				);
			} catch (IOException e) {
				try {
					Thread.sleep(100);
				} catch (InterruptedException e1) { }
				Console.write("Déconnecté du serveur vidéo");
				if(!ConnexionServeur.getInstance().isConnected()) {
					VoyantsPanel.set(StatutRobot.ARRETE);
					VoyantsPanel.set(EtatConnexion.DECONNECTE);
				}
				break;
			}
		}
	}

	/**
	 * Fermer la socket.
	 */
	public void close() {
		try {
			socket.close();
		} catch (IOException e) {
			System.err.println("erreur lors de la fermeture de StreamingServer");
		}
	}

	
	/**
	 * Récupérer l'unique instance de cette classe, conformément
	 * au design pattern Singleton.
	 * 
	 * @return	L'instance de {@link StreamingServer}
	 */
	public static StreamingServer getInstance() {
		return instance;
	}
}
