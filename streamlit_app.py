import streamlit as st
import folium
from streamlit_folium import st_folium
import time

# === Définir les scénarios ===
scenarios = {
    "Trajet Normal": [
        (35.66367, 10.11041),
        (35.62677,10.16845),
        (35.6298846, 10.2123705),
        (35.5908689 ,10.1914794),
        (35.6046867,10.2570794),
        (35.512247,10.287366),
        (35.66367, 10.11041)
        
    
    ],
    "Nouveau Trajet": [
         (35.66367, 10.11041),
        (35.62677,10.16845),
        (35.6298846, 10.2123705),
        (35.5908689 ,10.1914794),
        (35.6046867,10.2570794),
        (35.512247,10.287366),
        (35.62677,10.16845)
       ] 
}


st.title("🚌 Simulation de Trajet de Bus")

# === Sélection du scénario ===
scenario = st.selectbox("Scénario :", list(scenarios.keys()))
trajet = scenarios[scenario]

# === Zone dynamique pour la carte ===
carte_placeholder = st.empty()

# === Bouton pour lancer l’animation ===
if st.button("▶️ Lancer la simulation"):
    for i, point in enumerate(trajet):
        # Créer la carte vide à chaque étape
        m = folium.Map(location=point, zoom_start=14)

        # Ligne du trajet
        folium.PolyLine(trajet, color="blue", weight=4).add_to(m)

        # Position actuelle du bus
        folium.Marker(
            location=point,
            icon=folium.Icon(color="red", icon="bus", prefix="fa"),
            popup=f"Étape {i + 1}"
        ).add_to(m)

        # Afficher dans le placeholder avec une clé différente à chaque étape
        with carte_placeholder.container():
            st_folium(m, width=700, height=500, key=f"map_{i}")

        time.sleep(0.2)
