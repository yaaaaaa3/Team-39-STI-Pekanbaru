# app.py
import streamlit as st
import serial
import time
import json

st.set_page_config(page_title="Aplikasi Deteksi Sidik Jari", layout="centered")
st.title("Aplikasi Deteksi Sidik Jari & Kontrol Pintu")

# Fungsi bantu untuk membaca data dari sensor via Serial
@st.cache_resource
def get_serial_connection(port="COM3", baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Tunggu koneksi stabil
        return ser
    except Exception as e:
        st.error(f"Gagal membuka koneksi serial: {e}")
        return None

# Inisialisasi koneksi serial
ser = get_serial_connection()

# Tampilkan status sensor
if ser:
    st.success("Tersambung ke sensor sidik jari!")
else:
    st.warning("Tidak dapat tersambung ke sensor. Periksa koneksi hardware.")

# Tombol untuk memulai proses deteksi sidik jari
if st.button("Scan Sidik Jari"):
    if ser:
        st.info("Menunggu respon dari sensor...")
        try:
            # Kirim perintah ke Arduino jika diperlukan (opsional)
            ser.write(b'scan\n')
            time.sleep(2)

            if ser.in_waiting:
                response = ser.readline().decode().strip()
                st.success("Data diterima dari sensor:")
                st.code(response)

                # Jika Arduino mengirimkan data JSON, tampilkan lebih rapi
                try:
                    result = json.loads(response)
                    st.json(result)
                except:
                    st.write(response)

            else:
                st.warning("Tidak ada respon dari sensor.")
        except Exception as e:
            st.error(f"Error saat membaca data: {e}")
    else:
        st.error("Serial belum tersambung.")

# Form untuk kirim perintah ke Arduino (opsional)
with st.form("perintah_form"):
    command = st.text_input("Kirim perintah manual ke Arduino (opsional):")
    kirim = st.form_submit_button("Kirim")

    if kirim and ser:
        try:
            ser.write((command + "\n").encode())
            st.success(f"Perintah '{command}' telah dikirim.")
        except Exception as e:
            st.error(f"Gagal mengirim perintah: {e}")
