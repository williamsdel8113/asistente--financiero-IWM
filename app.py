import streamlit as st
import pandas as pd
import requests
import yfinance as yf

# Configuración inicial
st.set_page_config(page_title="Asistente Financiero IWM", layout="wide")
st.title("📊 Asistente Financiero Automatizado para IWM")

# API Key de Alpha Vantage
API_KEY = "TU_API_KEY_AQUÍ"  # ← Reemplaza con tu clave personal de Alpha Vantage

# Función para obtener precios y BID/ASK
def obtener_precio_actual(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    return info.get("regularMarketPrice"), info.get("bid"), info.get("ask")

# Función para obtener medias móviles y Bollinger Bands
def obtener_indicadores(symbol, interval="60min"):
    url = f"https://www.alphavantage.co/query?function=BBANDS&symbol={symbol}&interval={interval}&time_period=20&series_type=close&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    return "BBANDS" in data

# Función para detectar GAP
def detectar_gap(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="2d")
    if len(hist) < 2:
        return False
    cierre = hist["Close"].iloc[-2]
    apertura = hist["Open"].iloc[-1]
    return abs(apertura - cierre) > 0.5

# Tabla de requisitos
requisitos = [
    "Reunión FED (última y próxima)",
    "Earnings (últimos y próximos)",
    "Bollinger Bands (15m, 1h, 1d)",
    "Medias móviles (1h, 1d)",
    "Punto de ruptura de línea de tendencia",
    "GAP al alza o a la baja",
    "Precio actual",
    "BID & ASK",
    "Fecha de expiración (si aplica para opciones)"
]

# Evaluaciones automáticas
precio, bid, ask = obtener_precio_actual("IWM")
gap_detectado = detectar_gap("IWM")
bbands_1h = obtener_indicadores("IWM", "60min")

# Construcción de tabla
estado = []
for req in requisitos:
    if req == "Precio actual":
        estado.append("✅" if precio else "❌")
    elif req == "BID & ASK":
        estado.append("✅" if bid and ask else "❌")
    elif req == "GAP al alza o a la baja":
        estado.append("✅" if gap_detectado else "❌")
    elif req == "Bollinger Bands (15m, 1h, 1d)":
        estado.append("✅" if bbands_1h else "❌")
    else:
        estado.append("🔲")  # Manual o pendiente

# Mostrar tabla
df = pd.DataFrame({
    "REQUISITOS": requisitos,
    "SE CUMPLE": [s if s == "✅" else "" for s in estado],
    "NO SE CUMPLE": [s if s == "❌" else "" for s in estado]
})
st.dataframe(df, use_container_width=True)

# Mostrar precios
st.markdown(f"**Precio actual de IWM:** ${precio:.2f}")
st.markdown(f"**BID:** ${bid:.2f} | **ASK:** ${ask:.2f}")