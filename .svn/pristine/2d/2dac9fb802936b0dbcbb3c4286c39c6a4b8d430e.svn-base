package projet.l3aa1.gui;

import javafx.scene.layout.BorderPane;

public class MainPanel extends BorderPane {
	private BoutonsPanel boutonsPanel;
	private VoyantsPanel voyantsPanel;
	
	public MainPanel() {
		voyantsPanel = new VoyantsPanel();
		boutonsPanel = new BoutonsPanel(voyantsPanel);

		setTop(voyantsPanel);
		setCenter(boutonsPanel);
		setBottom(Console.getNode());
	}
}
