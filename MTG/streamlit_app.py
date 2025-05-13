import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# Configuration Google Sheets
SHEET_NAME = "mtg-assassin-data"
GOOGLE_CREDENTIALS_FILE = "google_service_account.json"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Accès aux onglets
sheet_joueurs = client.open(SHEET_NAME).worksheet("Joueurs")
sheet_decks = client.open(SHEET_NAME).worksheet("Decks")
sheet_scores = client.open(SHEET_NAME).worksheet("ScoreFinal")
sheet_historique = client.open(SHEET_NAME).worksheet("Historique")

def get_col_values(sheet):
    return [cell.strip() for cell in sheet.col_values(1) if cell.strip()]

def get_joueurs():
    return get_col_values(sheet_joueurs)

def get_decks():
    return get_col_values(sheet_decks)

def get_score_total():
    data = sheet_scores.get_all_records()
    return {row['Joueur']: {"total_points": int(row['Total Points']), "games_played": int(row['Games Played'])} for row in data}

def update_score_total(scores):
    current = get_score_total()
    for joueur, points in scores.items():
        if joueur in current:
            current[joueur]['total_points'] += points
            current[joueur]['games_played'] += 1
        else:
            current[joueur] = {"total_points": points, "games_played": 1}
    sheet_scores.clear()
    sheet_scores.append_row(["Joueur", "Total Points", "Games Played"])
    for joueur, data in current.items():
        sheet_scores.append_row([joueur, data['total_points'], data['games_played']])

def enregistrer_historique(date, joueurs, decks, kills, bonus, placements, scores):
    sheet_historique.append_row([
        date,
        json.dumps(joueurs),
        json.dumps(decks),
        json.dumps(kills),
        json.dumps(bonus),
        json.dumps(placements),
        json.dumps(scores)
    ])

# Interface Streamlit
st.set_page_config(page_title="Assassin MTG", layout="centered")
st.sidebar.title("Menu")
page = st.sidebar.radio("Navigation", ["🎮 Nouvelle Partie", "📊 Classement global"])

if page == "🎮 Nouvelle Partie":
    st.title("🎮 Nouvelle Partie - Assassin MTG")
    joueurs = get_joueurs()
    decks = get_decks()

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
            scores = {joueur: 0 for joueur in st.session_state["decks"]}
            bonus = {joueur: 0 for joueur in st.session_state["decks"]}

            vivants = list(st.session_state["decks"].keys())
            for tueur, victime, cible in kills:
                if tueur not in vivants or victime not in vivants:
                    continue
                if cible == tueur:
                    scores[tueur] += 2
                    bonus[tueur] += 2
                elif cible == victime:
                    scores[tueur] += 4
                    bonus[tueur] += 4
                else:
                    scores[tueur] += 1
                    bonus[tueur] += 1
                vivants.remove(victime)

            for i, joueur in enumerate(morts):
                scores[joueur] += i + 1
                bonus[joueur] += i + 1

            score_total = get_score_total()
            leader = max(score_total.items(), key=lambda x: x[1]['total_points'])[0] if score_total else None
            if leader:
                for tueur, victime, _ in kills:
                    if victime == leader:
                        scores[tueur] += 1
                        bonus[tueur] += 1

            update_score_total(scores)

            st.write("## Scores finaux")
            for joueur, score in scores.items():
                st.write(f"**{joueur}** ({st.session_state['decks'][joueur]}) : {score} points")

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            enregistrer_historique(
                date,
                joueurs_choisis,
                st.session_state["decks"],
                kills,
                bonus,
                morts,
                scores
            )

            st.success("✅ Partie enregistrée avec succès dans l'historique.")
            st.session_state.clear()

elif page == "📊 Classement global":
    st.title("📊 Classement général")
    scores = get_score_total()

    if not scores:
        st.info("Aucun score enregistré pour l'instant.")
    else:
        classement = sorted(scores.items(), key=lambda x: x[1]['total_points'], reverse=True)
        for joueur, data in classement:
            st.write(f"**{joueur}** — {data['total_points']} pts en {data['games_played']} parties")
