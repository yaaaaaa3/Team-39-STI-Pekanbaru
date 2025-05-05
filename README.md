# *Pressure Plate Door* 
- Team 39 STI Pekanbaru

Sistem otomatisasi pintu berbasis **ESP32** yang menggunakan beberapa sensor dan dikontrol melalui aplikasi **Streamlit** berbasis Python.

## 🚪 Fitur Utama
- Autentikasi pengguna dengan **fingerprint sensor (AS608)**
- Pengendalian pintu otomatis dengan **motor servo**
- Visualisasi data sensor secara real-time di **Blynk Dashboard**

---

## 🧰 Perangkat Keras

- ESP32 Dev Board
- Sensor Fingerprint AS608
- LoadCell + HX711 Module
- Motor Servo SG90 / MG996R
- Breadboard dan kabel jumper
- LED
- LCD I2C 16x2

---

## 💻 Software yang Digunakan

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- PySerial (`pyserial`)
- Arduino IDE untuk pemrograman ESP32
- VisualStudio Code
- Blynk Cloud

---

## 📊 Tampilan Dashboard

Aplikasi Streamlit menampilkan:
- Status fingerprint
- Status servo pintu (terbuka/tertutup)
- Riwayat Berat
