package application.interfaceGraphique;

import java.io.FileInputStream;
import java.io.FileNotFoundException;

import application.definition.Constantes;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.Pane;

public class MainPanel extends Pane {
	public MainPanel () {
		try {
			FileInputStream input = new FileInputStream(Constantes.IMAGE);
			Image image = new Image(input);
			ImageView imageView = new ImageView(image);
			imageView.setLayoutX(100);
			imageView.setLayoutY(25);
			imageView.setFitWidth(250);
			imageView.setFitHeight(80);
					
			this.getChildren().addAll(imageView);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		this.getChildren().addAll(VoyantsPanel.getINSTANCE().getVoyant1(), VoyantsPanel.getINSTANCE().getVoyant2());
		this.getChildren().addAll(VoyantsPanel.getINSTANCE().getLabel1(), VoyantsPanel.getINSTANCE().getLabel2());
		this.getChildren().addAll(BoutonsPanel.getINSTANCE().getStart(), BoutonsPanel.getINSTANCE().getStop());
		this.getChildren().addAll(Console.getINSTANCE().getTexteArea());
		this.getChildren().addAll(LecteurImage.getINSTANCE().getImageView());
	}
}
