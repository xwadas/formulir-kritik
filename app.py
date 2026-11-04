import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import requests
import random
import base64
from streamlit_qrcode_scanner import qrcode_scanner

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
# MENAMBAHKAN LATAR BELAKANG & CSS KUSTOM
# =========================================================
background_image_path = "background.jpg"

def apply_custom_style(image_file):
    bg_css = ""
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        bg_css = f"""
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("data:image/jpg;base64,{encoded_string.decode()}");
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
    /* --- EFEK TRANSISI PERPINDAHAN HALAMAN --- */
    @keyframes pageSlideIn {{
        0% {{
            opacity: 0;
            transform: translateY(35px) scale(0.97);
            filter: blur(4px);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0px);
        }}
    }}

    {bg_css}

    .block-container {{
        background: rgba(255, 255, 255, 0.22) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 18px;
        padding: 2.2rem;
        box-shadow: 0 10px 35px 0 rgba(0, 0, 0, 0.35);
        max-width: 96% !important;
        width: 96% !important;
        margin: 15px auto;
    }}

    /* Kelas animasi yang dipaksa aktif setiap elemen dimuat ulang */
    .transition-wrapper {{
        animation: pageSlideIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    /* Memperlebar komponen QR Scanner agar pas dan penuh di layar */
    iframe[title*="streamlit_qrcode_scanner"], 
    div[data-testid="stIframe"] {{
        width: 100% !important;
        max-width: 100% !important;
        border-radius: 12px;
    }}
    
    video {{
        width: 100% !important;
        height: auto !important;
        border-radius: 12px;
    }}

    /* Warna teks utama hitam */
    .block-container h1, 
    .block-container h2, 
    .block-container h3, 
    .block-container p, 
    .block-container span, 
    .block-container label,
    .block-container .stMarkdown,
    .block-container [data-testid="stMetricValue"],
    .block-container [data-testid="stMetricLabel"] {{
        color: #000000 !important;
        font-weight: 500;
    }}

    .block-container h1 {{
        text-align: center;
        font-size: 1.7rem;
        margin-bottom: 0.3rem;
    }}

    /* --- GAYA TOMBOL MODERN & ESTETIK --- */
    .stButton > button {{
        width: 100% !important;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.7rem 1rem;
        font-size: 1rem;
        background: linear-gradient(135deg, #1f1f1f 0%, #2d2d2d 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .stButton > button *, .stButton > button p {{
        color: #ffffff !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #2d2d2d 100%, #404040 0%) !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.4) !important;
    }}

    /* Input form agar lebih rapi */
    .stTextInput input, .stTextArea textarea {{
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.88) !important;
        color: #000000 !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

apply_custom_style(background_image_path)

# =========================================================
# KONFIGURASI GOOGLE APPS SCRIPT WEB APP URL
# =========================================================
WEB_APP_URL = "MASUKKAN_URL_WEB_APP_GOOGLE_SCRIPT_DISINI"

# =========================================================
# INISIALISASI NAVIGASI HALAMAN (SESSION STATE)
# =========================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Lobby Utama"

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# =========================================================
# KONTEN UTAMA DENGAN PEMBUNGKUS DINAMIS (MEMICU ANIMASI)
# =========================================================
# Menggunakan ID dinamis agar browser merender ulang elemen saat halaman berganti
st.markdown(f'<div class="transition-wrapper" id="page-{st.session_state.current_page}">', unsafe_allow_html=True)

if st.session_state.current_page == "Lobby Utama":
    st.title("🌟 Selamat Datang di Lobby Utama!")
    st.markdown("<p style='text-align: center; margin-bottom: 20px;'>Jelajahi fitur interaktif aplikasi kami melalui menu di bawah ini:</p>", unsafe_allow_html=True)
    st.write("---")
    
    if st.button("🎮 Mainkan Game Code Breaker", use_container_width=True):
        navigate_to("Code Breaker")
    
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    if st.button("📷 Masuk ke Menu Absensi QR", use_container_width=True):
        navigate_to("Absensi QR")

    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    if st.button("📝 Masuk ke Kritik & Pesan", use_container_width=True):
        navigate_to("Kritik & Pesan")

elif st.session_state.current_page == "Code Breaker":
    col_back, _ = st.columns([1.3, 2.7])
    with col_back:
        if st.button("⬅️ Kembali", use_container_width=True):
            navigate_to("Lobby Utama")
        
    st.title("🕵️‍♂️ Code Breaker")
    st.markdown("<p style='text-align: center;'>Pecahkan 3 digit angka rahasia unik (1-9) menggunakan strategi analisis petunjuk!</p>", unsafe_allow_html=True)
    st.write("---")

    if "cb_secret" not in st.session_state:
        digits = random.sample(range(1, 10), 3)
        st.session_state.cb_secret = "".join(map(str, digits))
        st.session_state.cb_attempts = 0
        st.session_state.cb_history = []
        st.session_state.cb_win = False

    if not st.session_state.cb_win:
        guess_input = st.text_input("Masukkan 3 digit angka unik (Contoh: 123):", max_chars=3)
        
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        if st.button("Analisis Tebakan 🔍", use_container_width=True):
            if len(guess_input) != 3 or not guess_input.isdigit() or len(set(guess_input)) != 3:
                st.error("⚠️ Masukkan tepat 3 digit angka berbeda (tanpa angka kembar)!")
            else:
                st.session_state.cb_attempts += 1
                secret = st.session_state.cb_secret
                
                bulls = sum(1 for a, b in zip(guess_input, secret) if a == b)
                cows = sum(1 for a in guess_input if a in secret) - bulls
                
                st.session_state.cb_history.append(f"Tebakan **{guess_input}** ➔ 🎯 Tepat Posisi: **{bulls}** | 🟡 Benar Posisi Salah: **{cows}**")
                
                if bulls == 3:
                    st.session_state.cb_win = True
                    st.balloons()
                st.rerun()

    if st.session_state.cb_history:
        st.markdown("### 📋 Riwayat Analisis Logika:")
        for h in reversed(st.session_state.cb_history):
            st.markdown(f"- {h}")

    if st.session_state.cb_win:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.success(f"🎉 **LUAR BIASA! Kamu Berhasil Memecahkan Kode!** Angka rahasianya adalah **{st.session_state.cb_secret}**.")
        st.info(f"Berhasil dipecahkan dalam {st.session_state.cb_attempts} kali percobaan analitik.")

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Reset / Kode Baru", use_container_width=True):
        del st.session_state.cb_secret
        st.rerun()

elif st.session_state.current_page == "Absensi QR":
    col_back, _ = st.columns([1.3, 2.7])
    with col_back:
        if st.button("⬅️ Kembali", use_container_width=True):
            navigate_to("Lobby Utama")
        
    st.title("📷 Menu Absensi QR")
    st.markdown("<p style='text-align: center;'>Arahkan kamera perangkat Anda ke QR Code. Data akan langsung terkirim secara otomatis.</p>", unsafe_allow_html=True)
    st.write("---")

    if "attendance_success" not in st.session_state:
        st.session_state.attendance_success = False
    if "last_scanned_qr" not in st.session_state:
        st.session_state.last_scanned_qr = None

    if st.session_state.attendance_success:
        st.success("🎉 Absensi Berhasil Tercatat!")
        st.info(f"Data QR Terakhir: **{st.session_state.last_scanned_qr}**")
        st.balloons()
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Baca QR Code Lagi", use_container_width=True):
            st.session_state.attendance_success = False
            st.session_state.last_scanned_qr = None
            st.rerun()
    else:
        qr_code = qrcode_scanner(key='qrcode_scanner')

        if qr_code:
            if qr_code != st.session_state.last_scanned_qr:
                st.session_state.last_scanned_qr = qr_code
                
                wib = timezone(timedelta(hours=7))
                waktu_absen = datetime.now(wib).strftime("%Y-%m-%d %H:%M:%S")
                
                payload = {
                    "tipe": "absensi",
                    "waktu": waktu_absen,
                    "data_qr": qr_code
                }
                
                try:
                    with st.spinner(f"⏳ Mengirim absensi untuk **{qr_code}** ke server..."):
                        response = requests.post(WEB_APP_URL, json=payload)
                        
                    if response.status_code == 200:
                        st.session_state.attendance_success = True
                        st.rerun()
                    else:
                        st.error("❌ Gagal mengirim absensi ke server.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan koneksi: {e}")

elif st.session_state.current_page == "Kritik & Pesan":
    col_back, _ = st.columns([1.3, 2.7])
    with col_back:
        if st.button("⬅️ Kembali", use_container_width=True):
            navigate_to("Lobby Utama")
        
    st.title("📝 Halaman Kritik & Pesan")
    st.markdown("<p style='text-align: center;'>Silakan isi pesan di bawah ini. Kolom Nama dan No HP bersifat opsional.</p>", unsafe_allow_html=True)
    st.write("---")
    
    if "form_submitted_success" not in st.session_state:
        st.session_state.form_submitted_success = False

    if st.session_state.form_submitted_success:
        st.success("✅ Terima kasih! Data Anda berhasil masuk ke Google Sheets.")
        st.balloons()
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Kirim Pesan Lain", use_container_width=True):
            st.session_state.form_submitted_success = False
            st.rerun()
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🏠 Kembali ke Lobby", use_container_width=True):
            st.session_state.form_submitted_success = False
            navigate_to("Lobby Utama")
            
    else:
        with st.form("form_kritik_pesan"):
            nama = st.text_input("Nama Lengkap (Opsional)")
            no_hp = st.text_input("No HP / WhatsApp (Opsional)")
            pesan = st.text_area("Pesan / Kritik & Saran (Wajib Diisi)")
            
            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Kirim Pesan 🚀", use_container_width=True)
            
            if submitted:
                if not pesan.strip():
                    st.error("Pesan wajib diisi!")
                else:
                    final_nama = nama.strip() if nama.strip() else "Anonim"
                    final_no_hp = no_hp.strip() if no_hp.strip() else "-"
                    
                    wib = timezone(timedelta(hours=7))
                    waktu_kirim = datetime.now(wib).strftime("%Y-%m-%d %H:%M:%S")
                    
                    payload = {
                        "tipe": "kritik_pesan",
                        "waktu": waktu_kirim,
                        "nama": final_nama,
                        "no_hp": final_no_hp,
                        "pesan": pesan
                    }
                    
                    try:
                        with st.spinner("⏳ Mengirim pesan ke server, mohon tunggu..."):
                            response = requests.post(WEB_APP_URL, json=payload)
                            
                        if response.status_code == 200:
                            st.session_state.form_submitted_success = True
                            st.rerun()
                        else:
                            st.error("❌ Gagal mengirim data ke server.")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")

st.markdown('</div>', unsafe_allow_html=True)
