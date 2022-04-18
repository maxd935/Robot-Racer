package projet.l3aa1.app;

public enum EtatConnexion {
	EN_RECHERCHE("En recherche"),
	INTROUVABLE("Introuvable"),
	DECONNECTE("Déconnecté"),
	CONNECTE("Connecté");
	
	private String texteLisible;
	
	private EtatConnexion(String texte) {
		texteLisible = texte;
	}
	
	@Override
	public String toString() {
		return texteLisible;
	}
}
