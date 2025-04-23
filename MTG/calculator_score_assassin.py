import json
import os
from datetime import datetime

def sauvegarder_partie(cibles_initiales, kills_order, ordre_morts, scores):
    partie = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cibles_initiales": cibles_initiales,
        "kills_order": kills_order,
        "ordre_morts": ordre_morts,
        "scores": scores
    }

    # Créer le dossier si besoin
    if not os.path.exists("sauvegardes"):
        os.makedirs("sauvegardes")

    nom_fichier = f"sauvegardes/partie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(partie, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Partie sauvegardée dans {nom_fichier}")


def saisir_joueurs_et_cibles():
    n = int(input("Nombre de joueurs : "))
    joueurs = []
    cibles = {}

    for i in range(n):
        nom = input(f"Nom du joueur {i+1} : ").strip()
        joueurs.append(nom)

    print("\n--- Attribution des cibles ---")
    for joueur in joueurs:
        cible = input(f"Cible de {joueur} : ").strip()
        while cible not in joueurs:
            print("❌ Cible invalide. Elle doit être un autre joueur existant.")
            cible = input(f"Cible de {joueur} : ").strip()
        cibles[joueur] = cible

    return cibles

def saisir_kills(cibles_initiales):
    kills_order = []
    ordre_morts = []
    vivants = set(cibles_initiales.keys())

    print("\n--- Saisie des kills ---")
    while len(vivants) > 1:
        print(f"\nJoueurs vivants : {', '.join(vivants)}")
        tueur = input("Tueur : ").strip()
        victime = input("Victime : ").strip()

        if tueur not in vivants or victime not in vivants:
            print("❌ Tueur ou victime invalide ou déjà mort.")
            continue

        if tueur == victime:
            print("❌ Un joueur ne peut pas se tuer lui-même.")
            continue

        kills_order.append((tueur, victime))
        ordre_morts.append(victime)
        vivants.remove(victime)

    # Ajouter le dernier survivant à la fin
    survivant = vivants.pop()
    ordre_morts.append(survivant)
    return kills_order, ordre_morts

def calculer_scores(cibles_initiales, kills_order, ordre_morts):
    scores = {joueur: 0 for joueur in cibles_initiales}
    cibles_actuelles = cibles_initiales.copy()
    vivants = set(cibles_initiales.keys())

    for tueur, victime in kills_order:
        if tueur not in vivants or victime not in vivants:
            continue

        cible_actuelle = cibles_actuelles.get(tueur)
        a_sa_propre_carte = cible_actuelle == tueur

        if a_sa_propre_carte:
            scores[tueur] += 2
        elif cible_actuelle == victime:
            scores[tueur] += 4
        else:
            scores[tueur] += 1

        # Mise à jour de la cible
        nouvelle_cible = cibles_actuelles.get(victime)
        cibles_actuelles[tueur] = nouvelle_cible

        vivants.remove(victime)

    # Points de placement
    for i, joueur in enumerate(ordre_morts):
        placement = i + 1
        scores[joueur] += placement

    return scores

# --- Saisie interactive des joueurs, cibles, et kills ---
cibles_initiales = saisir_joueurs_et_cibles()
kills_order, ordre_morts = saisir_kills(cibles_initiales)

scores = calculer_scores(cibles_initiales, kills_order, ordre_morts)
print("\n=== Scores finaux ===")
for joueur, score in scores.items():
    print(f"{joueur} : {score} points")

sauvegarder_partie(cibles_initiales, kills_order, ordre_morts, scores)