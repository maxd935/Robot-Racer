package com.l3aa1.interfaceGraphique;

import com.l3aa1.definition.EtatConnexion;
import com.l3aa1.definition.StatutRobot;

import javafx.geometry.Orientation;
import javafx.scene.control.Label;
import javafx.scene.layout.FlowPane;

/**
 * La classe {@link VoyantsPanel} comprend l'ensemble des voynts
 * affichés sur le logiciel.
 */
public class VoyantsPanel extends FlowPane {
	/**
	 * Instance de {@link VoyantsPanel}
	 */
	private static VoyantsPanel instance = new VoyantsPanel();
	
	/**
	 * Label courant d'état du robot
	 */
	private Label labelEtatConnexion;
	
	/**
	 * Label courant de statut du robot
	 */
	private Label labelStatutRobot;

	/**
	 * Constructeur<br>
	 * 
	 * Création des labels dans un {@link FlowPane} vertical.
	 */
	private VoyantsPanel() {
		super(Orientation.VERTICAL);
		getStyleClass().add("voyants-pane");

		labelEtatConnexion = new Label("");
		labelEtatConnexion.getStyleClass().add("label-etat");

		labelStatutRobot = new Label("");
		labelStatutRobot.getStyleClass().add("label-etat");

		getChildren().addAll(labelEtatConnexion, labelStatutRobot);
	}

	/**
	 * Définir un nouvel état de connexion
	 * @see EtatConnexion
	 * @param etatConnexion Le nouvel état de connexion
	 */
	public static void set(EtatConnexion etatConnexion) {
		instance.labelEtatConnexion.setText(etatConnexion.getName());
		instance.labelEtatConnexion
				.getStyleClass()
				.removeIf((str) -> str.startsWith("icon"));
		instance.labelEtatConnexion.getStyleClass().add("icon-" + etatConnexion.getCouleur());
	}

	/**
	 * Définir un nouveau statut de robot
	 * @see StatutRobot
	 * @param statutRobot Le nouveau statut de robot
	 */
	public static void set(StatutRobot statutRobot) {
		instance.labelStatutRobot.setText(statutRobot.getName());
		instance.labelStatutRobot
				.getStyleClass()
				.removeIf((str) -> str.startsWith("icon"));
		instance.labelStatutRobot.getStyleClass().add("icon-" + statutRobot.getCouleur());
	}

	/**
	 * Récupérer l'instance de {@link VoyantsPanel}
	 * @return L'instance {@link VoyantsPanel}
	 */
	public static VoyantsPanel getInstance() {
		return instance;
	}
}
