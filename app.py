import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import random
import base64

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Aplikasi Lengkap dengan Latar Belakang & Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =========================================================
# MENAMBAHKAN LATAR BELAKANG DENGAN CSS KUSTOM
# =========================================================
# Pastikan file 'background.jpg' sudah diunggah ke repositori GitHub kamu
background_image_path = "background.jpg"

def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string.decode()}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.92);
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        pass # Jika file gambar belum ada, aplikasi tetap berjalan normal tanpa background

add_bg_from_local(background_image_path)

# =========================================================
# KONFIGURASI GOOGLE APPS SCRIPT WEB APP URL
# =========================================================
# Ganti teks di dalam tanda kutip dengan URL Web App dari Google Apps Script kamu
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyyO_Vnj3f6_Qtq7v32tJewxbTH77ZMQUwHAHZfQbAE1IwCwPuOZU42uqc_kErDgOKA/exec"

# =========================================================
# NAVIGATION BAR / PILIHAN MENU
# =========================================================
st.sidebar.title("📌 Navigation Menu")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Mini Game Seru", "Kritik & Pesan"]
)


# HALAMAN 1: MINI GAME SERU (Diperbaiki agar clue muncul)

if menu == "Mini Game Seru":
    st.title("🎮 Arcade: Tebak Angka Misterius")
    st.write("Uji keberuntungan dan logika-mu! Temukan angka rahasia sebelum nyawamu habis.")
    st.write("---")

    # Pilih Level Kesulitan
    level = st.selectbox("Pilih Level Kesulitan:", ["Mudah (1 - 50)", "Sedang (1 - 100)", "Sulit (1 - 200)"])
    
    max_val = 50 if "Mudah" in level else (100 if "Sedang" in level else 200)

    # Inisialisasi State Game
    if "target" not in st.session_state or st.session_state.get("max_val") != max_val:
        st.session_state.max_val = max_val
        st.session_state.target = random.randint(1, max_val)
        st.session_state.lives = 5
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.win = False
        st.session_state.clue_used = False
        st.session_state.message = ""
        st.session_state.clue_text = ""

    # Tampilkan Status Nyawa & Percobaan
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="Sisa Nyawa ❤️", value=f"{st.session_state.lives} / 5")
    with col_stat2:
        st.metric(label="Total Tebakan 🎯", value=st.session_state.attempts)

    if not st.session_state.game_over and not st.session_state.win:
        tebakan = st.number_input(f"Masukkan angka antara 1 sampai {max_val}:", min_value=1, max_value=max_val, value=1, step=1)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            kirim_btn = st.button("Kirim Tebakan 🚀", use_container_width=True)
        with col_btn2:
            clue_btn = st.button("🔍 Minta Clue", use_container_width=True)

        # Logika Tombol Clue
        if clue_btn:
            if not st.session_state.clue_used:
                st.session_state.clue_used = True
                sifat = "Genap" if st.session_state.target % 2 == 0 else "Ganjil"
                kelipatan_5 = "Ya" if st.session_state.target % 5 == 0 else "Tidak"
                st.session_state.clue_text = f"💡 *CLUE:* Angka rahasia berstatus *{sifat}* dan kelipatan 5 adalah *{kelipatan_5}*!"
            else:
                st.session_state.clue_text = "⚠️ Clue sudah digunakan untuk ronde ini!"

        # Tampilkan Clue jika ada
        if st.session_state.clue_text:
            st.info(st.session_state.clue_text)

        # Logika Tombol Kirim Tebakan
        if kirim_btn:
            st.session_state.attempts += 1
            
            if tebakan == st.session_state.target:
                st.session_state.win = True
                st.session_state.message = ""
                st.balloons()
            elif tebakan < st.session_state.target:
                st.session_state.lives -= 1
                st.session_state.message = f"💡 Tebakanmu (*{tebakan}) terlalu **KECIL*! Cari angka yang lebih besar."
            else:
                st.session_state.lives -= 1
                st.session_state.message = f"💡 Tebakanmu (*{tebakan}) terlalu **BESAR*! Cari angka yang lebih kecil."
                
            if st.session_state.lives <= 0:
                st.session_state.game_over = True
            
            st.rerun()

        # Tampilkan Pesan Hasil Tebakan Terakhir
        if st.session_state.message:
            st.warning(st.session_state.message)

    # Kondisi Menang
    if st.session_state.win:
        st.success(f"🎉 *LUAR BIASA! Kamu Menang!* Angka rahasianya adalah *{st.session_state.target}*.")
        st.info(f"Kamu berhasil menebaknya dalam {st.session_state.attempts} kali percobaan.")
        if st.button("Main Lagi 🔄"):
            del st.session_state.target
            st.rerun()

    # Kondisi Kalah (Game Over)
    if st.session_state.game_over:
        st.error(f"💀 *GAME OVER!* Nyawamu habis. Angka rahasia yang benar adalah *{st.session_state.target}*.")
        if st.button("Coba Lagi 🔄"):
            del st.session_state.target
            st.rerun()

    # Tombol Reset Manual
    st.write("")
    if st.button("🔄 Reset / Ganti Angka Baru"):
        del st.session_state.target
        st.rerun()


# HALAMAN 2: FORMULIR KRITIK & PESAN (Terhubung Google Sheets)

elif menu == "Kritik & Pesan":
    st.title("📝 Halaman Kritik & Pesan")
    st.write("Silakan isi formulir di bawah ini, data akan langsung masuk ke Google Sheets secara permanen.")
    st.write("---")
    
    with st.form("form_kritik_pesan"):
        nama = st.text_input("Nama Lengkap")
        no_hp = st.text_input("No HP / WhatsApp")
        pesan = st.text_area("Pesan / Kritik & Saran")
        
        submitted = st.form_submit_button("Kirim Pesan 🚀")
        
        if submitted:
            if not nama.strip():
                st.error("Nama wajib diisi!")
            elif not no_hp.strip():
                st.error("No HP wajib diisi!")
            elif not pesan.strip():
                st.error("Pesan tidak boleh kosong!")
            else:
                waktu_kirim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                payload = {
                    "waktu": waktu_kirim,
                    "nama": nama,
                    "no_hp": no_hp,
                    "pesan": pesan
                }
                
                try:
                    response = requests.post(WEB_APP_URL, json=payload)
                    if response.status_code == 200:
                        st.success("✅ Terima kasih! Data Anda berhasil masuk ke Google Sheets.")
                        st.balloons()
                    else:
                        st.error("❌ Gagal mengirim data ke server.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
