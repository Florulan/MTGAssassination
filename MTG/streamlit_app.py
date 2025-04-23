import streamlit as st
import json
import os
from datetime import datetime

# Préparer le contenu du script Streamlit complet
streamlit_code = """\
import streamlit as st
import json
import os
from datetime import datetime

# --- Fonctions utilitaires ---
def charger_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def sauvegarder_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Chargement initial ---
joueurs_path = "joueurs.json"
decks_path = "decks.json"
sauvegardes_path = "sauvegardes"

if not os.path.exists(sauvegardes_path):
    os.makedirs(sauvegardes_path)

joueurs = charger_json(joueurs_path)
decks = charger_json(decks_path)

# --- Interface Streamlit ---
st.set_page_config(page_title="Assassin MTG", layout="centered")
st.sidebar.title("Menu")
page = st.sidebar.radio("Navigation", ["🎮 Nouvelle Partie", "🛠️ Gérer Joueurs & Decks"])

# --- PAGE 1 : Nouvelle Partie ---
if page == "🎮 Nouvelle Partie":
    st.title("🎮 Nouvelle Partie - Assassin MTG")
    joueurs_choisis = st.multiselect("Sélectionnez les joueurs :", joueurs)
    decks_par_joueur = {}

    if joueurs_choisis:
        st.subheader("Choix des decks :")
        for joueur in joueurs_choisis:
            decks_par_joueur[joueur] = st.selectbox(f"{joueur} joue avec :", decks, key=joueur)

    if joueurs_choisis and st.button("Commencer la partie"):
        st.session_state["en_partie"] = True
        st.session_state["vivants"] = joueurs_choisis.copy()
        st.session_state["kills"] = []
        st.session_state["ordre_morts"] = []
        st.session_state["decks"] = decks_par_joueur
        st.success("Partie lancée !")

    if "en_partie" in st.session_state and st.session_state["en_partie"]:
        st.subheader("Saisie des kills")
        vivants = st.session_state["vivants"]

        if len(vivants) > 1:
            tueur = st.selectbox("Tueur :", vivants, key="tueur")
            victime = st.selectbox("Victime :", [v for v in vivants if v != tueur], key="victime")
            cible = st.selectbox("Cible révélée par le tueur :", joueurs, key="cible")

            if st.button("Valider le kill"):
                st.session_state["kills"].append((tueur, victime, cible))
                st.session_state["ordre_morts"].append(victime)
                st.session_state["vivants"].remove(victime)
                st.success(f"{tueur} a tué {victime} (cible révélée : {cible})")

        else:
            survivant = st.session_state["vivants"][0]
            st.session_state["ordre_morts"].append(survivant)
            st.subheader("🎉 Fin de partie")
            kills = st.session_state["kills"]
            morts = st.session_state["ordre_morts"]
            scores = {}

            for joueur in joueurs_choisis:
                scores[joueur] = 0

            vivants = joueurs_choisis.copy()
            for tueur, victime, cible in kills:
                if tueur not in vivants or victime not in vivants:
                    continue
                if cible == tueur:
                    scores[tueur] += 2
                elif cible == victime:
                    scores[tueur] += 4
                else:
                    scores[tueur] += 1
                vivants.remove(victime)

            for i, joueur in enumerate(morts):
                scores[joueur] += i + 1

            st.write("## Scores finaux")
            for joueur, score in scores.items():
                st.write(f"**{joueur}** ({st.session_state['decks'][joueur]}) : {score} points")

            partie = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "kills_order": kills,
                "ordre_morts": morts,
                "scores": scores,
                "decks": st.session_state["decks"]
            }
            nom_fichier = f"sauvegardes/partie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            sauvegarder_json(partie, nom_fichier)
            st.success(f"Partie sauvegardée dans `{nom_fichier}`")

            st.session_state.clear()

# --- PAGE 2 : Gérer Joueurs & Decks ---
if page == "🛠️ Gérer Joueurs & Decks":
    st.title("🛠️ Gestion des Joueurs et Decks")

    st.subheader("👤 Joueurs")
    nouveau_joueur = st.text_input("Ajouter un joueur")
    if st.button("Ajouter joueur"):
        if nouveau_joueur and nouveau_joueur not in joueurs:
            joueurs.append(nouveau_joueur)
            sauvegarder_json(joueurs, joueurs_path)
            st.success(f"{nouveau_joueur} ajouté.")

    joueur_a_supprimer = st.selectbox("Supprimer un joueur :", joueurs) if joueurs else None
    if st.button("Supprimer joueur") and joueur_a_supprimer:
        joueurs.remove(joueur_a_supprimer)
        sauvegarder_json(joueurs, joueurs_path)
        st.success(f"{joueur_a_supprimer} supprimé.")

    st.subheader("📦 Decks")
    nouveau_deck = st.text_input("Ajouter un deck")
    if st.button("Ajouter deck"):
        if nouveau_deck and nouveau_deck not in decks:
            decks.append(nouveau_deck)
            sauvegarder_json(decks, decks_path)
            st.success(f"{nouveau_deck} ajouté.")

    deck_a_supprimer = st.selectbox("Supprimer un deck :", decks) if decks else None
    if st.button("Supprimer deck") and deck_a_supprimer:
        decks.remove(deck_a_supprimer)
        sauvegarder_json(decks, decks_path)
        st.success(f"{deck_a_supprimer} supprimé.")
"""

# Écriture du fichier
streamlit_file = Path("/mnt/data/streamlit_app.py")

streamlit_file.name  # Afficher le nom du fichier généré pour téléchargement ou exécution
