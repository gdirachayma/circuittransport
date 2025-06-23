import streamlit as st
import folium
from streamlit_folium import st_folium
import time

# === Données enrichies avec arret + élèves
trajet_info = [
    {"coords": (35.66367, 10.11041), "arret": "Départ - Lycée Ibn Sina", "eleves": 12},
    {"coords": (35.62677, 10.16845), "arret": "Arrêt 1 - Collège Ennour", "eleves": 8},
    {"coords": (35.6298846, 10.2123705), "arret": "Arrêt 2 - École Primaire", "eleves": 5},
    {"coords": (35.5908689 ,10.1914794), "arret": "Arrêt 3 - Institut Agricole", "eleves": 7},
    {"coords": (35.6046867,10.2570794), "arret": "Arrêt 4 - Quartier Sud", "eleves": 3},
    {"coords": (35.512247,10.287366), "arret": "Dernier Arrêt - Terminal", "eleves": 0}
]

# === Session State pour animation
if "step" not in st.session_state:
    st.session_state.step = 0
if "run" not in st.session_state:
    st.session_state.run = False

st.title("🚌 Animation du circuit scolaire en temps réel")

# === Bouton pour lancer
if st.button("▶️ Lancer le trajet"):
    st.session_state.step = 0
    st.session_state.run = True

# === Zone dynamique
map_placeholder = st.empty()

# === Si l'animation est en cours
if st.session_state.run and st.session_state.step < len(trajet_info):

    current = trajet_info[st.session_state.step]

    # Créer la carte centrée sur le point actuel
    m = folium.Map(location=current["coords"], zoom_start=13)

    # Ajouter tous les arrêts
    for i, info in enumerate(trajet_info):
        folium.Marker(
            location=info["coords"],
            popup=f"{info['arret']}<br>🎒 Élèves: {info['eleves']}",
            icon=folium.Icon(color="blue" if i != st.session_state.step else "red", icon="bus")
        ).add_to(m)

    # Tracer la ligne du trajet complet
    folium.PolyLine([pt["coords"] for pt in trajet_info], color="blue", weight=4).add_to(m)

    # Afficher la carte
    map_placeholder.folium_chart = st_folium(m, width=700, height=500)

    # Passer à l'étape suivante
    st.session_state.step += 1
    time.sleep(1)
    st.experimental_rerun()

elif st.session_state.step >= len(trajet_info):
    st.success("✅ Le trajet est terminé !")
    st.session_state.run = False
