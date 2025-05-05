import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime

UBIDOTS_TOKEN = "BBUS-12k3H1t3siSKFWPyeh0k0jc4mdjmkN"  # Ganti jika perlu
DEVICE_LABEL = "esp32"
VARIABLE_LABEL = "berat"
BASE_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"

HEADERS = {
    "X-Auth-Token": UBIDOTS_TOKEN,
    "Content-Type": "application/json"
}

def get_latest_weight():
    try:
        url = f"{BASE_URL}/{VARIABLE_LABEL}/lv"
        res = requests.get(url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            return float(res.text)
        return None
    except:
        return None

def get_weight_history(limit=10):
    try:
        url = f"{BASE_URL}/{VARIABLE_LABEL}/values?limit={limit}"
        res = requests.get(url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            data = res.json()["results"]
            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["value"] = df["value"].astype(float)
            return df[["datetime", "value"]]
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# UI
st.set_page_config(page_title="Smart Door Weight Monitor", layout="centered")
st.title("🚪 Smart Security - Pressure Plate Monitor")
st.caption("📡 Data berat dikirim dari ESP32 ke Ubidots")

berat = get_latest_weight()
col1, col2 = st.columns(2)

with col1:
    st.metric("Berat Terakhir", f"{berat:.1f} kg" if berat else "N/A")

with col2:
    if berat:
        st.success("✅ Akses diberikan" if berat > 0 else "⛔ Tidak ada berat terdeteksi")

st.caption(f"🕒 Terakhir diperbarui: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

st.subheader("📈 Riwayat Berat")
limit = st.slider("Jumlah data", 5, 50, 10)
df = get_weight_history(limit)

if not df.empty:
    chart = alt.Chart(df).mark_line().encode(
        x="datetime:T",
        y="value:Q"
    ).properties(title="Perubahan Berat dari Pressure Plate")
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Belum ada data berat.")
