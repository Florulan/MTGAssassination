import json
import os

FICHIER_DECKS = "decks.json"

def charger_decks():
    if not os.path.exists(FICHIER_DECKS):
        return []
    with open(FICHIER_DECKS, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def sauvegarder_decks(decks):
    with open(FICHIER_DECKS, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=4)

def menu_gestion_decks():
    decks = charger_decks()

    while True:
        print("\n--- Gestion des decks ---")
        for i, d in enumerate(decks):
            print(f"{i+1}. {d}")
        print("a - Ajouter un deck")
        print("s - Supprimer un deck")
        print("q - Quitter")

        choix = input("Choix : ").strip().lower()
        if choix == 'a':
            nouveau = input("Nom du nouveau deck : ").strip()
            if nouveau and nouveau not in decks:
                decks.append(nouveau)
                print(f"✅ {nouveau} ajouté.")
            else:
                print("❌ Nom vide ou déjà existant.")
        elif choix == 's':
            idx = input("Numéro du deck à supprimer : ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(decks):
                supprimé = decks.pop(int(idx)-1)
                print(f"🗑️ {supprimé} supprimé.")
            else:
                print("❌ Numéro invalide.")
        elif choix == 'q':
            break
        else:
            print("❌ Choix invalide.")

    sauvegarder_decks(decks)
    print("✅ Modifications enregistrées.")

if __name__ == "__main__":
    menu_gestion_decks()
