import streamlit as st
import pandas as pd
from datetime import datetime
import openai

st.set_page_config(page_title="RestoRH Ultimate", layout="wide")

# HEADER
st.markdown("""
<div style='text-align: center'>
    <h1 style='color:#2E86C1;'>👨‍🍳 <b>RestoRH Ultimate</b></h1>
    <p style='font-size:18px;'>Le copilote RH intelligent pour restaurateurs exigeants</p>
</div>
""", unsafe_allow_html=True)
st.divider()

menu = st.sidebar.radio("🧭 Menu", [
    "👥 Employés",
    "📅 Planning",
    "⏱️ Pointage",
    "📊 Tableau de bord",
    "📆 Congés",
    "🎯 Évaluations",
    "🧠 Assistant RH (ChatGPT)"
])

if "employees" not in st.session_state:
    st.session_state.employees = []

if "pointages" not in st.session_state:
    st.session_state.pointages = []

if "conges" not in st.session_state:
    st.session_state.conges = []

if "evaluations" not in st.session_state:
    st.session_state.evaluations = []

# Employés
if menu == "👥 Employés":
    st.subheader("Ajouter un employé")
    with st.form("add_employee"):
        nom = st.text_input("Nom complet")
        role = st.selectbox("Poste", ["Serveur", "Cuisinier", "Plonge", "Manager"])
        contrat = st.selectbox("Type de contrat", ["CDI", "CDD", "Extra"])
        dispo = st.text_input("Disponibilités (ex: Lun-Ven)")
        submit = st.form_submit_button("Ajouter")
        if submit:
            st.session_state.employees.append({
                "Nom": nom, "Rôle": role, "Contrat": contrat, "Dispo": dispo
            })
            st.success(f"{nom} ajouté ✅")
    st.divider()
    st.subheader("Liste des employés")
    if st.session_state.employees:
        st.dataframe(pd.DataFrame(st.session_state.employees), use_container_width=True)
    else:
        st.info("Aucun employé ajouté.")

# Planning
elif menu == "📅 Planning":
    st.subheader("Planning Hebdomadaire")
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    planning = {}
    for emp in st.session_state.employees:
        emp_name = emp["Nom"]
        planning[emp_name] = {}
        cols = st.columns(len(jours))
        st.markdown(f"**{emp_name}**")
        for i, jour in enumerate(jours):
            shift = cols[i].selectbox(f"{jour}", ["Repos", "Matin", "Soir", "Journée"], key=f"{emp_name}_{jour}")
            planning[emp_name][jour] = shift
    if st.button("💾 Sauvegarder le planning"):
        st.session_state.planning = planning
        st.success("Planning sauvegardé.")

# Pointage
elif menu == "⏱️ Pointage":
    st.subheader("Pointage des employés")
    if not st.session_state.employees:
        st.warning("Ajoutez d'abord des employés.")
    else:
        employe = st.selectbox("Employé", [e["Nom"] for e in st.session_state.employees])
        action = st.radio("Action", ["Entrée", "Sortie"])
        if st.button("📍 Enregistrer le pointage"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.pointages.append({
                "Employé": employe, "Action": action, "Heure": now
            })
            st.success(f"{action} enregistrée pour {employe} à {now}.")
    st.divider()
    st.subheader("Historique des pointages")
    if st.session_state.pointages:
        st.dataframe(pd.DataFrame(st.session_state.pointages), use_container_width=True)
    else:
        st.info("Aucun pointage enregistré.")

# Tableau de bord
elif menu == "📊 Tableau de bord":
    st.subheader("Statistiques RH")
    col1, col2 = st.columns(2)
    col1.metric("👥 Employés", len(st.session_state.employees))
    col2.metric("📍 Pointages", len(st.session_state.pointages))
    st.divider()
    if st.session_state.pointages:
        df = pd.DataFrame(st.session_state.pointages)
        st.download_button("⬇️ Exporter les pointages (.csv)", df.to_csv(index=False), "pointages.csv", "text/csv")

# Congés
elif menu == "📆 Congés":
    st.subheader("Demandes de congés")
    employe = st.selectbox("Employé concerné", [e["Nom"] for e in st.session_state.employees])
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")
    if st.button("📩 Demander un congé"):
        st.session_state.conges.append({
            "Employé": employe,
            "Du": date_debut.strftime("%Y-%m-%d"),
            "Au": date_fin.strftime("%Y-%m-%d")
        })
        st.success("Demande enregistrée ✅")
    st.divider()
    st.subheader("Historique des congés")
    if st.session_state.conges:
        st.dataframe(pd.DataFrame(st.session_state.conges), use_container_width=True)
    else:
        st.info("Aucune demande enregistrée.")

# Évaluations
elif menu == "🎯 Évaluations":
    st.subheader("Évaluation des employés")
    employe = st.selectbox("👤 Choisir un employé", [e["Nom"] for e in st.session_state.employees])
    note = st.slider("Note générale", 1, 10, 5)
    commentaire = st.text_area("Commentaires")
    if st.button("✅ Enregistrer l’évaluation"):
        st.session_state.evaluations.append({
            "Employé": employe,
            "Note": note,
            "Commentaire": commentaire,
            "Date": datetime.now().strftime("%Y-%m-%d")
        })
        st.success("Évaluation enregistrée")
    st.divider()
    st.subheader("Historique des évaluations")
    if st.session_state.evaluations:
        st.dataframe(pd.DataFrame(st.session_state.evaluations), use_container_width=True)
    else:
        st.info("Aucune évaluation disponible.")

# ChatGPT
elif menu == "🧠 Assistant RH (ChatGPT)":
    st.subheader("🤖 Assistant RH intelligent")
    st.markdown("Pose une question liée à ton équipe, ton planning ou tes RH 👇")

    openai.api_key = st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else None

    user_input = st.text_area("💬 Ta question :")
    if st.button("Envoyer à ChatGPT"):
        if not openai.api_key:
            st.warning("Clé API OpenAI non configurée. Va dans Streamlit Secrets.")
        elif user_input.strip() == "":
            st.warning("Pose une vraie question 😉")
        else:
            with st.spinner("Réponse de l'assistant..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un assistant RH spécialisé pour les restaurants."},
                        {"role": "user", "content": user_input}
                    ]
                )
                st.success(response['choices'][0]['message']['content'])
