package projet.l3aa1.app;

import java.io.IOException;
import java.net.Socket;

import projet.l3aa1.gui.Console;

public class ConnexionServeur {
	
	private Socket socket;
	
	private static ConnexionServeur instance = new ConnexionServeur();
	private ConnexionServeur() { init(); }
	public static ConnexionServeur getInstance() {
		return instance;
	}
	
	private void init() {
//		socket = new Socket();;
	}
	
	public void connect() {
		if(socket != null && socket.isConnected()) 
			return;
		
		Console.write("Connexion ...");

		try {
			socket = new Socket(Constantes.IP_ROBOT, Constantes.PORT);
			Console.write("Connecté ...");
		} catch (IOException e) {
			Console.write("Impossible de se connecter " + e.getMessage());
		}
	}

	public void start() {
		write("start");
		Console.write("Demande de démarrage envoyée");
	}
	
	public void stop() {
		write("stop");
		Console.write("Demande de stop envoyée");
	}
	
	public void close() {
		try {
			socket.close();
			Console.write("Connexion au serveur close.");
		} catch (IOException e) {
			Console.write("Erreur lors de la fermeture de la socket "
						  + e.getMessage());
		}
	}
	
	private void write(String data) {
		try {
			if(socket == null)
				Console.write("Non connecté au robot");
			else
				socket.getOutputStream().write(data.getBytes());
		} catch (NullPointerException e) {
			Console.write("Impossible d'écrire au serveur : socket invalide");
		}catch (IOException e) {
			Console.write("Impossible d'écrire au serveur : " + e.getMessage());
		}
	}
	
	public boolean isConnected() {
		return socket != null && socket.isConnected();
	}
}
