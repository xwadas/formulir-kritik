import streamlit as st
import datetime
import pandas as pd
import os

# Konfigurasi halaman web
st.set_page_config(
    page_title="Formulir Kritik dan Pesan",
    page_icon="📝",
    layout="centered"
)

# Nama file Excel untuk menyimpan data
EXCEL_FILE = "data_kritik_pesan.xlsx"

# Fungsi untuk menyimpan data ke file Excel
def simpan_ke_excel(waktu, nama, email, kategori, pesan):
    data_baru = {
        "Waktu": [waktu],
        "Nama": [nama if nama else "Anonim"],
        "Email": [email if email else "-"],
        "Kategori": [kategori],
        "Pesan": [pesan]
    }
    df_baru = pd.DataFrame(data_baru)
    
    # Jika file sudah ada, append (tambahkan) data baru ke bawahnya
    if os.path.exists(EXCEL_FILE):
        df_lama = pd.read_excel(EXCEL_FILE)
        df_gabungan = pd.concat([df_lama, df_baru], ignore_index=True)
        df_gabungan.to_excel(EXCEL_FILE, index=False)
    else:
        # Jika file belum ada, buat file baru
        df_baru.to_excel(EXCEL_FILE, index=False)

# Judul dan Deskripsi Form
st.title("📬 Kotak Kritik dan Pesan")
st.markdown("Silakan isi formulir di bawah ini untuk menyampaikan kritik, saran, atau pesan Anda.")

st.markdown("---")

# Membuat Form menggunakan st.form
with st.form("kritik_form"):
    # Input Nama
    nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama Anda...")
    
    # Input Email
    email = st.text_input("Email", placeholder="contoh@email.com...")
    
    # Kategori Pesan dengan opsi placeholder di awal
    kategori = st.selectbox(
        "Kategori Pesan",
        ["Pilih Kategori...", "Kritik", "Saran", "Pertanyaan", "Pujian", "Lainnya"]
    )
    
    # Input Pesan dan Kritik
    pesan = st.text_area(
        "Pesan / Kritik / Saran", 
        placeholder="Tuliskan pesan atau kritik Anda secara detail di sini..."
    )
    
    # Tombol Kirim
    submit_button = st.form_submit_button(label="Kirim Pesan")

# Logika ketika tombol kirim ditekan
if submit_button:
    if pesan.strip() == "":
        st.warning("⚠️ Mohon isi bagian pesan atau kritik Anda sebelum mengirimkan.")
    elif kategori == "Pilih Kategori...":
        st.warning("⚠️ Mohon pilih kategori pesan terlebih dahulu.")
    else:
        # Waktu pengiriman
        waktu_kirim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simpan ke file Excel
        simpan_ke_excel(waktu_kirim, nama, email, kategori, pesan)
        
        # Menampilkan pesan sukses
        st.success("✅ Terima kasih! Pesan dan kritik Anda berhasil dikirim dan tersimpan.")