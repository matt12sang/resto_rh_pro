import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="RestoRH Pro", layout="wide")

# HEADER DESIGN
st.markdown("""
<div style='text-align: center'>
    <h1 style='color:#2E86C1;'>🍽️ <b>RestoRH Pro</b></h1>
    <p style='font-size:18px;'>La plateforme RH intelligente pour les restaurateurs</p>
</div>
""", unsafe_allow_html=True)

st.divider()

menu = st.sidebar.radio("📋 Menu", ["👥 Fiches employés", "📅 Planning du personnel", "⏱️ Pointage", "📊 Tableau de bord RH"])

if "employees" not in st.session_state:
    st.session_state.employees = []

if "pointages" not in st.session_state:
    st.session_state.pointages = []

if menu == "👥 Fiches employés":
    st.subheader("👤 Ajouter un employé")
    with st.form("add_employee"):
        nom = st.text_input("Nom")
        role = st.selectbox("Rôle", ["Serveur", "Cuisinier", "Plonge", "Manager"])
        contrat = st.selectbox("Type de contrat", ["CDI", "CDD", "Extra"])
        submit = st.form_submit_button("Ajouter")
        if submit:
            st.session_state.employees.append({"Nom": nom, "Rôle": role, "Contrat": contrat})
            st.success(f"{nom} a été ajouté avec succès ✅")

    st.divider()
    st.subheader("📋 Liste des employés")
    if st.session_state.employees:
        st.dataframe(pd.DataFrame(st.session_state.employees), use_container_width=True)
    else:
        st.info("Aucun employé pour l’instant.")

elif menu == "📅 Planning du personnel":
    st.subheader("🗓️ Planning hebdomadaire")
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
        st.success("✅ Planning sauvegardé.")

elif menu == "⏱️ Pointage":
    st.subheader("🔔 Pointage des employés")
    if not st.session_state.employees:
        st.warning("Ajoutez d'abord des employés.")
    else:
        employe = st.selectbox("👤 Employé", [e["Nom"] for e in st.session_state.employees])
        action = st.radio("Action", ["Entrée", "Sortie"])
        if st.button("📍 Enregistrer"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.pointages.append({"Employé": employe, "Action": action, "Heure": now})
            st.success(f"{action} enregistrée pour {employe} à {now}.")

    st.divider()
    st.subheader("🕓 Historique des pointages")
    if st.session_state.pointages:
        st.dataframe(pd.DataFrame(st.session_state.pointages), use_container_width=True)
    else:
        st.info("Aucun pointage enregistré.")

elif menu == "📊 Tableau de bord RH":
    st.subheader("📈 Statistiques générales")
    col1, col2 = st.columns(2)
    col1.metric("👥 Nombre d’employés", len(st.session_state.employees))
    col2.metric("⏱️ Total de pointages", len(st.session_state.pointages))

    st.divider()
    st.subheader("🧾 Détail des pointages")
    if st.session_state.pointages:
        df = pd.DataFrame(st.session_state.pointages)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Télécharger les données RH (.csv)", csv, "pointages_export.csv", "text/csv")
    else:
        st.info("Aucune donnée à exporter.")
