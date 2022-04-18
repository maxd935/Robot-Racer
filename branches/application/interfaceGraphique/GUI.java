package application.interfaceGraphique;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;

public class GUI extends Application {
	@Override
	public void start (Stage stage) throws Exception {
	stage.setTitle("Tableau de bord: ");
	Pane pane = new MainPanel();
	Scene scene = new Scene(pane, 725, 600);
	stage.setResizable(false);
	stage.setScene(scene);
	stage.sizeToScene();
	stage.show ();
	}
	public static void main (String [ ] args) {
		launch (args) ;
	}
}
