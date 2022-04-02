black = "#000000"
blue = "#283493"
red = "#FF0000"

suffixes = ["e", "ice", "trice", "rice", "euse", "se"]
punctuation = [".", "-", "·"]
replaced = ["parl", "assistante"]
replacements = ["PARL", "assistant"]
france_bleu_words = ["montbéliard", "ardenne", "orne", "eure","étienne"]
articles = ["un", "une", "le", "la", "les", "aux", "du", "des", "à", "de", "d'", "et"]
capital = ["radio france", "philharmonique", "orchestre national de france"]
syndicats = ["CGT", "CFDT", "SUD", "UNSA", "SNJ", "FO"]

bleus = ["Alsace", "Armorique", "Auxerre", "Azur", "Béarn", "Bigorre", "Belfort-Montbéliard", "Berry", "Besançon", "Bourgogne", "Breizh Izel", "Champagne-Ardenne", "Cotentin", "Creuse", "Drôme Ardèche", "Elsass", "Gard Lozère", "Gascogne", "Gironde", "Hérault", "Isère", "La Rochelle", "Limousin", "Loire", "Océan", "Lorraine", "Nord", "Maine", "Mayenne", "Nord","Calvados", "Orne", "Normandie", "Seine-Maritime", "Eure", "Occitanie", "Orléans", "Paris", "Pays Basque", "Pays d'\Auvergne", "Pays de Savoie", "Périgord", "Picardie", "Poitou", "Provence", "RCFM", "Roussillon","Saint-Étienne", "Loire", "Sud", "Lorraine", "Touraine", "Vaucluse", "France Bleu", "FB", "Rouen", "Caen"]

valid = bleus + ["parl", "audiovisuels", "radiophoniques", "matinalier", "FB", "France Bleu", "La-Roche-sur-Yon"] 

labels = {"Technologie (ingénierie, maintenance et supports techniques)" : ["maintenance", "réseau", "télécom", "informatique", "systèmes", "assistance", "machinerie", "technologies", "développeur", "offres numériques"],
"Exploitation des moyens audiovisuels (technique)" : ["technicien supérieur du son", "technicien du son", "sonoris", "DPAV", "image", "reportage", "montage", "monteur", "responsable technique"],
"Production et suivi de programmes/information (production et coordination des moyens, numérique, documentation)" : ["production", "document", "biblio", "planificat", "programmes", "édition multimédia", "édition web", "création", "régisseur", "photographie", "éclairage"],
"Communication - Marketing" : ["communication", "presse", "partenariats", "médias", "réseaux sociaux", "publicité", "relations auditeurs", "média vendeur", "chargé d'études"],
"Animation radio" : ["parl", "animateur"],
"Gestion d’entreprise (gestion, comptabilité et finance, RH, juridique, achat, développement des ressources)" : ["directeur de radio locale", "gestion", "administrati", "paie", "personnels", "accueil", "audit", "assistant de direction", "contrat", "finances", "ressources humaines", "RH"],
"Journalisme" : ["journaliste", "matinalier", "rédacteur en chef", "secrétaire de rédaction", "présentateur"],
"Bâtiments, Logistique et Services (dont accueil sécurité et incendie)" : ["régisseur", "sécurité", "logistique", "maîtrise d'ouvrage"]}