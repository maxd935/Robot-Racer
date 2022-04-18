package com.l3aa1.definition;


/**
 * L'énumération {@link StatutRobot} décrit l'état du robot : en marche, arrêté.
 */
public enum StatutRobot implements Etat {
	/**
	 * La voiture est à l'arrêt.
	 */
	ARRETE("Arrete", "rouge", "VOITURE A L'ARRET."),
	
	/**
	 * La voiture est démarrée.
	 */
	DEMARRE("Demarre", "vert", "DEMARRAGE DE LA VOITURE.");
	
	
	/**
	 * Nom du voyant
	 */
	private String name;
	
	/**
	 * Message à afficher dans la console
	 */
	private String description;
	
	/**
	 * Couleur du voyant
	 */
	private String couleur;
	
	private StatutRobot(String texte, String coul, String msg) {
		name = texte;
		couleur = coul;
		description = msg;
	}
	
	@Override
	public String getCouleur() { return couleur; }

	@Override
	public String getDescription() { return description; }

	@Override
	public String getName() { return name; }
}
