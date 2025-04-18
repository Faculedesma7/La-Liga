import streamlit as st
import requests

st.set_page_config(page_title="La Liga Live 2025", layout="wide")
st.title("⚽ Tabla en Vivo - La Liga 2024/2025")

# API gratuita desde ZylaLabs para La Liga
@st.cache_data(ttl=600)  # Cache por 10 minutos
def obtener_tabla():
    try:
        url = "https://zylalabs.com/api/857/la+liga+table+api/635/obtain+la+liga+table"
        params = {"season": "2024"}  # Temporada actual
        response = requests.get(url, params=params)
        data = response.json()

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

        return tabla
    except Exception as e:
        print("Error al obtener datos:", e)
        return None

# Mostrar tabla
tabla = obtener_tabla()
if tabla:
    st.dataframe(tabla, use_container_width=True)
else:
    st.error("No se pudo cargar la tabla. Intentá más tarde.")

# Predicción básica entre 2 equipos
st.subheader("🤖 Predicción: ¿Quién tiene más chances de ganar?")
equipos = [fila["Equipo"] for fila in tabla] if tabla else []

col1, col2 = st.columns(2)
with col1:
    equipo1 = st.selectbox("Equipo 1", equipos)
with col2:
    equipo2 = st.selectbox("Equipo 2", equipos, index=1 if len(equipos) > 1 else 0)

if equipo1 and equipo2 and equipo1 != equipo2:
    eq1 = next(e for e in tabla if e["Equipo"] == equipo1)
    eq2 = next(e for e in tabla if e["Equipo"] == equipo2)

    puntos1 = eq1["Pts"]
    puntos2 = eq2["Pts"]
    dif1 = eq1["Dif"]
    dif2 = eq2["Dif"]

    resultado = f"🔮 Resultado: "
    if puntos1 > puntos2:
        resultado += f"{equipo1} tiene más chances de ganar."
    elif puntos2 > puntos1:
        resultado += f"{equipo2} tiene más chances de ganar."
    else:
        if dif1 > dif2:
            resultado += f"{equipo1} tiene más chances (mejor diferencia de gol)."
        elif dif2 > dif1:
            resultado += f"{equipo2} tiene más chances (mejor diferencia de gol)."
        else:
            resultado += "Es un partido muy parejo, puede ser empate."

    st.success(resultado)
elif equipo1 == equipo2:
    st.warning("Elegí dos equipos distintos.")
