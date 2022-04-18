package application.interfaceGraphique;

import javafx.scene.control.TextArea;

public class Console {
	private static Console INSTANCE = new Console();
	private TextArea texteArea;
	private Console() {
		this.texteArea = new TextArea();
		this.texteArea.setEditable(false);
		this.texteArea.setLayoutX(25);
		this.texteArea.setLayoutY(250);
		this.texteArea.setPrefSize(325, 325);
	}
	public static Console getINSTANCE() {
		return INSTANCE;
	}
	public String getNode () {
		return texteArea.getText();
	}
	public void write (String text) {
		texteArea.setText(getNode()+text+"\n");
	}
	public TextArea getTexteArea() {
		return texteArea;
	}
}
