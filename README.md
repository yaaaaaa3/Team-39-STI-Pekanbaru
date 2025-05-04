
# Pressure Plate Door - Team 39 STI Pekanbaru

Sistem otomatisasi pintu berbasis **ESP32** yang menggunakan beberapa sensor dan dikontrol melalui aplikasi **Streamlit** berbasis Python.

## 🚪 Fitur Utama

- Deteksi kehadiran dengan **sensor ultrasonik**
- Deteksi beban menggunakan **load cell**
- Autentikasi pengguna dengan **fingerprint sensor (AS608)**
- Pengendalian pintu otomatis dengan **motor servo**
- Visualisasi data sensor secara real-time di **Streamlit Dashboard**

---

## 🧰 Perangkat Keras

- ESP32 Dev Board
- Sensor Ultrasonik HC-SR04
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

---

## 📦 Instalasi

1. **Clone repositori ini**:
   ```bash
   git clone https://github.com/ya555522/pressure-plate-door.git
   cd pressure-plate-door
   ```

2. **Install dependensi Python**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Sambungkan ESP32 via kabel USB**, dan pastikan port-nya benar (misal: `COM3` atau `/dev/ttyUSB0`).

4. **Jalankan aplikasi Streamlit**:
   ```bash
   streamlit run app.py
   ```

---

## 🔄 Format Data Serial dari ESP32

ESP32 mengirim data ke PC melalui serial dengan format berikut:

```
<jarak_cm>,<berat_kg>,<status_fingerprint>,<status_servo>
```

**Contoh:**
```
34.5,12.7,Terdaftar,Terbuka
```

---

## 📊 Tampilan Dashboard

Aplikasi Streamlit menampilkan:
- Jarak dari sensor ultrasonik
- Berat dari load cell
- Status fingerprint
- Status servo pintu (terbuka/tertutup)

---

## 👨‍💻 Kontributor

- Team 39 - STI Pekanbaru
