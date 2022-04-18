package com.l3aa1.interfaceGraphique;

import java.awt.image.BufferedImage;

import com.l3aa1.definition.Constantes;
import com.l3aa1.reseaux.StreamingServer;

import javafx.application.Platform;
import javafx.embed.swing.SwingFXUtils;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;

/**
 * La classe {@link LecteurImage} représente l'élément graphique correspondant
 * au lecteur en streaming de la vidéo envoyée par le RPi.
 */
public class LecteurImage extends BorderPane {
	/**
	 * Unique instance de {@link LecteurImage}
	 */
	private static LecteurImage instance = new LecteurImage();
	
	/**
	 * Container de l'image
	 */
	private ImageView imageView;

	/**
	 * Constructeur :
	 * <ul>
	 * 	<li>Créer le buffer pour l'image en nuances de gris :
	 * 		un pixel est codé avec <b>un octet</b></li>
	 * 	<li>Création du thread en attente de nouvelles images</li>
	 * </ul>
	 */
	private LecteurImage() {
		imageView = new ImageView();
		imageView.setPreserveRatio(true);
		imageView.setFitWidth(Constantes.CONTAINER_WIDTH);
		imageView.setFitHeight(
				Constantes.IMG_HEIGHT
				* Constantes.CONTAINER_WIDTH
				/ Constantes.IMG_WIDTH
		);
		setCenter(imageView);

		Platform.runLater(() -> {
			Thread stream = new Thread(() -> {
				StreamingServer.getInstance().ecouter();
			});
			stream.setDaemon(true);
			stream.start();
		});
	}

	/**
	 * Met à jour l'image du buffer en attendant le prochain paquet
	 * , en convertissant les octets recus non signés en int signés
	 * et en mettant à jour l'élément graphique.
	 * 
	 * @param image La nouvelle image
	 */
	public static void setImage(BufferedImage image) {
		instance.imageView.setImage(SwingFXUtils.toFXImage(image, null));
	}

	
	/**
	 * Redimensionner l'objet imageView avec largeur et hauteur.
	 * Les dimensions sont des doubles car nous utilisons la
	 * méthode setFit[Height|Width]() qui utilise des doubles.
	 * 
	 * @param width		Nouvelle largeur
	 * @param height	Nouvelle hauteur
	 */
	public void setDimensions(double width, double height) {
		imageView.setFitHeight(height);
		imageView.setFitWidth(width);
	}
	
	/**
	 * Récupérer l'instance de {@link LecteurImage}.
	 * 
	 * @return L'instance de {@link LecteurImage}
	 */
	public static LecteurImage getInstance() {
		return instance;
	}
}