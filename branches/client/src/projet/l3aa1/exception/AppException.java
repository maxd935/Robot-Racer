package projet.l3aa1.exception;

import projet.l3aa1.gui.Console;
import projet.l3aa1.gui.MainPanel;

public class AppException extends Exception {
	private static final long serialVersionUID = 711313912464675616L;


	public AppException(MainPanel console, String message) {
		Console.write(message);
	}

	public AppException(MainPanel console) {
		Console.write("Une erreur inconnue à été levée.");
	}
}
