package com.l3aa1.interfaceGraphique;

import com.l3aa1.definition.EtatConnexion;
import com.l3aa1.definition.StatutRobot;

import javafx.geometry.Orientation;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.FlowPane;

/**
 * La classe {@link MainPanel} est le conteneur graphique principal<br>
 * du logiciel.
 */
public class MainPanel extends BorderPane {
	/**
	 * Constructeur : Ajoute de haut en bas :
	 * <ul>
	 * 	<li>Le conteneur des voyants</li>
	 * 	<li>Les boutons Start/Stop</li>
	 * 	<li>La console</li>
	 * </ul>
	 */
	public MainPanel() {
		setBottom(Console.getNode());
		setTop(new TopMainPane());
		setCenter(new BoutonsPanel());
		
		VoyantsPanel.set(EtatConnexion.DECONNECTE);
		VoyantsPanel.set(StatutRobot.ARRETE);
	}
	
	/**
	 * Petit container pour les voyants.
	 * Il contient uniquement les voyants, et aligne le 
	 * bloc de voyants à droite.
	 */
	private static class TopMainPane  extends FlowPane {
		/**
		 * Constructeur initiant un FlowPane horizontal, 
		 * avec éléments alignés à droite.
		 */
		public TopMainPane() {
			super(Orientation.HORIZONTAL);
			getStyleClass().add("top-pane");
			getChildren().add(VoyantsPanel.getInstance());
		}
	}
}
