# *Pressure Plate Door* 
- Team 39 STI Pekanbaru

Sistem otomatisasi pintu berbasis **ESP32** yang menggunakan beberapa sensor dan dikontrol melalui aplikasi **Streamlit** berbasis Python.

## 🚪 Fitur Utama

- Deteksi beban menggunakan **load cell**
- Autentikasi pengguna dengan **fingerprint sensor (AS608)**
- Pengendalian pintu otomatis dengan **motor servo**
- Visualisasi data sensor secara real-time di **Ubidots Dashboard**

---

## 🧰 Perangkat Keras

- ESP32 Dev Board
- Load Cell + HX711 Amplifier
- Sensor Fingerprint AS608
- Motor Servo SG90 / MG996R
- Breadboard dan kabel jumper

---

## 💻 Software yang Digunakan

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- PySerial (`pyserial`)
- Arduino IDE untuk pemrograman ESP32
- Thonny

---

## 📊 Tampilan Dashboard

Aplikasi Streamlit menampilkan:
- Berat dari load cell
- Status fingerprint
- Status servo pintu (terbuka/tertutup)
- Riwayat Berat
