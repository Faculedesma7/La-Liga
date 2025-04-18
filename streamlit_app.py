import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="La Liga Live 2025", layout="wide")
st.title("⚽ La Liga 2024/2025 - En Vivo con Predicciones")

API_KEY = "33247bdd475582ecc4324a116254a287"
LEAGUE_ID = 140  # La Liga
SEASON = 2024
HEADERS = {
    "x-apisports-key": API_KEY
}

@st.cache_data(ttl=300)
def obtener_tabla():
    url = f"https://v3.football.api-sports.io/standings"
    params = {"league": LEAGUE_ID, "season": SEASON}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    try:
        equipos = data["response"][0]["league"]["standings"][0]
        tabla = []
        for team in equipos:
            tabla.append({
                "Posición": team["rank"],
                "Equipo": team["team"]["name"],
                "PJ": team["all"]["played"],
                "G": team["all"]["win"],
                "E": team["all"]["draw"],
                "P": team["all"]["lose"],
                "GF": team["all"]["goals"]["for"],
                "GC": team["all"]["goals"]["against"],
                "Pts": team["points"]
            })
        return pd.DataFrame(tabla)
    except:
        return None

# Obtener tabla
tabla_df = obtener_tabla()

st.subheader("📊 Tabla de Posiciones - La Liga 2024/2025")
if tabla_df is not None:
    st.dataframe(tabla_df.sort_values("Posición"), use_container_width=True)

    # Gráfico
    st.subheader("📈 Gráfico de Puntos")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(tabla_df["Equipo"], tabla_df["Pts"], color="deepskyblue")
    ax.set_xlabel("Puntos")
    ax.set_title("Puntos por Equipo")
    ax.invert_yaxis()
    st.pyplot(fig)

    # Predicción
    st.subheader("🔮 Predicción de Partido")
    equipos = tabla_df["Equipo"].tolist()
    col1, col2 = st.columns(2)
    with col1:
        equipo1 = st.selectbox("Equipo 1", equipos)
    with col2:
        equipo2 = st.selectbox("Equipo 2", equipos, index=1 if len(equipos) > 1 else 0)

    if equipo1 != equipo2:
        stats1 = tabla_df[tabla_df["Equipo"] == equipo1].iloc[0]
        stats2 = tabla_df[tabla_df["Equipo"] == equipo2].iloc[0]
        st.markdown("### Resultado Probable")
        if stats1["Pts"] > stats2["Pts"]:
            st.success(f"{equipo1} tiene más chances de ganar.")
        elif stats2["Pts"] > stats1["Pts"]:
            st.success(f"{equipo2} tiene más chances de ganar.")
        else:
            st.info("Es un partido muy parejo. Empate posible.")
    else:
        st.warning("Elegí dos equipos distintos.")
else:
    st.error("⚠️ No se pudo cargar la tabla. Verificá tu API Key o intentá más tarde.")
