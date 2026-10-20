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
    page_title="Aplikasi Multi-Halaman Interaktif",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# MENAMBAHKAN LATAR BELAKANG & ANIMASI CSS KUSTOM
# =========================================================
background_image_path = "background.jpg"

def apply_custom_style(image_file):
    bg_css = ""
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        bg_css = f"""
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url("data:image/jpg;base64,{encoded_string.decode()}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
    except FileNotFoundError:
        bg_css = f"""
        @keyframes gradientBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .stApp {{
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            background-attachment: fixed;
        }}
        """

    st.markdown(
    f"""
    <style>
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    {bg_css}

    /* Membuat semua judul (h1 / st.title) berada di tengah */
    .block-container h1 {{
        text-align: center;
    }}

    /* Animasi muncul otomatis setiap kali berpindah halaman */
    .block-container {{
        animation: fadeIn 0.7s ease-out;
        background-color: rgba(255, 255, 255, 0.94);
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    }}

    .stButton > button {{
        transition: all 0.3s ease-in-out;
        border-radius: 8px;
        font-weight: bold;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.25);
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

apply_custom_style(background_image_path)

# =========================================================
# KONFIGURASI GOOGLE APPS SCRIPT WEB APP URL
# =========================================================
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyyO_Vnj3f6_Qtq7v32tJewxbTH77ZMQUwHAHZfQbAE1IwCwPuOZU42uqc_kErDgOKA/exec"

# =========================================================
# INISIALISASI NAVIGASI HALAMAN (SESSION STATE)
# =========================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Lobby Utama"

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# =========================================================
# HALAMAN 1: LOBBY UTAMA
# =========================================================
if st.session_state.current_page == "Lobby Utama":
    st.title("🌟 Selamat Datang di Lobby Utama!")
    st.write("Jelajahi fitur interaktif aplikasi kami melalui tombol di bawah ini:")
    st.write("---")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        if st.button("🎮 Masuk ke Mini Game", use_container_width=True):
            navigate_to("Mini Game Seru")
    with col_l2:
        if st.button("📝 Masuk ke Kritik & Pesan", use_container_width=True):
            navigate_to("Kritik & Pesan")

# =========================================================
# HALAMAN 2: MINI GAME SERU
# =========================================================
elif st.session_state.current_page == "Mini Game Seru":
    if st.button("⬅️ Kembali ke Lobby"):
        navigate_to("Lobby Utama")
        
    st.title("🎮 Arcade: Tebak Angka Misterius")
    st.write("Uji keberuntungan dan logika-mu! Temukan angka rahasia sebelum nyawamu habis.")
    st.write("---")

    level = st.selectbox("Pilih Level Kesulitan:", ["Mudah (1 - 50)", "Sedang (1 - 100)", "Sulit (1 - 200)"])
    max_val = 50 if "Mudah" in level else (100 if "Sedang" in level else 200)

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

        if clue_btn:
            if not st.session_state.clue_used:
                st.session_state.clue_used = True
                sifat = "Genap" if st.session_state.target % 2 == 0 else "Ganjil"
                kelipatan_5 = "Ya" if st.session_state.target % 5 == 0 else "Tidak"
                st.session_state.clue_text = f"💡 **CLUE:** Angka rahasia berstatus **{sifat}** dan kelipatan 5 adalah **{kelipatan_5}**!"
            else:
                st.session_state.clue_text = "⚠️ Clue sudah digunakan untuk ronde ini!"

        if st.session_state.clue_text:
            st.info(st.session_state.clue_text)

        if kirim_btn:
            st.session_state.attempts += 1
            
            if tebakan == st.session_state.target:
                st.session_state.win = True
                st.session_state.message = ""
                st.balloons()
            elif tebakan < st.session_state.target:
                st.session_state.lives -= 1
                st.session_state.message = f"💡 Tebakanmu (**{tebakan}**) terlalu **KECIL**! Cari angka yang lebih besar."
            else:
                st.session_state.lives -= 1
                st.session_state.message = f"💡 Tebakanmu (**{tebakan}**) terlalu **BESAR**! Cari angka yang lebih kecil."
                
            if st.session_state.lives <= 0:
                st.session_state.game_over = True
            
            st.rerun()

        if st.session_state.message:
            st.warning(st.session_state.message)

    if st.session_state.win:
        st.success(f"🎉 **LUAR BIASA! Kamu Menang!** Angka rahasianya adalah **{st.session_state.target}**.")
        st.info(f"Kamu berhasil menebaknya dalam {st.session_state.attempts} kali percobaan.")
        if st.button("Main Lagi 🔄"):
            del st.session_state.target
            st.rerun()

    if st.session_state.game_over:
        st.error(f"💀 **GAME OVER!** Nyawamu habis. Angka rahasia yang benar adalah **{st.session_state.target}**.")
        if st.button("Coba Lagi 🔄"):
            del st.session_state.target
            st.rerun()

    st.write("")
    if st.button("🔄 Reset / Ganti Angka Baru"):
        del st.session_state.target
        st.rerun()

# =========================================================
# HALAMAN 3: KRITIK & PESAN
# =========================================================
elif st.session_state.current_page == "Kritik & Pesan":
    if st.button("⬅️ Kembali ke Lobby"):
        navigate_to("Lobby Utama")
        
    st.title("📝 Halaman Kritik & Pesan")
    st.write("Silakan isi pesan di bawah ini. Kolom Nama dan No HP bersifat opsional (boleh dikosongkan).")
    st.write("---")
    
    if "form_submitted_success" not in st.session_state:
        st.session_state.form_submitted_success = False

    if st.session_state.form_submitted_success:
        st.success("✅ Terima kasih! Data Anda berhasil masuk ke Google Sheets.")
        st.balloons()
        st.write("")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("🔄 Kirim Pesan Lain"):
                st.session_state.form_submitted_success = False
                st.rerun()
        with col_f2:
            if st.button("🏠 Kembali ke Lobby"):
                st.session_state.form_submitted_success = False
                navigate_to("Lobby Utama")
            
    else:
        with st.form("form_kritik_pesan"):
            nama = st.text_input("Nama Lengkap (Opsional)")
            no_hp = st.text_input("No HP / WhatsApp (Opsional)")
            pesan = st.text_area("Pesan / Kritik & Saran (Wajib Diisi)")
            
            submitted = st.form_submit_button("Kirim Pesan 🚀")
            
            if submitted:
                if not pesan.strip():
                    st.error("Pesan wajib diisi!")
                else:
                    final_nama = nama.strip() if nama.strip() else "Anonim"
                    final_no_hp = no_hp.strip() if no_hp.strip() else "-"
                    
                    waktu_kirim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    payload = {
                        "waktu": waktu_kirim,
                        "nama": final_nama,
                        "no_hp": final_no_hp,
                        "pesan": pesan
                    }
                    
                    try:
                        response = requests.post(WEB_APP_URL, json=payload)
                        if response.status_code == 200:
                            st.session_state.form_submitted_success = True
                            st.rerun()
                        else:
                            st.error("❌ Gagal mengirim data ke server.")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
