package com.l3aa1.interfaceGraphique;

import java.util.Arrays;

import com.l3aa1.definition.Constantes;
import com.l3aa1.reseaux.ConnexionServeur;

import javafx.scene.control.Label;
import javafx.scene.input.MouseButton;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;

/**
 * La classe {@link ControlePad} offre un moyen de controller le robot depuis l'ordinateur.<br>
 * C'est une grille contenant des cases, et chaque cases correspond à<br>
 * faire avancer / tourner / ... le robot.<br>
 * Il y a 2 façons d'utiliser cette grille : <br>
 * 	- en cliquant sur la case<br>
 *  - en survolant la case<br>
 */

public class ControlePad extends GridPane {
	/**
	 * Permet de passer en mode bloqué (cliquer sur la case pour 
	 * changer le pad)
	 */
	private boolean isBloque = false;
	
	/**
	 * Coordonnées de la case enfoncée
	 */
	private int 	[]bloqueCoord;
	
	/**
	 * Labels composant le pad (boutons)
	 */
	private Label 	[][]labels = new Label[3][5];
	
	/**
	 * Constructeur : On initialise chaque case, en y joignant l'event.<br>
	 * On initialise également à stop / stop<br>
	 */
	public ControlePad() {
		getStylesheets().add("style.css");
		getStyleClass().add("controlepad");
		
		for(int i = 0; i < 3; i++) {
			for(int j = 0; j < 5; j++) {
				Label label = labels[i][j] = new Label();
				
				label.getStyleClass().add("controlepad_case");
				label.setPrefHeight(Constantes.CONTROLE_PAD_WIDTH);
				label.setPrefWidth(Constantes.CONTROLE_PAD_WIDTH * 3 / 5);
				
				addEvents(label, new int[] {i, j});

				setRowIndex(label, i);
				setColumnIndex(label, j);
				getChildren().add(label);
			}
		}
		
		labels[1][2].fireEvent(new MouseEvent(null, labels[1][2], MouseEvent.MOUSE_CLICKED, 0, 0, 0, 0, MouseButton.PRIMARY, 1, false	, false, false, false, true, false, false, false, false, false, null));
	}
	
	/**
	 * Ajoute les évènements liés à une case.<br>
	 * <ul>
	 * 	<li>Souris entre sur une case : si mode survol, on execute l'action</li>
	 * 	<li>Souris sort d'une case : si mode survol, on remet la case comme par défaut</li>
	 * 	<li>Souris clic sur une case :
	 * 			- Si mode survol, on passe en mode clic et on selectionne cette case.
	 * 			- Si mode clic:
	 * 				- Si nouvelle case = ancienne : on passe en mode survol
	 * 				- Sinon on selectionne la nouvelle case et execute les actions appropriées.
	 * </li>
	 * </ul>
	 * @param label		Label de la case
	 * @param coord		Coordonnées du label, vecteur d'entier (x; y)
	 */
	private void addEvents(Label label, int []coord) {
		label.addEventHandler(MouseEvent.MOUSE_EXITED, (event) -> {
			if(isBloque)
				return;
			clearHovered(coord[0], coord[1]);
		});
		
		label.addEventHandler(MouseEvent.MOUSE_CLICKED, (event) -> {
			clearHovered();
			if(isBloque) {
				if(Arrays.equals(coord, bloqueCoord)) {
					isBloque = false;
					label.getStyleClass().remove("blocked");
					label.getStyleClass().add("hovered");
					return ;
				}
				clearBlocked();
			}
			else
				isBloque = true;
			label.getStyleClass().add("blocked");
			doAction(coord[0], coord[1]);
			bloqueCoord = new int[] {coord[0], coord[1]};
		});
		
		label.addEventHandler(MouseEvent.MOUSE_ENTERED, (vent) -> {
			if(isBloque)
				return;
			label.getStyleClass().add("hovered");
			doAction(coord[0], coord[1]);
		});
	}

	/**
	 * Execute l'action liée à une case donnée
	 * 
	 * @param ligne		Ligne de la case
	 * @param colonne	Colonne de la case
	 */
	private void doAction(int ligne, int colonne) {
		String dirVerticale = "", dirHorizontale = "";
		
		switch (ligne) {
			case 0: dirVerticale = "a"; break;
			case 1: dirVerticale = "s"; break;
			case 2: dirVerticale = "r"; break;
		}
		
		switch (colonne) {
			case 0: dirHorizontale = "gg"; break;
			case 1: dirHorizontale = "g"; break;
			case 2: dirHorizontale = "s"; break;
			case 3: dirHorizontale = "d"; break;
			case 4: dirHorizontale = "dd"; break;
		}
		ConnexionServeur.getInstance().sendDirection(dirVerticale, dirHorizontale);
	}
	
	
	/******* Actions graphiques ******/
	/**
	 * Nettoyer le tableau des hover
	 */
	private void clearHovered() {
		for(int i = 0; i < 3; i++)
			for(int j = 0; j < 5; j++)
				clearHovered(i, j);
	}
	/**
	 * Nettoyer le tableau des cases bloquées
	 */
	private void clearBlocked() {
		for(int i = 0; i < 3; i++)
			for(int j = 0; j < 5; j++)
				clearClass(i, j, "blocked");
	}
	
	/**
	 * Nettoyer supprimer hover d'une case
	 * @param i  ligne
	 * @param j	 colonne
	 */
	private void clearHovered(int i, int j) {
		clearClass(i, j, "hovered");
	}

	/**
	 * Nettoyer supprimer la classe d'un label
	 * @param i  		ligne
	 * @param j	 		colonne
	 * @param className	Nom de la classe à supprimer
	 */
	private void clearClass(int i, int j, String className) {
		if(labels[i][j] != null) {
			labels[i][j].getStyleClass().remove(className);
		}
	}
}
