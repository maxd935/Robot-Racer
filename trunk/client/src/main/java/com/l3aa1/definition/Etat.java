package com.l3aa1.definition;

/**
 * L'interface {@link Etat} fourni les méthodes necessaires
 * à la description d'un état qui sera associé à un voyant : 
 * <ul>
 * 	   <li>Nom de l'état</li>
 * 	   <li>Couleur du voyant associé</li>
 * 	   <li>Description de l'état</li>
 * </ul>
 *
 */
public interface Etat {
	/**
	 * Récupérer la couleur du voyant représentant cet état.
	 * 
	 * @return La couleur du voyant associé à cet état.
	 */
	public String  getCouleur();
	
	/**
	 * Récupérer la description de l'état.
	 * 
	 * @return La description
	 */
	public String getDescription();
	

	/**
	 * Récupérer le nom affichable de l'état.
	 * 
	 * @return Le nom
	 */
	public String getName();
}
