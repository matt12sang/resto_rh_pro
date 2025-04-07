import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="RestoRH Pro", layout="wide")

st.title("RestoRH Pro - Gestion RH pour Restaurateurs")

menu = st.sidebar.radio("Menu", ["Fiches employés", "Planning du personnel", "Pointage", "Tableau de bord RH"])

if "employees" not in st.session_state:
    st.session_state.employees = []

if "pointages" not in st.session_state:
    st.session_state.pointages = []

if menu == "Fiches employés":
    st.subheader("Ajouter un employé")
    with st.form("add_employee"):
        nom = st.text_input("Nom")
        role = st.selectbox("Rôle", ["Serveur", "Cuisinier", "Plonge", "Manager"])
        contrat = st.selectbox("Type de contrat", ["CDI", "CDD", "Extra"])
        submit = st.form_submit_button("Ajouter")
        if submit:
            st.session_state.employees.append({"Nom": nom, "Rôle": role, "Contrat": contrat})
            st.success(f"{nom} ajouté avec succès.")

    st.subheader("Liste des employés")
    st.write(pd.DataFrame(st.session_state.employees))

elif menu == "Planning du personnel":
    st.subheader("Planning (semaine)")
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    planning = {}
    for emp in st.session_state.employees:
        emp_name = emp["Nom"]
        planning[emp_name] = {}
        for jour in jours:
            shift = st.selectbox(f"{emp_name} - {jour}", ["Repos", "Matin", "Soir", "Journée"], key=f"{emp_name}_{jour}")
            planning[emp_name][jour] = shift
    if st.button("Sauvegarder le planning"):
        st.session_state.planning = planning
        st.success("Planning sauvegardé.")

elif menu == "Pointage":
    st.subheader("Pointage des employés")
    employe = st.selectbox("Employé", [e["Nom"] for e in st.session_state.employees])
    action = st.radio("Action", ["Entrée", "Sortie"])
    if st.button("Enregistrer"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.pointages.append({"Employé": employe, "Action": action, "Heure": now})
        st.success(f"{action} enregistrée pour {employe} à {now}.")

    st.subheader("Historique des pointages")
    st.write(pd.DataFrame(st.session_state.pointages))

elif menu == "Tableau de bord RH":
    st.subheader("Tableau de bord")
    st.metric("Total employés", len(st.session_state.employees))
    total_pointages = len(st.session_state.pointages)
    st.metric("Total de pointages", total_pointages)

    if total_pointages > 0:
        st.subheader("Détail des pointages")
        st.write(pd.DataFrame(st.session_state.pointages))

    if st.button("Exporter les données RH"):
        df = pd.DataFrame(st.session_state.pointages)
        df.to_csv("pointages_export.csv", index=False)
        st.success("Export réalisé. Fichier : pointages_export.csv")
