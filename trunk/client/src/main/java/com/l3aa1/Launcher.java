package com.l3aa1;

import com.l3aa1.definition.Constantes;
import com.l3aa1.interfaceGraphique.ControlePad;
import com.l3aa1.interfaceGraphique.MainPanel;
import com.l3aa1.reseaux.ConnexionServeur;
import com.l3aa1.reseaux.StreamingServer;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.stage.Stage;

/**
 * La classe Launcher est le réel point d'entrée de l'application.<br>
 * Elle permet d'initialiser le programme avec les fenêtres
 * nécessaires.
 */
public class Launcher extends Application {
	/**
	 * Fenêtre principale
	 */
	private static Stage primaryStage;

	/**
	 * Initialisation de JavaFX et de la fenêtre principale.
	 * 
	 * @param stage Le stage primaraire fourni par JFX
	 */
	@Override
	public void start (Stage stage) throws Exception {
		primaryStage = stage;
		Scene scene = new Scene(
				new MainPanel(),
				Constantes.WINDOW_WIDTH,
				Constantes.WINDOW_HEIGHT
		);
		stage.setScene(scene);
		stage.sizeToScene();
		scene.getStylesheets().add("style.css");
		setTitle(null);
		stage.setOnCloseRequest((event)->{
			Thread t = new Thread(()-> {
				ConnexionServeur.getInstance().close();
				try { Thread.sleep(200); }
				catch (InterruptedException e) { }
				StreamingServer.getInstance().close();
				Platform.exit();
			});
			t.setDaemon(true);
			t.start();
		});

		stage.show();

		if(Constantes.ACTIVATE_CONTROLS)
			setControls();
	}

	/**
	 * Création de la fenêtre permettant de contrôler la voiture<br>
	 * avec un pad (comme un télécommande).
	 */
	private void setControls() {
		Stage stage = new Stage();
		Scene scene = new Scene(new ControlePad());
		stage.setScene(scene);
		stage.sizeToScene();
		stage.show();
		stage.setX(primaryStage.getX() - stage.getWidth());
		stage.setY(primaryStage.getY());
	}

	/**
	 * Première fonction exécutée : envoie les arguments à JFX
	 *
	 * @param args	le vecteur d'arguments
	 */
	public static void main (String[] args) {
		if(args.length >= 1)
			Constantes.IP_ROBOT = args[0];
		System.out.println("IP du robot : " + Constantes.IP_ROBOT);
		launch(args) ;
	}

	/**
	 * Calcule l'abcisse la plus à droite de la fenêtre principale.
	 *
	 * @return	Le point X tout à droite
	 */
	public static double getX() {
		return primaryStage.getX() + primaryStage.getWidth();
	}

	/**
	 * Calcule le point le plus à droite de la fenêtre principale.
	 * 
	 * @return	Le point Y tout en haut de la fenêtre principale
	 */
	public static double getY() {
		return primaryStage.getY();
	}


	/**
	 * Ajouter un petit texte à la fin du titre
	 * de la fenêtre principale.
	 * Le texte ajouté est mis entre crochet.
	 * Si le texte est vide (null), alors le titre est celui par défaut.
	 *
	 * @param prefixe	Petit texte
	 */
	public static void setTitle(String prefixe) {
		if(prefixe == null || prefixe.length() == 0)
			primaryStage.setTitle(Constantes.WINDOW_TITLE);
		else
			primaryStage.setTitle(Constantes.WINDOW_TITLE + " [" + prefixe + "]");
	}

	/**
	 * Raccourcis pour <code>setTitle(null)</code>
	 */
	public static void setTitle() { setTitle(null); }
}
