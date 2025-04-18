import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="La Liga Live ⚽", layout="wide")
st.title("⚽ La Liga 2024/2025 - Datos en Vivo y Predicciones")

# ------------------- CONFIG -------------------
ZYLALABS_API_URL = "https://zylalabs.com/api/857/la+liga+table+api/635/obtain+la+liga+table"
TEMPORADA = "2024"
# ----------------------------------------------

@st.cache_data(ttl=300)  # se actualiza cada 5 minutos
def obtener_tabla():
    try:
        response = requests.get(ZYLALABS_API_URL, params={"season": TEMPORADA})
        data = response.json()
        tabla = []
        for team in data:
            tabla.append({
                "Posición": team["position"],
                "Equipo": team["team"]["name"],
                "PJ": team["stats"]["played"],
                "G": team["stats"]["wins"],
                "E": team["stats"]["draws"],
                "P": team["stats"]["loses"],
                "GF": team["stats"]["goalsFor"],
                "GC": team["stats"]["goalsAgainst"],
                "Pts": team["stats"]["points"]
            })
        return pd.DataFrame(tabla)
    except Exception as e:
        return None

# Obtener tabla y mostrar
st.subheader("📊 Tabla de posiciones")
tabla_df = obtener_tabla()

if tabla_df is not None:
    st.dataframe(tabla_df.sort_values("Posición"), use_container_width=True)

    # Gráfico de barras - Puntos por equipo
    st.subheader("📈 Comparación de puntos")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(tabla_df["Equipo"], tabla_df["Pts"], color="skyblue")
    ax.invert_yaxis()
    ax.set_xlabel("Puntos")
    ax.set_title("Puntos por equipo")
    st.pyplot(fig)

    # Predicción
    st.subheader("🔮 Predicción de partido")
    equipos = tabla_df["Equipo"].tolist()
    col1, col2 = st.columns(2)
    with col1:
        equipo1 = st.selectbox("Equipo 1", equipos)
    with col2:
        equipo2 = st.selectbox("Equipo 2", equipos, index=1 if len(equipos) > 1 else 0)

    if equipo1 != equipo2:
        stats1 = tabla_df[tabla_df["Equipo"] == equipo1].iloc[0]
        stats2 = tabla_df[tabla_df["Equipo"] == equipo2].iloc[0]

        if stats1["Pts"] > stats2["Pts"]:
            st.success(f"✅ {equipo1} tiene más chances de ganar.")
        elif stats2["Pts"] > stats1["Pts"]:
            st.success(f"✅ {equipo2} tiene más chances de ganar.")
        else:
            st.info("⚠️ Es un partido parejo, puede ser empate.")
    else:
        st.warning("Elegí dos equipos distintos.")
else:
    st.error("⚠️ No se pudo cargar la tabla. Intentá más tarde o verificá la API.")
