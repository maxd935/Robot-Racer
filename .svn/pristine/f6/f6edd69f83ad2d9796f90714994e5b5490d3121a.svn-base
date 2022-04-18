package application.interfaceGraphique;

import java.io.ByteArrayInputStream;
import application.reseaux.ConnexionServeur;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

public class LecteurImage implements Runnable {
	private static LecteurImage INSTANCE = new LecteurImage();
	private ImageView imageView;
	private LecteurImage() {
		imageView = new ImageView();
		imageView.setLayoutX(375);
		imageView.setLayoutY(250);
		imageView.setFitWidth(325);
		imageView.setFitHeight(325);
	}
	public void run() {
		while (ConnexionServeur.getInstance().isConnected()) {
			Image image = new Image(new ByteArrayInputStream(ConnexionServeur.getInstance().read()));
			imageView = new ImageView(image);
		}
	}
	public static LecteurImage getINSTANCE() {
		return INSTANCE;
	}
	public ImageView getImageView() {
		return imageView;
	}
}
