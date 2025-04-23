# MTGAssassination
🧙‍♂️ Assassin MTG – Suivi des parties
Application en Python pour gérer les parties du format Assassin dans Magic: The Gathering, avec :

Suivi des scores et kills,

Attribution des cibles IRL via cartes,

Gestion des joueurs et des decks,

Historique des parties,

Préparation pour les statistiques (ex: winrates par deck).

📁 Structure des fichiers

Fichier | Description
main.py | Script principal à exécuter pour jouer une partie.
gestion_des_joueurs.py | Script pour gérer la base des joueurs (ajouter/supprimer).
gestion_des_decks.py | Script pour gérer les decks (ajouter/supprimer).
sauvegardes/ | Dossier contenant les fichiers .json de chaque partie jouée.
joueurs.json | Fichier contenant la liste des joueurs disponibles.
decks.json | Fichier contenant la liste des decks disponibles.


🚀 Lancer une partie

Configurer les joueurs
Exécuter le script : python gestion_des_joueurs.py

Configurer les decks
Exécuter le script : python gestion_des_decks.py

Lancer une partie
Exécuter : python main.py

À chaque kill, le tueur révèle sa carte-cible (physique), et la saisit dans le programme.

📝 Données enregistrées
À chaque partie, un fichier est sauvegardé dans sauvegardes/, contenant :

Les joueurs et leurs decks,

L’ordre des kills (avec la cible révélée),

L’ordre de mort,

Les scores finaux.

🔜 À venir
Calcul automatique des winrates par deck.

Classements globaux.

Interface web ou mobile.
