import streamlit as st
import graphviz

# --- Titre ---
st.title("Circuit de transport scolaire")

# --- Entrée utilisateur ---
lieux = ["Collège assad Ibn Fourt", "Lycée Okba Ibn Nafaa", "ElKwessam","Nabech", "ElKhazaziya", "ElMakhssouma", "ElHenbez","Awled Nhar"]

lieu_depart = st.selectbox("📍 Lieu de départ :", lieux)
lieu_arrivee_1 = st.selectbox("🏁 Lieu d'arrivée 1 :", lieux)
lieu_arrivee_2 = st.selectbox("🏁 Lieu d'arrivée 2 :", lieux)
lieu_arrivee_3 = st.selectbox("🏁 Lieu d'arrivée 3 :", lieux)

nb_collegiens = st.number_input("👦 Nombre de collégiens :", min_value=0, value=0)
nb_lyceens = st.number_input("👩 Nombre de lycéens :", min_value=0, value=0)
nb_bus=st.number_input("Nombre de bus utilisé pour assurer le transport de cette tranche d'élève:",min_value=0, value=0)

# --- Calcul ---
total_eleves = nb_collegiens + nb_lyceens


# --- Graphique ---
if lieu_depart and (lieu_arrivee_1 or lieu_arrivee_2):
    st.subheader("🛣️ Trajet proposé :")
    dot = graphviz.Digraph()
    dot.node("D", lieu_depart)
    if lieu_arrivee_1:
        dot.node("A1", lieu_arrivee_1)
        dot.edge("D", "A1", label="Trajet 1")
    if lieu_arrivee_2 and lieu_arrivee_2 != lieu_arrivee_1:
        dot.node("A2", lieu_arrivee_2)
        dot.edge("A1", "A2", label="Trajet 2")
     if lieu_arrivee_2 and lieu_arrivee_2 != lieu_arrivee_2:
        dot.node("A3", lieu_arrivee_3)
        dot.edge("A2", "A3", label="Trajet 3")
        
    st.graphviz_chart(dot)

    # --- Résultats ---
    st.markdown(f"### 🚸 Total d'élèves : {total_eleves}")
    st.markdown(f"### 🚌 Bus nécessaires : {nb_bus}")

    # --- Validation ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Valider le schéma"):
            st.success("Schéma validé ! Enregistrement en cours...")

    with col2:
        if st.button("🔁 Corriger les informations"):
            st.warning("Veuillez modifier les données ci-dessus.")

