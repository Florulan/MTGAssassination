import json
import os

FICHIER_JOUEURS = "joueurs.json"

def charger_joueurs():
    if not os.path.exists(FICHIER_JOUEURS):
        return []
    with open(FICHIER_JOUEURS, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def sauvegarder_joueurs(joueurs):
    with open(FICHIER_JOUEURS, 'w', encoding='utf-8') as f:
        json.dump(joueurs, f, ensure_ascii=False, indent=4)

def menu_gestion_joueurs():
    joueurs = charger_joueurs()

    while True:
        print("\n--- Gestion des joueurs ---")
        for i, j in enumerate(joueurs):
            print(f"{i+1}. {j}")
        print("a - Ajouter un joueur")
        print("s - Supprimer un joueur")
        print("q - Quitter")

        choix = input("Choix : ").strip().lower()
        if choix == 'a':
            nouveau = input("Nom du nouveau joueur : ").strip()
            if nouveau and nouveau not in joueurs:
                joueurs.append(nouveau)
                print(f"✅ {nouveau} ajouté.")
            else:
                print("❌ Nom vide ou déjà existant.")
        elif choix == 's':
            try:
                idx = int(input("Numéro du joueur à supprimer : ").strip()) - 1
                if 0 <= idx < len(joueurs):
                    supprimé = joueurs.pop(idx)
                    print(f"🗑️ {supprimé} supprimé.")
                else:
                    print("❌ Numéro invalide.")
            except ValueError:
                print("❌ Veuillez entrer un numéro.")
        elif choix == 'q':
            break
        else:
            print("❌ Choix invalide.")

    sauvegarder_joueurs(joueurs)
    print("✅ Modifications sauvegardées.")

if __name__ == "__main__":
    menu_gestion_joueurs()
