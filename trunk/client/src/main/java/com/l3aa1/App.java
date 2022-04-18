package com.l3aa1;

/**
 * Point d'entrée du logiciel.<br>
 * <br>
 * La classe App est nécessaire à l'intégration de JavaFX à Maven, car
 * et au déploiement multiplateforme.<br>
 * Son seul rôle est donc d'appeler le <b>réel</b> main de la classe
 * Launcher.
 */
public class App {
	/**
	 * Appel de la fonction main
	 * 
	 * @param args Arguments passés en ligne de commande
	 */
    public static void main(String[] args) {
        Launcher.main(args);
    }
}