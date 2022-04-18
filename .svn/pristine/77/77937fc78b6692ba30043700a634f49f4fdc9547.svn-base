package projet.l3aa1.gui;

import java.text.SimpleDateFormat;
import java.util.Date;

import javafx.scene.Node;
import javafx.scene.control.TextArea;

public class Console {
	private static Console instance = new Console();
	private TextArea textArea;
	private Console() {
		textArea = new TextArea();
		textArea.setPrefRowCount(5);
		textArea.setPrefColumnCount(50);
		textArea.setStyle("-fx-font-size: 25; ");
	}
	public static Node getNode() { return instance.textArea; }
	
	public static void write(String text) {
		String date = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss")
				          .format(new Date());

		instance.textArea.appendText("[" + date + "] " + text + System.lineSeparator());
	}
}
