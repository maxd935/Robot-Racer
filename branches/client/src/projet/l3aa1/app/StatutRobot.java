package projet.l3aa1.app;

public enum StatutRobot {
	ARRETE("Arrêté"),
	DEMARRE("Démarré");
	
	private String texteLisible;
	
	private StatutRobot(String texte) {
		texteLisible = texte;
	}
	
	@Override
	public String toString() {
		return texteLisible;
	}
}
