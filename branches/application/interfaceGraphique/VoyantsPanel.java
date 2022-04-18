package application.interfaceGraphique;

import application.definition.EtatConnexion;
import application.definition.StatutRobot;
import javafx.scene.control.Label;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Font;

public class VoyantsPanel {
	private static VoyantsPanel INSTANCE = new VoyantsPanel();
	private EtatConnexion etatConnexion;
	private StatutRobot statutRobot;
	private Circle voyant1, voyant2;
	private Label label1, label2;
	private VoyantsPanel () {
		voyant1=new Circle();
		voyant1.setCenterX(520);//réglage de la position, de la taille et de la couleur du cercle
		voyant1.setCenterY(35);
		voyant1.setRadius(20);
		voyant1.setStroke(Color.BLACK);//réglage de la couleur de la bordure et de son épaisseur
		voyant1.setStrokeWidth(1);
		
		label1=new Label();
		label1.setFont(new Font(20));
		label1.setLayoutX(550);
		label1.setLayoutY(20);
        
		voyant2=new Circle();
		voyant2.setCenterX(520);//réglage de la position, de la taille et de la couleur du cercle
		voyant2.setCenterY(90);
		voyant2.setRadius(20);
		voyant2.setStroke(Color.BLACK);//réglage de la couleur de la bordure et de son épaisseur
		voyant2.setStrokeWidth(1);
		
		label2=new Label();
		label2.setFont(new Font(20));
		label2.setLayoutX(550);
		label2.setLayoutY(75);
		
		this.setEtatConnexion(EtatConnexion.DECONNECTE);
		this.setStatutRobot(StatutRobot.ARRETE);
	}
	public void setEtatConnexion(EtatConnexion etatConnexion) {
		this.etatConnexion = etatConnexion;
		this.setLabel1(etatConnexion);
	}
	public void setStatutRobot(StatutRobot statutRobot) {
		this.statutRobot = statutRobot;
		this.setLabel2(statutRobot);
	}
	private void setLabel1(EtatConnexion ec) {
		switch (ec) {
			case EN_RECHERCHE:
				voyant1.setFill(Color.YELLOW);
				label1.setText("EN RECHERCHE");	
				Console.getINSTANCE().write("EN ATTENDE DE LA CONNECTION AVEC LA VOITURE.");
				break;
			case CONNECTE:
				voyant1.setFill(Color.SPRINGGREEN);
				label1.setText("CONNECTE");	
				Console.getINSTANCE().write("CONNECTION ETABLIEE.");
				break;
			case DECONNECTE:
				voyant1.setFill(Color.MEDIUMPURPLE);
				label1.setText("DECONNECTE");	
				Console.getINSTANCE().write("VOITURE DECONNECTEE.");
				break;
			case INTROUVABLE:
				voyant1.setFill(Color.RED);
				label1.setText("INTROUVABLE");	
				Console.getINSTANCE().write("VOITURE INTROUVABLEE.");
				break;
		}
	}
	private void setLabel2(StatutRobot sr) {
		if (sr.equals(StatutRobot.DEMARRE)){
			voyant2.setFill(Color.SPRINGGREEN);
			label2.setText("DEMARRER");
			Console.getINSTANCE().write("DEMARRAGE DE LA VOITURE.");
		}
		if (sr.equals(StatutRobot.ARRETE)) {
			voyant2.setFill(Color.RED);
			label2.setText("ARRETE");
			Console.getINSTANCE().write("VOITURE A L'ARRET.");
		}
	}
	public static VoyantsPanel getINSTANCE() {
		return INSTANCE;
	}
	public Label getLabel2() {
		return label2;
	}
	public Label getLabel1() {
		return label1;
	}
	public Circle getVoyant1() {
		return voyant1;
	}
	public Circle getVoyant2() {
		return voyant2;
	}
	public EtatConnexion getEtatConnexion() {
		return etatConnexion;
	}
	public StatutRobot getStatutRobot() {
		return statutRobot;
	}
}
