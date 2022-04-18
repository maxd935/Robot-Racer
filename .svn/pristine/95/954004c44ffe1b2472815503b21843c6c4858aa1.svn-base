package application.interfaceGraphique;

import application.definition.EtatConnexion;
import application.definition.StatutRobot;
import application.reseaux.ConnexionServeur;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.CornerRadii;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Font;

public class BoutonsPanel {
	private static BoutonsPanel INSTANCE = new BoutonsPanel();
	private Button start, stop;
	private BoutonsPanel () {
		start = new Button ("START");
		start.setFont(new Font(20));
		start.setBackground(new Background(new BackgroundFill(Color.CYAN, CornerRadii.EMPTY, Insets.EMPTY)));
		start.setShape(new Circle(1));
		start.setPrefSize(90, 90);
		start.setLayoutX(180);
		start.setLayoutY(135);
		start.setOnAction((event)->{
			for(int i = 0; i < 3 && !ConnexionServeur.getInstance().isConnected(); i++) {
				VoyantsPanel.getINSTANCE().setEtatConnexion(EtatConnexion.DECONNECTE);
				ConnexionServeur.getInstance().connect();
			}
			if(ConnexionServeur.getInstance().isConnected()) {
				VoyantsPanel.getINSTANCE().setEtatConnexion(EtatConnexion.CONNECTE);
				ConnexionServeur.getInstance().start();
				VoyantsPanel.getINSTANCE().setStatutRobot(StatutRobot.DEMARRE);
				Thread thread = new Thread(LecteurImage.getINSTANCE());
			    thread.start();
			}
			else {
				//A FAIRE
			}
		});
		
		stop = new Button ("STOP");
		stop.setFont(new Font(20));
		stop.setBackground(new Background(new BackgroundFill(Color.ORANGE, CornerRadii.EMPTY, Insets.EMPTY)));
		stop.setShape(new Circle(1));
		stop.setPrefSize(90, 90);
		stop.setLayoutX(455);
		stop.setLayoutY(135);
		stop.setOnAction((event)->{
			ConnexionServeur.getInstance().stop();
			VoyantsPanel.getINSTANCE().setStatutRobot(StatutRobot.ARRETE);			
		});
	}
	public static BoutonsPanel getINSTANCE() {
		return INSTANCE;
	}
	public Button getStart() {
		return start;
	}
	public Button getStop() {
		return stop;
	}
}
