package com.l3aa1.definition;

/**
 * L'énumération {@link EtatConnexion} décrit l'état de la connexion entre le 
 * Raspberry PI et l'ordinateur du client.
 */
public enum EtatConnexion implements Etat {
	/**
	 * En attente de la connexion
	 */
	EN_RECHERCHE("En recherche", "jaune", "EN ATTENDE DE LA CONNECTION AVEC LA VOITURE."),
	
	/**
	 * Le robot est introuvable
	 */
	INTROUVABLE("Introuvable", "bleu", "VOITURE INTROUVABLE."),
	
	/**
	 * le robot est déconnecté
	 */
	DECONNECTE("Deconnecte", "rouge", "VOITURE DECONNECTEE."),
	
	/**
	 * Le robot est connecté
	 */
	CONNECTE("Connecte", "vert", "CONNECTION ETABLIE.");
	
	
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
	
	private EtatConnexion(String texte, String coul, String msg) {
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
