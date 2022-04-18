package application.definition;

public enum StatutRobot {
	ARRETE("Arrete"),
	DEMARRE("Demarre");
	
	private String texteLisible;
	
	private StatutRobot(String texte) {
		texteLisible = texte;
	}
	
	@Override
	public String toString() {
		return texteLisible;
	}
}
