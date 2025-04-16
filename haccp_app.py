# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 09:35:02 2025

@author: sibya
"""

import streamlit as st
import datetime
import pandas as pd

# --- Configuration ---
st.set_page_config(page_title="Edonia HACCP", page_icon="🧊", layout="wide")

with open("custom_head.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)



# --- Style ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#local_css("style.css")  # Assurez-vous d'avoir un fichier style.css pour personnaliser l'apparence

# --- Data Storage ---
#  Pour simplifier, nous utiliserons des fichiers CSV.
#  Pour une application plus robuste, une base de données est recommandée.
def save_data(module, data):
    filename = f"data/{module}.csv"  # Create a 'data' folder
    try:
        existing_data = pd.read_csv(filename)
        updated_data = pd.concat([existing_data, pd.DataFrame([data])], ignore_index=True)
    except FileNotFoundError:
        updated_data = pd.DataFrame([data])
    updated_data.to_csv(filename, index=False)

def load_data(module):
    filename = f"data/{module}.csv"
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame()

# --- Modules ---

def controle_reception():
    st.header("Contrôles à Réception")
    with st.form(key='controle_reception_form'):
        col1, col2 = st.columns(2)
        date_controle = col1.date_input("Date du contrôle", datetime.date.today())
        qui = col1.text_input("Contrôle effectué par")
        nom_transporteur = col2.text_input("Nom du Transporteur")
        livraison_annoncee = col2.radio("Livraison annoncée", ["Oui", "Non"])
        numero_bl = col1.text_input("N° BL")
        nom_fournisseur = col1.text_input("Nom du Fournisseur")
        produit_controle = col2.text_input("Produit contrôlé")
        numero_lot_fournisseur = col2.text_input("N° Lot Fournisseur")
        dlc_fournisseur = col1.date_input("DLC Fournisseur")
        quantite_receptionnee = col1.number_input("Quantité réceptionnée")
        numero_lot_edonia = col2.text_input("N° Lot Edonia")

        col3, col4 = st.columns(2)
        t_transport = col3.number_input("T°C Transport")
        conformite_t_transport = col3.radio("Conformité T°C Transport", ["Oui", "Non"])
        t_produit = col4.number_input("T°C Produit")
        conformite_t_produit = col4.radio("Conformité T°C Produit", ["Oui", "Non"])

        conformite_emballage = st.radio("Conformité Emballage", ["Oui", "Non"])
        conformite_etiquetage = st.radio("Conformité Étiquetage", ["Oui", "Non"], index=0)

        action_corrective = st.text_area("Action corrective")

        submit_button = st.form_submit_button(label='Enregistrer le contrôle')

    if submit_button:
        data = {
            "Date": date_controle, "Qui": qui, "Transporteur": nom_transporteur,
            "Livraison Annoncée": livraison_annoncee, "N° BL": numero_bl,
            "Fournisseur": nom_fournisseur, "Produit": produit_controle,
            "N° Lot Fournisseur": numero_lot_fournisseur, "DLC Fournisseur": dlc_fournisseur,
            "Quantité Réceptionnée": quantite_receptionnee, "N° Lot Edonia": numero_lot_edonia,
            "T°C Transport": t_transport, "Conformité T°C Transport": conformite_t_transport,
            "T°C Produit": t_produit, "Conformité T°C Produit": conformite_t_produit,
            "Conformité Emballage": conformite_emballage, "Conformité Étiquetage": conformite_etiquetage,
            "Action Corrective": action_corrective
        }
        save_data("reception", data)
        st.success("Contrôle enregistré avec succès!")
    
    # Display previous data
    if st.checkbox("Afficher les contrôles précédents"):
        previous_data = load_data("reception")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucun contrôle précédent enregistré.")

def controle_expedition():
    st.header("Contrôles à Expédition")
    # ... (Similaire à controle_reception, adaptez les champs)
    with st.form(key='controle_expedition_form'):
        col1, col2 = st.columns(2)
        date_controle = col1.date_input("Date", datetime.date.today())
        qui = col1.text_input("Qui")
        nom_transporteur = col2.text_input("Nom du Transporteur")
        expedition_annoncee = col2.radio("Expédition annoncée", ["Oui", "Non"])
        numero_bl = col1.text_input("N° BL")
        produit_controle = col1.text_input("Produit contrôlé")
        numero_lot_edonia = col2.text_input("N° Lot Edonia")
        dlc_edonia = col1.date_input("DLC Edonia")
        quantite_expediee = col1.number_input("Quantité expédiée")

        conformite_t_transport = col2.radio("Conformité T°C Transport", ["Oui", "Non"])
        conformite_t_produit = col1.radio("Conformité T°C Produit", ["Oui", "Non"])
        conformite_emballage = col2.radio("Conformité Emballage", ["Oui", "Non"])
        action_corrective = st.text_area("Action corrective")

        submit_button = st.form_submit_button(label='Enregistrer')

    if submit_button:
        data = {
            "Date": date_controle, "Qui": qui, "Nom du Transporteur": nom_transporteur,
            "Expédition annoncée": expedition_annoncee, "N° BL": numero_bl,
            "Produit contrôlé": produit_controle, "N° Lot Edonia": numero_lot_edonia,
            "DLC Edonia": dlc_edonia, "Quantité expédiée": quantite_expediee,
            "Conformité T°C Transport": conformite_t_transport,
            "Conformité T°C Produit": conformite_t_produit,
            "Conformité Emballage": conformite_emballage,
            "Action corrective": action_corrective
        }
        save_data("expedition", data)
        st.success("Contrôle enregistré avec succès!")
    
    # Display previous data
    if st.checkbox("Afficher les contrôles précédents"):
        previous_data = load_data("expedition")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucun contrôle précédent enregistré.")

def controle_temperature_chambres():
    st.header("Contrôle Température Chambres Froides")
    # ... (Tableau complexe, utilise st.dataframe pour l'affichage/édition si nécessaire)
    with st.form(key='controle_temperature_form'):
        date = st.date_input("Date", datetime.date.today())
        equipe = st.text_input("Équipe")
        qui = st.text_input("Qui")
        heure = st.time_input("Heure")

        chp1_temperature = st.number_input("CHP 1 Température (+4°C)", value=4.0, format="%.1f")
        stock_mp_temperature = st.number_input("Stock MP Température (+4°C)", value=4.0, format="%.1f")
        emballage_temperature = st.number_input("Emballage Température (+4°C)", value=4.0, format="%.1f")
        chn_temperature = st.number_input("CHN Température (-20°C)", value=-20.0, format="%.1f")

        action_corrective = st.text_area("Action corrective")

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date": date,
            "Equipe": equipe,
            "Qui": qui,
            "Heure": heure,
            "CHP 1 (+4°C)": chp1_temperature,
            "Stock MP (+4°C)": stock_mp_temperature,
            "Emballage (+4°C)": emballage_temperature,
            "CHN (-20°C)": chn_temperature,
            "Action corrective": action_corrective
        }
        save_data("temperature_chambres", data)
        st.success("Contrôle enregistré !")

    # Display previous data
    if st.checkbox("Afficher les contrôles précédents"):
        previous_data = load_data("temperature_chambres")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucun contrôle précédent enregistré.")

def fiche_non_conformite_materiel():
    st.header("Fiche de Non-Conformité Matériel")
    # ...
    with st.form(key='non_conformite_materiel_form'):
        date = st.date_input("Date", datetime.date.today())
        qui = st.text_input("Qui")
        secteur = st.text_input("Secteur")
        anomalie = st.text_area("Anomalie(s) constatées")
        action_corrective = st.text_area("Action(s) corrective(s)")
        intervention_date = st.date_input("Intervention réalisée le", datetime.date.today())
        intervention_par = st.text_input("Intervention réalisée par")
        responsable_nom_visa = st.text_input("Nom et visa du responsable de Service")

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date": date,
            "Qui": qui,
            "Secteur": secteur,
            "Anomalie(s) constatées": anomalie,
            "Action(s) corrective(s)": action_corrective,
            "Intervention réalisée le": intervention_date,
            "Intervention réalisée par": intervention_par,
            "Nom et visa du responsable de Service": responsable_nom_visa
        }
        save_data("non_conformite_materiel", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("non_conformite_materiel")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

def traceabilite_interne():
    st.header("Traçabilité Interne")
    # ...
    with st.form(key='traceabilite_interne_form'):
        produit_fabrique = st.text_input("Dénomination du produit fabriqué")
        date_fabrication = st.date_input("Date de fabrication", datetime.date.today())
        numero_lot = st.text_input("Numéro de lot du produit fabriqué")

        matieres_premieres = []
        num_matieres_premieres = st.number_input("Nombre de matières premières", min_value=1, value=1, step=1)

        for i in range(num_matieres_premieres):
            st.subheader(f"Matière Première {i + 1}")
            denomination = st.text_input(f"Dénomination matière {i + 1}")
            identification = st.text_input(f"Identification matière {i + 1} (N° de lot Edonia)")
            dlc_ddm = st.date_input(f"DLC ou DDM matière {i + 1}")
            quantite = st.number_input(f"Quantité utilisée matière {i + 1}", value=0.0)
            action_mp = st.text_area(f"Action corrective matière {i + 1}")

            matieres_premieres.append({
                "Dénomination": denomination,
                "Identification": identification,
                "DLC ou DDM": dlc_ddm,
                "Quantité utilisée": quantite,
                "Action corrective": action_mp
            })

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Dénomination du produit fabriqué": produit_fabrique,
            "Date de fabrication": date_fabrication,
            "Numéro de lot du produit fabriqué": numero_lot,
            "Matières premières": matieres_premieres
        }
        save_data("traceabilite_interne", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("traceabilite_interne")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

def qualite_huile_cuisson():
    st.header("Qualité de l'Huile de Cuisson")
    # ...
    with st.form(key='qualite_huile_cuisson_form'):
        date = st.date_input("Date", datetime.date.today())
        qui = st.text_input("Qui")
        numero_cuisson = st.number_input("N° cuisson", min_value=1, value=1, step=1)
        conformite = st.radio("Conformité", ["Conforme", "A surveiller", "A changer"])
        date_changement_huile = st.date_input("Date changement de l'huile")
        changement_huile_par = st.text_input("Changement de l'huile réalisé par")

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date": date,
            "Qui": qui,
            "N° cuisson": numero_cuisson,
            "Conformité": conformite,
            "Date changement de l'huile": date_changement_huile,
            "Changement de l'huile réalisé par": changement_huile_par
        }
        save_data("qualite_huile", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("qualite_huile")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

def controle_etat_machine():
    st.header("Contrôle État Machine et Matériel au Démarrage")
    # ...
    with st.form(key='controle_etat_machine_form'):
        date_controle = st.date_input("Date de contrôle", datetime.date.today())
        heure_controle = st.time_input("Heure de contrôle")
        realise_par = st.text_input("Réalisé par")

        materiels = ["Mélangeur", "Marmite de cuisson", "Système d'égouttage et lessivage",
                     "Système de filtration", "Centrifugeuse", "Cellule de surgélation",
                     "Thermoscelleuse et balance", "Petit Matériel"]

        controle_materiels = []
        for materiel in materiels:
            st.subheader(f"Contrôle {materiel}")
            piece_manquante = st.radio("Pièce manquante ou abîmée", ["Conforme", "Non conforme"], key=f"{materiel}_piece")
            presence_graisse = st.radio("Présence de graisse au contact du produit", ["Conforme", "Non conforme"], key=f"{materiel}_graisse")
            proprete_visuelle = st.radio("Propreté visuelle", ["Conforme", "Non conforme"], key=f"{materiel}_proprete")
            action_corrective = st.text_area("Action corrective", key=f"{materiel}_action")

            controle_materiels.append({
                "Matériel": materiel,
                "Pièce manquante ou abîmée": piece_manquante,
                "Présence de graisse": presence_graisse,
                "Propreté visuelle": proprete_visuelle, "Action corrective": action_corrective
            })

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date de contrôle": date_controle,
            "Heure de contrôle": heure_controle,
            "Réalisé par": realise_par,
            "Contrôle des matériels": controle_materiels
        }
        save_data("controle_etat_machine", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("controle_etat_machine")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

def controle_balance():
    st.header("Contrôle Balance Conditionnement Produit Fini")
    # ...
    with st.form(key='controle_balance_form'):
        date = st.date_input("Date", datetime.date.today())
        equipe = st.text_input("Équipe")
        qui = st.text_input("Qui")
        heure = st.time_input("Heure")
        poids_etalon = st.number_input("Poids Étalon (1kg)", value=1.0, format="%.3f")
        conformite_balance = st.radio("Conformité balance", ["Conforme", "Non conforme"])
        action_corrective = st.text_area("Action corrective")

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date": date,
            "Equipe": equipe,
            "Qui": qui,
            "Heure": heure,
            "Poids Étalon (1kg)": poids_etalon,
            "Conformité balance": conformite_balance,
            "Action corrective": action_corrective
        }
        save_data("controle_balance", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("controle_balance")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

def suivi_fabrication():
    st.header("Suivi de la Fabrication")
    # This is a complex form, consider breaking it down into smaller sections
    with st.form(key='suivi_fabrication_form'):
        date_enregistrement = st.date_input("Date de l'enregistrement", datetime.date.today())
        heure_debut_enregistrement = st.time_input("Heure de début de l'enregistrement")
        heure_fin_enregistrement = st.time_input("Heure de fin de l'enregistrement")
        realise_par = st.text_input("Réalisé par")

        # Mélange
        st.subheader("Mélange")
        melanges = []
        num_melanges = st.number_input("Nombre de mélanges", min_value=1, value=1, step=1)
        for i in range(num_melanges):
            st.write(f"Mélange {i + 1}")
            no_melange = st.number_input(f"N° du mélange {i + 1}", min_value=1, value=1, step=1)
            quantite = st.number_input(f"Quantité (kg) mélange {i + 1}", value=0.0)
            t_debut = st.number_input(f"T°C début mélange {i + 1}", value=0.0)
            t_fin = st.number_input(f"T°C fin mélange {i + 1}", value=0.0)
            controle_ph = st.number_input(f"Contrôle pH (cible 6.3 ± 0.2) mélange {i + 1}", value=6.3)
            remarques_melange = st.text_area(f"Remarques mélange {i + 1}")
            melanges.append({
                "N° mélange": no_melange, "Quantité (kg)": quantite,
                "T°C début": t_debut, "T°C fin": t_fin,
                "Contrôle pH": controle_ph, "Remarques": remarques_melange
            })

        # Stockage en chambre froide réfrigérée
        st.subheader("Stockage en chambre froide réfrigérée")
        heure_entree_1er_melange = st.time_input("Heure entrée du 1er mélange")
        t_chambre_entree = st.number_input("T°C chambre (entrée)", value=0.0)
        heure_sortie_dernier_melange = st.time_input("Heure sortie du dernier mélange")
        t_chambre_sortie = st.number_input("T°C chambre (sortie)", value=0.0)
        remarques_stockage = st.text_area("Remarques stockage chambre froide")

        # Suivi des cuissons
        st.subheader("Suivi des cuissons")
        cuissons = []
        num_cuissons = st.number_input("Nombre de cuissons", min_value=1, value=1, step=1)
        for i in range(num_cuissons):
            st.write(f"Cuisson {i + 1}")
            no_cuisson = st.number_input(f"N° cuisson {i + 1}", min_value=1, value=1, step=1)
            t_huile_avant = st.number_input(f"T°C huile avant cuisson {i + 1}", value=0.0)
            heure_debut_cuisson = st.time_input(f"Heure de début de cuisson {i + 1}")
            t_double_enveloppe = st.number_input(f"T°C double enveloppe (consigne 160°C) cuisson {i + 1}", value=160.0)
            heure_sortie_cuisson = st.time_input(f"Heure de sortie de cuisson {i + 1}")
            t_produit_cuisson = st.number_input(f"T°C produit cuisson {i + 1}", value=0.0)
            cuissons.append({
                "N° cuisson": no_cuisson, "T°C huile avant": t_huile_avant,
                "Heure début cuisson": heure_debut_cuisson,
                "T°C double enveloppe": t_double_enveloppe,
                "Heure sortie cuisson": heure_sortie_cuisson, "T°C produit": t_produit_cuisson
            })

        # Suivi de l'égouttage et du lessivage
        st.subheader("Suivi de l'égouttage et du lessivage")
        egouttages = []
        num_egouttages = st.number_input("Nombre d'égouttages", min_value=1, value=1, step=1)
        for i in range(num_egouttages):
            st.write(f"Égouttage {i + 1}")
            no_cuisson_egouttage = st.number_input(f"N° cuisson égouttage {i + 1}", min_value=1, value=1, step=1)
            poids_sortie_egouttage = st.number_input(f"Poids sortie égouttage {i + 1}", value=0.0)
            t_eau_lessivage = st.number_input(f"T°C eau de lessivage {i + 1}", value=0.0)
            duree_lessivage = st.number_input(f"Durée lessivage {i + 1}", value=0.0)
            poids_sortie_lessivage = st.number_input(f"Poids sortie lessivage {i + 1}", value=0.0)
            t_produit_lessivage = st.number_input(f"T° produit sortie de lessivage {i + 1}", value=0.0)
            egouttages.append({
                "N° cuisson": no_cuisson_egouttage,
                "Poids sortie égouttage": poids_sortie_egouttage,
                "T°C eau lessivage": t_eau_lessivage,
                "Durée lessivage": duree_lessivage,
                "Poids sortie lessivage": poids_sortie_lessivage,
                "T° produit sortie lessivage": t_produit_lessivage
            })

        # Suivi de la centrifugation
        st.subheader("Suivi de la centrifugation")
        centrifugations = []
        num_centrifugations = st.number_input("Nombre de centrifugations", min_value=1, value=1, step=1)
        for i in range(num_centrifugations):
            st.write(f"Centrifugation {i + 1}")
            no_cuisson_centrifugation = st.number_input(f"N° cuisson centrifugation {i + 1}", min_value=1, value=1, step=1)
            poids_sortie_lessivage_centrifugation = st.number_input(f"Poids sortie lessivage centrifugation {i + 1}", value=0.0)
            vitesse_centrifugation = st.number_input(f"Vitesse centrifugation {i + 1}", value=0.0)
            duree_centrifugation = st.number_input(f"Durée centrifugation {i + 1}", value=0.0)
            poids_sortie_centrifugation = st.number_input(f"Poids sortie centrifugation {i + 1}", value=0.0)
            remarques_centrifugation = st.text_area(f"Remarques centrifugation {i + 1}")
            centrifugations.append({
                "N° cuisson": no_cuisson_centrifugation,
                "Poids sortie lessivage": poids_sortie_lessivage_centrifugation,
                "Vitesse centrifugation": vitesse_centrifugation,
                "Durée centrifugation": duree_centrifugation,
                "Poids sortie centrifugation": poids_sortie_centrifugation,
                "Remarques": remarques_centrifugation
            })

        # Stockage en chambre froide réfrigérée (1er refroidissement avant surgélation)
        st.subheader("Stockage en chambre froide réfrigérée (1er refroidissement avant surgélation)")
        heure_entree_1ere_cuisson = st.time_input("Heure entrée 1ère cuisson")
        t_chambre_ref_entree = st.number_input("T°C chambre (entrée)", value=0.0)
        heure_sortie_derniere_cuisson = st.time_input("Heure sortie dernière cuisson")
        t_chambre_ref_sortie = st.number_input("T°C chambre (sortie)", value=0.0)
        remarques_refroidissement = st.text_area("Remarques refroidissement")

        # Suivi de la surgélation
        st.subheader("Suivi de la surgélation")
        surgelations = []
        num_surgelations = st.number_input("Nombre de surgélations", min_value=1, value=1, step=1)
        for i in range(num_surgelations):
            st.write(f"Surgélation {i + 1}")
            no_surgelation = st.number_input(f"N° Surgélation {i + 1}", min_value=1, value=1, step=1)
            quantite_surgelation = st.number_input(f"Quantité (kg) surgélation {i + 1}", value=0.0)
            t_produit_entree_surgelation = st.number_input(f"T°C produit entrée surgélation {i + 1}", value=0.0)
            t_surgelation = st.number_input(f"T°C de surgélation {i + 1}", value=0.0)
            duree_surgelation = st.number_input(f"Durée de surgélation {i + 1}", value=0.0)
            t_produit_sortie_surgelation = st.number_input(f"T°C produit sortie surgélation {i + 1}", value=0.0)
            surgelations.append({
                "N° Surgélation": no_surgelation, "Quantité (kg)": quantite_surgelation,
                "T°C produit entrée": t_produit_entree_surgelation,
                "T°C surgélation": t_surgelation, "Durée surgélation": duree_surgelation,
                "T°C produit sortie": t_produit_sortie_surgelation
            })

        # Stockage en chambre froide négative (attente avec conditionnement)
        st.subheader("Stockage en chambre froide négative (attente avec conditionnement)")
        heure_entree_1ere_surgelation = st.time_input("Heure entrée 1ère surgélation")
        t_chambre_neg_entree = st.number_input("T°C chambre (entrée)", value=0.0)
        heure_sortie_derniere_surgelation = st.time_input("Heure sortie dernière surgélation")
        t_chambre_neg_sortie = st.number_input("T°C chambre (sortie)", value=0.0)
        remarques_attente = st.text_area("Remarques attente conditionnement")

        # Conditionnement en sac en salle réfrigérée (<10°C)
        st.subheader("Conditionnement en sac en salle réfrigérée (<10°C)")
        heure_debut_conditionnement = st.time_input("Heure début conditionnement")
        t_chambre_conditionnement_debut = st.number_input("T°C chambre (début conditionnement)", value=0.0)
        heure_fin_conditionnement = st.time_input("Heure fin conditionnement")
        t_chambre_conditionnement_fin = st.number_input("T°C chambre (fin conditionnement)", value=0.0)
        remarques_conditionnement_general = st.text_area("Remarques conditionnement général")

        # Suivi du conditionnement - Thermoscellage
        st.subheader("Suivi du conditionnement - Thermoscellage")
        thermoscellages = []
        num_thermoscellages = st.number_input("Nombre de contrôles thermoscellage", min_value=1, value=1, step=1)
        for i in range(num_thermoscellages):
            st.write(f"Contrôle Thermoscellage {i + 1}")
            heure_controle_thermoscellage = st.time_input(f"Heure contrôle {i + 1}")
            t_thermoscellage = st.number_input(f"T°C Thermoscellage {i + 1}", value=0.0)
            controle_soudures = st.radio(f"Contrôle visuel des soudures {i + 1}", ["Conforme", "Non conforme"])
            controle_vide = st.radio(f"Contrôle visuel du vide {i + 1}", ["Conforme", "Non conforme"])
            remarques_thermoscellage = st.text_area(f"Remarques Thermoscellage {i + 1}")
            thermoscellages.append({
                "Heure contrôle": heure_controle_thermoscellage, "T°C Thermoscellage": t_thermoscellage,
                "Contrôle soudures": controle_soudures, "Contrôle vide": controle_vide,
                "Remarques": remarques_thermoscellage
            })

        # Stockage en chambre froide négative (produits finis conditionnés)
        st.subheader("Stockage en chambre froide négative (produits finis conditionnés)")
        heure_entree_1er_carton = st.time_input("Heure entrée 1er carton")
        t_chambre_pf_entree = st.number_input("T°C chambre (entrée produits finis)", value=0.0)
        heure_sortie_dernier_carton = st.time_input("Heure sortie dernier carton")
        t_chambre_pf_sortie = st.number_input("T°C chambre (sortie produits finis)", value=0.0)
        remarques_produits_finis = st.text_area("Remarques produits finis conditionnés")

        # Nombre de poches et cartons conditionnés
        st.subheader("Nombre de poches et cartons conditionnés")
        nombre_poches = st.number_input("Nombre de poches conditionnées", min_value=0, value=0, step=1)
        
        nombre_cartons = st.number_input("Nombre de cartons conditionnés", min_value=0, value=0, step=1)
        no_lot_poches = st.text_input("N° de lot (poches)")
        no_lot_cartons = st.text_input("N° de lot (cartons)")

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date de l'enregistrement": date_enregistrement,
            "Heure début enregistrement": heure_debut_enregistrement,
            "Heure fin enregistrement": heure_fin_enregistrement,
            "Réalisé par": realise_par,
            "Mélanges": melanges,
            "Stockage chambre froide réfrigérée": {
                "Heure entrée 1er mélange": heure_entree_1er_melange,
                "T°C chambre entrée": t_chambre_entree,
                "Heure sortie dernier mélange": heure_sortie_dernier_melange,
                "T°C chambre sortie": t_chambre_sortie,
                "Remarques": remarques_stockage
            },
            "Cuissons": cuissons,
            "Égouttages": egouttages,
            "Centrifugations": centrifugations,
            "Stockage chambre froide réfrigérée (avant surgélation)": {
                "Heure entrée 1ère cuisson": heure_entree_1ere_cuisson,
                "T°C chambre entrée": t_chambre_ref_entree,
                "Heure sortie dernière cuisson": heure_sortie_derniere_cuisson,
                "T°C chambre sortie": t_chambre_ref_sortie,
                "Remarques": remarques_refroidissement
            },
            "Surgélations": surgelations,
            "Stockage chambre froide négative (attente conditionnement)": {
                "Heure entrée 1ère surgélation": heure_entree_1ere_surgelation,
                "T°C chambre entrée": t_chambre_neg_entree,
                "Heure sortie dernière surgélation": heure_sortie_derniere_surgelation,
                "T°C chambre sortie": t_chambre_neg_sortie,
                "Remarques": remarques_attente
            },
            "Conditionnement": {
                "Heure début conditionnement": heure_debut_conditionnement,
                "T°C chambre début": t_chambre_conditionnement_debut,
                "Heure fin conditionnement": heure_fin_conditionnement,
                "T°C chambre fin": t_chambre_conditionnement_fin,
                "Remarques général": remarques_conditionnement_general
            },
            "Thermoscellages": thermoscellages,
            "Stockage chambre froide négative (produits finis)": {
                "Heure entrée 1er carton": heure_entree_1er_carton,
                "T°C chambre entrée": t_chambre_pf_entree,
                "Heure sortie dernier carton": heure_sortie_derniere_surgelation,
                "T°C chambre sortie": t_chambre_pf_sortie,
                "Remarques produits finis": remarques_produits_finis
            },
            "Nombre de poches": nombre_poches,
            "Nombre de cartons": nombre_cartons,
            "N° lot poches": no_lot_poches,
            "N° lot cartons": no_lot_cartons
        }
        save_data("suivi_fabrication", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("suivi_fabrication")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

def suivi_nettoyage():
    st.header("Suivi du Nettoyage")
    # This form involves a table-like structure, consider using st.dataframe for display/edit
    with st.form(key='suivi_nettoyage_form'):
        date_enregistrement = st.date_input("Date de l'enregistrement", datetime.date.today())
        controle_realise_par = st.text_input("Contrôle réalisé par")

        zones_nettoyage = [
            {"Zone": "Couloirs de circulation", "Element": "Sol et murs"},
            {"Zone": "Stockage négatif", "Element": "Sol et murs"},
            {"Zone": "Stockage MP", "Element": "Déchets évacués"},
            {"Zone": "Stockage MP", "Element": "Mélangeur"},
            {"Zone": "Stockage MP", "Element": "Petit matériel"},
            {"Zone": "Stockage MP", "Element": "Sol et murs"},
            {"Zone": "Zone Fabrication", "Element": "Déchets évacués"},
            {"Zone": "Zone Fabrication", "Element": "Marmite et égouttage"},
            {"Zone": "Zone Fabrication", "Element": "Essoreuse"},
            {"Zone": "Zone Fabrication", "Element": "Cellule de surgélation"},
            {"Zone": "Zone Fabrication", "Element": "Petit matériel"},
            {"Zone": "Zone Fabrication", "Element": "Sol et murs"},
            {"Zone": "Zone Conditionnement", "Element": "Déchets évacués"},
            {"Zone": "Zone Conditionnement", "Element": "Balance"},
            {"Zone": "Zone Conditionnement", "Element": "Scelleuse"},
            {"Zone": "Zone Conditionnement", "Element": "Petit matériel"},
            {"Zone": "Zone Conditionnement", "Element": "Sol et murs"}
        ]

        controles_nettoyage = []
        for zone in zones_nettoyage:
            st.subheader(f"Nettoyage - {zone['Zone']} - {zone['Element']}")
            visuel = st.checkbox("Visuel", key=f"{zone['Zone']}_{zone['Element']}_visuel")
            lg = st.checkbox("LG (Lame gélosée)", key=f"{zone['Zone']}_{zone['Element']}_lg")
            ec = st.checkbox("EC (écouvillon)", key=f"{zone['Zone']}_{zone['Element']}_ec")
            ext = st.text_input("Ext (analyse du laboratoire)", key=f"{zone['Zone']}_{zone['Element']}_ext")

            controles_nettoyage.append({
                "Zone": zone["Zone"],
                "Element": zone["Element"],
                "Visuel": visuel,
                "LG": lg,
                "EC": ec,
                "Ext": ext
            })

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date de l'enregistrement": date_enregistrement,
            "Contrôle réalisé par": controle_realise_par,
            "Contrôles de nettoyage": controles_nettoyage
        }
        save_data("suivi_nettoyage", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("suivi_nettoyage")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

def maitrise_risque_verre():
    st.header("Maîtrise du Risque 'Bris de Verre'")
    # Again, table-like structure, consider st.dataframe
    with st.form(key='maitrise_risque_verre_form'):
        date_enregistrement = st.date_input("Date de l'enregistrement", datetime.date.today())
        controle_realise_par = st.text_input("Contrôle réalisé par")

        zones_verre = ["Couloirs de circulation", "Stockage négatif", "Stockage MP",
                       "Zone Fabrication", "Zone Conditionnement"]

        controles_verre = []
        for zone in zones_verre:
            st.subheader(f"Contrôle Verre - {zone}")
            vitres = st.radio("Vitres", ["Conforme", "Non conforme"], key=f"{zone}_vitres")
            eclairages = st.radio("Eclairages", ["Conforme", "Non conforme"], key=f"{zone}_eclairages")
            porte_oculus = st.radio("Porte avec occulus", ["Conforme", "Non conforme"], key=f"{zone}_porte")
            tableau_affichage = st.radio("Tableau d'affichage", ["Conforme", "Non conforme"], key=f"{zone}_tableau")
            baes = st.radio("BAES", ["Conforme", "Non conforme"], key=f"{zone}_baes")
            action_corrective_date = st.date_input("Action corrective réalisée le", key=f"{zone}_action_date")
            action_corrective_par = st.text_input("Action corrective réalisée par", key=f"{zone}_action_par")
            nature_action_corrective = st.text_area("Nature de l'action corrective", key=f"{zone}_nature")

            controles_verre.append({
                "Zone": zone,
                "Vitres": vitres,
                "Eclairages": eclairages,
                "Porte avec occulus": porte_oculus,
                "Tableau d'affichage": tableau_affichage,
                "BAES": baes,
                "Action corrective réalisée le": action_corrective_date,
                "Action corrective réalisée par": action_corrective_par,
                "Nature de l'action corrective": nature_action_corrective
            })

        submit_button = st.form_submit_button(label="Enregistrer")

    if submit_button:
        data = {
            "Date de l'enregistrement": date_enregistrement,
            "Contrôle réalisé par": controle_realise_par,
            "Contrôles du risque verre": controles_verre
        }
        save_data("maitrise_risque_verre", data)
        st.success("Fiche enregistrée !")

    # Display previous data
    if st.checkbox("Afficher les fiches précédentes"):
        previous_data = load_data("maitrise_risque_verre")
        if not previous_data.empty:
            st.dataframe(previous_data)
        else:
            st.info("Aucune fiche précédente enregistrée.")

# --- Main App ---
def main():
    st.sidebar.title("Navigation")
    module = st.sidebar.selectbox("Sélectionner le module", [
        "Contrôles à Réception",
        "Contrôles à Expédition",
        "Contrôle Température Chambres Froides",
        "Fiche de Non-Conformité Matériel",
        "Traçabilité Interne",
        "Qualité de l'Huile de Cuisson",
        "Contrôle État Machine",
        "Contrôle Balance",
        "Suivi de la Fabrication",
        "Suivi du Nettoyage",
        "Maîtrise du Risque Verre"
    ])

    if module == "Contrôles à Réception":
        controle_reception()
    elif module == "Contrôles à Expédition":
        controle_expedition()
    elif module == "Contrôle Température Chambres Froides":
        controle_temperature_chambres()
    elif module == "Fiche de Non-Conformité Matériel":
        fiche_non_conformite_materiel()
    elif module == "Traçabilité Interne":
        traceabilite_interne()
    elif module == "Qualité de l'Huile de Cuisson":
        qualite_huile_cuisson()
    elif module == "Contrôle État Machine":
        controle_etat_machine()
    elif module == "Contrôle Balance":
        controle_balance()
    elif module == "Suivi de la Fabrication":
        suivi_fabrication()
    elif module == "Suivi du Nettoyage":
        suivi_nettoyage()
    elif module == "Maîtrise du Risque Verre":
        maitrise_risque_verre()

if __name__ == "__main__":
    main()