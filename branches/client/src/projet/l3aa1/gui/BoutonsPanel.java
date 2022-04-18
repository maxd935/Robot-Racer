package projet.l3aa1.gui;

import javafx.event.ActionEvent;
import javafx.geometry.Orientation;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.layout.FlowPane;
import projet.l3aa1.app.ConnexionServeur;
import projet.l3aa1.app.EtatConnexion;
import projet.l3aa1.app.StatutRobot;

public class BoutonsPanel extends FlowPane {
	VoyantsPanel voyants;
	
	public BoutonsPanel(VoyantsPanel voyantsPanel) {
		super(Orientation.HORIZONTAL);
		voyants = voyantsPanel;
		Button start = new Button("START");
		Button stop  = new Button("STOP");
		start.setStyle("-fx-font-size: 40; ");
		stop.setStyle("-fx-font-size: 40; ");

		start.setOnAction((ActionEvent e) -> {
			for(int i = 0; i < 3 && !ConnexionServeur.getInstance().isConnected(); i++) {
				voyantsPanel.setEtatConnexion(EtatConnexion.DECONNECTE);
				ConnexionServeur.getInstance().connect();
			}
			if(ConnexionServeur.getInstance().isConnected()) {
				voyantsPanel.setEtatConnexion(EtatConnexion.CONNECTE);
				ConnexionServeur.getInstance().start();
				voyantsPanel.setStatutRobot(StatutRobot.DEMARRE);
			}
		});
		
		stop.setOnAction((ActionEvent e) -> {
			ConnexionServeur.getInstance().stop();
			voyantsPanel.setStatutRobot(StatutRobot.ARRETE);
		});
		
		getChildren().addAll(start, stop);
		
		setAlignment(Pos.CENTER);
		setPrefHeight(40);
		setHgap(10);
	}
}
