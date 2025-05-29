import streamlit as st
import graphviz
import pandas as pd
import requests
# --- Initialisation du state ---
if "page" not in st.session_state:
    st.session_state.page = 1
if "data" not in st.session_state:
    st.session_state.data = []

# --- Fonction de soumission ---
def valider_formulaire():
    trajet = {
        "lieu_depart": lieu_depart,
        "arrivee_1": lieu_arrivee_1,
        "arrivee_2": lieu_arrivee_2,
        "arrivee_3": lieu_arrivee_3,
        "collegiens": nb_collegiens,
        "lyceens": nb_lyceens,
        "bus":nb_bus
        
    }
    st.session_state.data.append(trajet)
    st.session_state.page += 1

# --- Titre ---
st.title("Circuit de transport scolaire")
col1 , col2=st.columns((3.5, 3), gap="medium")

with col1: 
    st.title(f"Trajet numéro  {st.session_state.page} : Saisie le trajet")


        # --- Entrée utilisateur ---
    lieux = [ "ElKwassam","Nabech", "ElKhazaziya", "ElMakhssouma", "ElHenbez","Awled Nhar","Collège assad Ibn Fourt", "Lycée Okba Ibn Nafaa","  Retour   "]
    lieu_depart = st.selectbox("📍 Lieu de départ :", lieux, key=f"dep{st.session_state.page}")
    lieu_arrivee_1 = st.selectbox("🏁 Lieu d'arrivée 1 :", lieux, key=f"arr1_{st.session_state.page}")
    lieu_arrivee_2 = st.selectbox("🏁 Lieu d'arrivée 2 :", lieux, key=f"arr2_{st.session_state.page}")
    lieu_arrivee_3 = st.selectbox("🏁 Lieu d'arrivée 3 :", lieux, key=f"arr3_{st.session_state.page}")

    nb_collegiens = st.number_input("👦 Nombre de collégiens :", min_value=0, value=0, key=f"col{st.session_state.page}")
    nb_lyceens = st.number_input("👩🏻‍🎓 Nombre de lycéens :", min_value=0, value=0, key=f"lyc{st.session_state.page}")
    nb_bus=st.number_input("🚌 Nombre de bus utilisé pour assurer le transport de cette tranche d'élève:",min_value=0, value=0,key=f"bus{st.session_state.page}")
        # --- Calcul ---
    total_eleves = nb_collegiens + nb_lyceens
            # --- Résultats ---
    st.markdown(f"### 🚸 Total d'élèves : {total_eleves}")
    st.markdown(f"### 🚌 Bus nécessaires : {nb_bus}")

with col2:   
        # --- Graphique ---
    if lieu_depart and (lieu_arrivee_1 or lieu_arrivee_2):
        st.subheader("🛣️ Trajet Réalisé :")
        dot = graphviz.Digraph()
        dot.node("D", lieu_depart)
        if lieu_arrivee_1:
            dot.node("A1", lieu_arrivee_1)
            dot.edge("D", "A1", label="Trajet 1")
        if lieu_arrivee_2 and lieu_arrivee_2 != lieu_arrivee_1:
            dot.node("A2", lieu_arrivee_2)
            dot.edge("A1", "A2", label="Trajet 2")
        if lieu_arrivee_3 and lieu_arrivee_3 != lieu_arrivee_2:
            dot.node("A3", lieu_arrivee_3)
            dot.edge("A2", "A3", label="Trajet 3")
        st.graphviz_chart(dot)


# Validation
if st.button("✅ Valider Ce trajet et passer au suivant"):
    valider_formulaire()

    # Option : Fin de saisie
    if st.session_state.page > 1:
        df = pd.DataFrame(st.session_state.data)
        csv_data = df.to_csv(index=False)
        if st.button("📤 Envoyer ce trajet saisi par email et terminer la saisie"):
            response = requests.post(
                "https://hooks.zapier.com/hooks/catch/23104980/2jwtn4u/",
                json={"filename": "trajets.csv", "content": csv_data}
                )
            if response.status_code == 200:
                st.success("✅ Trajets envoyés par email avec succès !")
            else:
                 st.error("❌ Une erreur est survenue lors de l'envoi.")
                    


    
