import json
import os
from datetime import datetime
from gestion_des_joueurs import charger_joueurs

def afficher_choix(options):
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    choix = input("Choisissez un numéro : ").strip()
    while not choix.isdigit() or not (1 <= int(choix) <= len(options)):
        choix = input("❌ Choix invalide. Choisissez un numéro valide : ").strip()
    return options[int(choix) - 1]

def saisir_joueurs_depuis_liste():
    tous_les_joueurs = charger_joueurs()
    joueurs_choisis = []

    print("\n--- Sélection des joueurs pour cette partie ---")
    print("(Tapez ENTER sans rien pour finir)")

    while True:
        print("\nJoueurs disponibles :")
        restants = [j for j in tous_les_joueurs if j not in joueurs_choisis]
        if not restants:
            break
        for i, nom in enumerate(restants):
            print(f"{i+1}. {nom}")
        choix = input("Numéro du joueur à ajouter (ou ENTER pour terminer) : ").strip()
        if not choix:
            break
        if choix.isdigit() and 1 <= int(choix) <= len(restants):
            joueurs_choisis.append(restants[int(choix) - 1])
        else:
            print("❌ Choix invalide.")

    return joueurs_choisis

def saisir_kills_et_cibles(joueurs):
    kills_order = []
    ordre_morts = []
    vivants = set(joueurs)

    print("\n--- Saisie des kills ---")
    while len(vivants) > 1:
        print(f"\nJoueurs vivants : {', '.join(sorted(vivants))}")
        print("Sélection du tueur :")
        tueur = afficher_choix(sorted(vivants))

        print("Sélection de la victime :")
        victime = afficher_choix([j for j in sorted(vivants) if j != tueur])

        print(f"{tueur}, quelle carte-cible as-tu révélée ?")
        cible_revelee = afficher_choix(joueurs)

        kills_order.append((tueur, victime, cible_revelee))
        ordre_morts.append(victime)
        vivants.remove(victime)

    survivant = vivants.pop()
    ordre_morts.append(survivant)

    return kills_order, ordre_morts

def calculer_scores(kills_order, ordre_morts):
    joueurs = set()
    for tueur, victime, _ in kills_order:
        joueurs.add(tueur)
        joueurs.add(victime)
    for joueur in ordre_morts:
        joueurs.add(joueur)

    scores = {joueur: 0 for joueur in joueurs}
    vivants = set(scores.keys())

    for tueur, victime, cible in kills_order:
        if tueur not in vivants or victime not in vivants:
            continue

        if cible == tueur:
            scores[tueur] += 2
        elif cible == victime:
            scores[tueur] += 4
        else:
            scores[tueur] += 1

        vivants.remove(victime)

    for i, joueur in enumerate(ordre_morts):
        scores[joueur] += i + 1

    return scores

def sauvegarder_partie(kills_order, ordre_morts, scores):
    partie = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "kills_order": kills_order,
        "ordre_morts": ordre_morts,
        "scores": scores
    }

    if not os.path.exists("sauvegardes"):
        os.makedirs("sauvegardes")

    nom_fichier = f"sauvegardes/partie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(partie, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Partie sauvegardée dans {nom_fichier}")

# --- Lancement du jeu ---
joueurs = saisir_joueurs_depuis_liste()
kills_order, ordre_morts = saisir_kills_et_cibles(joueurs)
scores = calculer_scores(kills_order, ordre_morts)

print("\n=== Scores finaux ===")
for joueur, score in scores.items():
    print(f"{joueur} : {score} points")

sauvegarder_partie(kills_order, ordre_morts, scores)
