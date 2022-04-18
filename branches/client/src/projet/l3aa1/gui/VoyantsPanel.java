package projet.l3aa1.gui;

import javafx.geometry.Orientation;
import javafx.geometry.Pos;
import javafx.geometry.VPos;
import javafx.scene.control.Label;
import javafx.scene.layout.FlowPane;
import projet.l3aa1.app.EtatConnexion;
import projet.l3aa1.app.StatutRobot;

public class VoyantsPanel extends FlowPane {
	Label     etatConnexion;
	Label     statutRobot;
	
	public VoyantsPanel() {
		super(Orientation.VERTICAL);
		etatConnexion = new Label(EtatConnexion.DECONNECTE.toString());
		statutRobot   = new Label(StatutRobot.ARRETE.toString());
		etatConnexion.setStyle("-fx-font-size: 25; ");
		statutRobot.setStyle("-fx-font-size: 25; ");
		
		getChildren().addAll(etatConnexion, statutRobot);
		

		setAlignment(Pos.TOP_RIGHT);
		setRowValignment(VPos.BASELINE);
		setPrefWrapLength(60);
	}

	public void setEtatConnexion(EtatConnexion etat) {
		etatConnexion.setText(etat.toString());
	}

	public void setStatutRobot(StatutRobot statut) {
		statutRobot.setText(statut.toString());
	}
}
