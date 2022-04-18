package com.l3aa1.interfaceGraphique;

import com.l3aa1.Launcher;
import com.l3aa1.definition.Constantes;
import com.l3aa1.definition.EtatConnexion;
import com.l3aa1.definition.StatutRobot;
import com.l3aa1.reseaux.ConnexionServeur;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Orientation;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.FlowPane;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

/**
 * La classe {@link BoutonsPanel} représente le groupe de bouton<br>
 * start et stop.<br>
 * Elle comprend par conséquent les éléments nécessaires à l'ouverture<br>
 * et la fermeture de la seconde fenêtre pour avoir une vision de <br>
 * la caméra.
 */
public class BoutonsPanel extends FlowPane {
	/**
	 * Fenêtre comportant le retour vidéo.
	 */
	private Stage videoStage;
	
	/**
	 * Scène que compose la fenêtre <code>videoStage</code>
	 */
	private final Scene videoScene;
	
	/**
	 * Instance de {@link LecteurImage}
	 */
	private LecteurImage lecteur;
	
	/**
	 * Constructeur : initialise les boutons, et les éléments<br>
	 * necessaire à la fenêtre de streaming.<br>
	 * <br>
	 * Le bouton <b>start</b> :
	 * <ul>
	 * 		<li>Se connecte si besoin au RPi</li>
	 * 		<li>Lance une demande type "démarrer" au RPi</li>
	 * 		<li>Ouvre une fenêtre pour visionner la caméra du robot</li>
	 * 		<li>Met à jour le titre de la fenêtre</li>
	 * </ul><br>
	 * 
	 * Le bouton <b>stop</b> :
	 * <ul>
	 * 		<li>Lance une demande type "stop" au RPi</li>
	 * 		<li>Ferme la fenêtre de streaming</li>
	 * 		<li>Met à jour le titre de la fenêtre</li>
	 * </ul>
	 */
	public BoutonsPanel() {
		super(Orientation.HORIZONTAL);
		this.getStyleClass().add("boutons-panel");
		createStartButton();
		createStopButton();
		
		lecteur = LecteurImage.getInstance();
		videoScene = new Scene(lecteur);
		if(Constantes.ACTIVATE_CONTROLS) 
			openWindow();

	}

	
	/**
	 * Création du bouton STOP
	 * Celle méthode inclut l'ajout au pane du bouton.
	 */
	private void createStopButton() {
		Button button = new Button("STOP");
		button.getStyleClass().add("btn-stop");
		
		button.setOnAction(new EventHandler<ActionEvent>() {
			private long lastClick = 0;
			
			@Override
			public void handle(ActionEvent event) {
				ConnexionServeur.getInstance().stop();
				VoyantsPanel.set(StatutRobot.ARRETE);
				if(!Constantes.ACTIVATE_CONTROLS && videoStage != null) {
					videoStage.close();
					videoStage = null;
				}
				Launcher.setTitle("arrêté");
				
				long clickTime = System.currentTimeMillis();
				if(clickTime - lastClick <= 500) {
					ConnexionServeur.getInstance().close();
					VoyantsPanel.set(EtatConnexion.DECONNECTE);
					Launcher.setTitle("déconnecté");
				}
				
				lastClick = clickTime;
			}
			
		});
		getChildren().add(button);
	}

	
	/**
	 * Création du bouton START
	 * Celle méthode inclut l'ajout au pane du bouton.
	 */
	private void createStartButton() {
		Button button = new Button("START");
		button.getStyleClass().add("btn-start");
		getChildren().add(button);
		
		button.setOnAction((event) -> {

			if (!ConnexionServeur.getInstance().isConnected()) {
				VoyantsPanel.set(EtatConnexion.DECONNECTE);
				ConnexionServeur.getInstance().connect();
			}
			else {
				System.out.println("Deja co");
			}
			if (ConnexionServeur.getInstance().isConnected()) {
				VoyantsPanel.set(EtatConnexion.CONNECTE);
				ConnexionServeur.getInstance().start();
				VoyantsPanel.set(StatutRobot.DEMARRE);
				if(!Constantes.ACTIVATE_CONTROLS)
					openWindow();
				Launcher.setTitle("en marche");
			}
		});
	}
	
	/**
	 * Création de la fenêtre de streaming, en utilisant
	 * la Scene déclarée dans les attributs.
	 * Cette fenêtre est alignée sur le bord droit de la fenêtre
	 * principale.
	 * Lorsque cette fenêtre est redimensionnée, on redimensionne également 
	 * le lecteur en faisant attention à maximiser sa taille dans la fenêtre.
	 */
	private void openWindow() {
        videoStage = new Stage();
        videoStage.setTitle("Stream");
        videoStage.setScene(videoScene);
        videoStage.sizeToScene();
        videoStage.setX(Launcher.getX());
        videoStage.setY(Launcher.getY());
		
        videoStage.setOnShown((WindowEvent event) -> {
	    		ChangeListener<Number> resize = (ObservableValue<? extends Number> observable, Number oldValue, Number newValue) -> {
	    			double height = videoStage.getHeight();
	    			double width = videoStage.getWidth();
	
	    			if(height > 3 * width / 4)
	    				lecteur.setDimensions(width, 3 * width / 4);
	    			else
	    				lecteur.setDimensions(4 * height / 3, height);
	    		};
	    		
				videoStage.widthProperty().addListener(resize);
				videoStage.heightProperty().addListener(resize);
		});
        
        videoStage.show();
	}
}
