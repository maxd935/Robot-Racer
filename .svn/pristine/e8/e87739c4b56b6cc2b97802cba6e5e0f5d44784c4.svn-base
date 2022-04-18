package com.l3aa1.reseaux;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

import com.l3aa1.definition.Constantes;
import com.l3aa1.definition.EtatConnexion;
import com.l3aa1.interfaceGraphique.Console;
import com.l3aa1.interfaceGraphique.VoyantsPanel;

/**
 * ConnexionServeur
 * 
 * Cette classe permet les opérations de connexion et 
 * d'envoi d'instructions au Raspberry PI.
 * On utilise ici le pattern Singleton.
 */
public class ConnexionServeur {
	/**
	 * Socket pour se connecter au RPi
	 */
	private Socket socket = new Socket();
	
	/**
	 * Instance de {@link ConnexionServeur}
	 */
	private static ConnexionServeur instance = new ConnexionServeur();

	/**
	 * Cette methode permet de se connecter au Raspberry PI.
	 * Afin de ne pas rester bloquer indéfiniment, cette méthode peut
	 * echouer. Pour vérifier cela, il faut tester 
	 * avec <code>isConnected()</code>.
	 */
	public void connect() {
		if (isConnected())
			return;

		Console.write("Connexion ...");

		try {
			socket.connect(new InetSocketAddress(Constantes.IP_ROBOT, Constantes.PORT_ROBOT),
					Constantes.CONNEXION_TIMEOUT);
			Console.write("Connecté !");
			VoyantsPanel.set(EtatConnexion.CONNECTE);
		} catch (IOException e) {
			Console.write("Impossible de se connecter " + e.getMessage());
			close();
		}
	}

	/**
	 * Envoyer au robot l'instruction démarrer.
	 */
	public void start() {
		write("start");
		Console.write("Demande de démarrage envoyée");
	}

	/**
	 * Envoyer au robot l'instruction arrêter.
	 */
	public void stop() {
		write("stop");
		Console.write("Demande de stop envoyée");
	}

	/**
	 * Envoyer au robot une instruction de direction.
	 * 
	 * @param dirVerticale		Avant / Arrière
	 * @param dirHorizontale	Gauche / Droite
	 */
	public void sendDirection(String dirVerticale, String dirHorizontale) {
		if(!isConnected())
			connect();
			
		write("direction_" + dirVerticale + "_" + dirHorizontale);
	}

	/**
	 * Fermer la connexion établie avec le Raspberry PI.
	 */
	public void close() {
		try {
			socket.close();
			Console.write("Connexion au serveur close.");
		} catch (IOException e) {
			Console.write("Erreur lors de la fermeture de la socket " + e.getMessage());
		}
		socket = null;
		socket = new Socket();
	}

	/**
	 * Écrire une donnée au RaspBerry PI.
	 * La donnée ne doit contenir que des caractères simples provenant
	 * de l'alphabet ASCI.
	 * 
	 * @param	data	Les données à envoyer
	 * @return			True si réussi, False si une erreur est survenue
	 */
	private boolean write(String data) {
		if (socket != null) {
			try {
				socket.getOutputStream().write(data.getBytes());
				return true;
			} catch (NullPointerException e) {
				Console.write("Impossible d'écrire au serveur : socket invalide");
			} catch (IOException e) {
				Console.write("Impossible d'écrire au serveur : " + e.getMessage());
			}
		}
		Console.write("Non connecté au robot");
		return false;
	}

	/**
	 * Vérifie l'état de connexion au serveur
	 * du Raspberry PI.
	 * 
	 * @return		True si on est connecté au serveur, false sinon.
	 */
	public boolean isConnected() {
		return socket != null && socket.isConnected() && !socket.isClosed();
	}
	
	/**
	 * Récupérer l'unique instance de cette classe, conformément
	 * au design pattern Singleton.
	 * 
	 * @return	L'instance de {@link ConnexionServeur}
	 */
	public static ConnexionServeur getInstance() {
		return instance;
	}
}
