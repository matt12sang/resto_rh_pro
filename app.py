import streamlit as st
import pandas as pd
from datetime import datetime
import openai

# Auth simulation
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "manager": {"password": "manager123", "role": "manager"},
    "employe": {"password": "employe123", "role": "employe"}
}

st.set_page_config(page_title="RestoRH 🇨🇭", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    st.title("🔐 Connexion sécurisée")
    user = st.text_input("Nom d'utilisateur")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if user in USERS and USERS[user]["password"] == pwd:
            st.session_state.logged_in = True
            st.session_state.role = USERS[user]["role"]
            st.success(f"Bienvenue {user} 👋 (rôle : {st.session_state.role})")
            st.rerun()
        else:
            st.error("Identifiants incorrects.")
    st.stop()

# Menu dynamique
menu_options = ["📊 Tableau de bord", "👥 Employés", "📅 Planning", "📆 Congés", "⏱️ Pointage", "📘 CCNT Suisse", "🧠 Assistant IA"]
if st.session_state.role == "admin":
    menu_options += ["📄 Rapport PDF (bientôt)", "📣 Notifications (mock)"]

menu = st.sidebar.selectbox("🧭 Menu", menu_options)

# DATA STATES SIMULÉES
if "employees" not in st.session_state:
    st.session_state.employees = []
if "pointages" not in st.session_state:
    st.session_state.pointages = []
if "conges" not in st.session_state:
    st.session_state.conges = []

# MODULE CCNT
if menu == "📘 CCNT Suisse":
    st.title("📘 Convention Collective Nationale de Travail (CCNT) - Hôtellerie et Restauration")
    st.markdown("""
    **Extraits utiles pour les restaurateurs :**

    - 🕒 Temps de travail max : 50h / semaine  
    - ⏸️ Temps de pause : 15 min si +5h, 30 min si +7h  
    - 💰 Salaire minimum : dépend du poste et de l'âge  
    - 📅 Congés : minimum 4 semaines/an  
    - 📝 Heures supp. payées à 125% ou compensées en temps

    **⚠️ Ces règles doivent être respectées dans les plannings.**
    """)
    st.info("À venir : vérification automatique de la conformité des plannings avec la CCNT.")

# MODULE TABLEAU DE BORD
elif menu == "📊 Tableau de bord":
    st.title("📊 Indicateurs RH")
    col1, col2 = st.columns(2)
    col1.metric("👥 Employés", len(st.session_state.employees))
    col2.metric("📍 Pointages", len(st.session_state.pointages))
    st.write("📆 Congés enregistrés :", len(st.session_state.conges))

# MODULE EMPLOYÉS
elif menu == "👥 Employés":
    st.title("👥 Gestion des employés")
    with st.form("add_emp"):
        nom = st.text_input("Nom")
        poste = st.selectbox("Poste", ["Serveur", "Cuisinier", "Plonge", "Manager"])
        salaire = st.number_input("Salaire brut", step=100)
        submit = st.form_submit_button("Ajouter")
        if submit:
            st.session_state.employees.append({"Nom": nom, "Poste": poste, "Salaire": salaire})
            st.success("Employé ajouté.")
    if st.session_state.employees:
        st.dataframe(pd.DataFrame(st.session_state.employees))

# MODULE PLANNING (placeholder)
elif menu == "📅 Planning":
    st.title("📅 Planning - à venir")
    st.info("Le planning intelligent conforme à la CCNT arrive très bientôt.")

# MODULE CONGÉS
elif menu == "📆 Congés":
    st.title("📆 Demandes de congés")
    employe = st.selectbox("Employé", [e["Nom"] for e in st.session_state.employees])
    date = st.date_input("Date souhaitée")
    if st.button("Demander congé"):
        st.session_state.conges.append({"Employé": employe, "Date": date.strftime("%Y-%m-%d")})
        st.success("Demande enregistrée.")

# MODULE POINTAGE
elif menu == "⏱️ Pointage":
    st.title("⏱️ Pointage")
    employe = st.selectbox("Employé à pointer", [e["Nom"] for e in st.session_state.employees])
    action = st.radio("Action", ["Entrée", "Sortie"])
    if st.button("Enregistrer"):
        st.session_state.pointages.append({
            "Employé": employe,
            "Action": action,
            "Heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success("Pointage enregistré.")

# MODULE CHATGPT
elif menu == "🧠 Assistant IA":
    st.title("🤖 Assistant RH IA")
    openai.api_key = st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else None
    question = st.text_area("Pose ta question RH ou CCNT")
    if st.button("Interroger ChatGPT"):
        if not openai.api_key:
            st.warning("Clé API manquante.")
        elif question.strip() != "":
            with st.spinner("Réponse en cours..."):
                rep = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un assistant RH spécialisé en restauration en Suisse avec connaissance de la CCNT."},
                        {"role": "user", "content": question}
                    ]
                )
                st.success(rep.choices[0].message.content)

# MODULES FUTURS
elif menu == "📄 Rapport PDF (bientôt)":
    st.title("📄 Génération de rapport RH PDF")
    st.info("Fonctionnalité en cours de développement.")

elif menu == "📣 Notifications (mock)":
    st.title("📣 Notifications automatiques")
    st.info("Notifications par email / Slack seront bientôt activables depuis cette interface.")
