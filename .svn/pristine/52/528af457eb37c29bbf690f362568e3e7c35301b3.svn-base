package com.l3aa1.interfaceGraphique;

import java.text.SimpleDateFormat;
import java.util.Date;

import javafx.scene.Node;
import javafx.scene.control.TextArea;

/**
 * La classe {@link Console} représente la zone de texte où toute information de<br>
 * débug / d'information est écrite.
 * 
 * Elle doit pour cela être accessible de tout endroit dans le logiciel, c'est<br>
 * pourquoi nous utiliserons une méthode statique<br>
 * <code>write(String texte)</code>
 *
 */
public class Console {
	/**
	 * Instance de la Console
	 */
	private static Console instance = new Console();
	
	/**
	 * Instance du {@link TextArea}
	 */
	private TextArea textArea = new TextArea();

	/**
	 * Afin de pouvoir insérer la console dans la fenêtre, nous avons besoin d'avoir
	 * un accès à l'élément de type Node qui représente la zone de texte. C'est le
	 * rôle de cette fonction.
	 * 
	 * @return le Node associé à la {@link Console}
	 */
	public static Node getNode() {
		return instance.textArea;
	}

	/**
	 * Écrire un message dans la console.
	 * 
	 * @param message Le message
	 */
	public static void write(String message) {
		String date = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(new Date());

		instance.textArea.appendText("[" + date + "] " + message + System.lineSeparator());
	}
}
