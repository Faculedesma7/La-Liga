import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="La Liga 2025 en Vivo", layout="wide")
st.title("⚽ La Liga 2024/25 - Tabla en Vivo + Predicciones")

# Temporada actual
season = "2024"

# Obtener datos de API gratuita de ZylaLabs
@st.cache_data(ttl=3600)
def obtener_datos():
    url = "https://zylalabs.com/api/857/la+liga+table+api/635/obtain+la+liga+table"
    params = {"season": season}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

# Mostrar tabla de posiciones
data = obtener_datos()
if data:
    tabla = []
    for team in data:
        tabla.append({
            "Pos": team["position"],
            "Equipo": team["team"]["name"],
            "PJ": team["stats"]["played"],
            "G": team["stats"]["wins"],
            "E": team["stats"]["draws"],
            "P": team["stats"]["loses"],
            "GF": team["stats"]["goalsFor"],
            "GC": team["stats"]["goalsAgainst"],
            "Dif": team["stats"]["goalsFor"] - team["stats"]["goalsAgainst"],
            "Pts": team["stats"]["points"]
        })

    df = pd.DataFrame(tabla)
    df = df.sort_values("Pos")
    st.dataframe(df, use_container_width=True)

    st.subheader("🔮 Predicción entre equipos")

    equipos = df["Equipo"].tolist()
    col1, col2 = st.columns(2)
    with col1:
        equipo1 = st.selectbox("Elegí el primer equipo", equipos)
    with col2:
        equipo2 = st.selectbox("Elegí el segundo equipo", equipos, index=1)

    if equipo1 != equipo2:
        e1 = df[df["Equipo"] == equipo1].iloc[0]
        e2 = df[df["Equipo"] == equipo2].iloc[0]

        score1 = (e1["Pts"] * 2 + e1["GF"] - e1["GC"])
        score2 = (e2["Pts"] * 2 + e2["GF"] - e2["GC"])

        st.markdown("### 🤔 Resultado estimado")
        if score1 > score2:
            st.success(f"✅ {equipo1} tiene más chances de ganar.")
        elif score2 > score1:
            st.success(f"✅ {equipo2} tiene más chances de ganar.")
        else:
            st.info("⚖️ Muy parejo, puede ser empate.")
    else:
        st.warning("Elegí dos equipos distintos.")
else:
    st.error("No se pudieron cargar los datos. Intentá más tarde.")
