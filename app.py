import joblib
import numpy as np
import pandas as pd
import base64
import streamlit as st

# ---------- Pengaturan halaman ----------
st.set_page_config(
    page_title="Bank Sampah Digital | Cek Potensi Konten",
    page_icon="♻️",
    layout="wide",
)

# Warna sesuai logo & website Bank Sampah Digital
HIJAU_TUA = "#2E8B0A"
HIJAU_GELAP = "#0A7A00"
HIJAU_MUDA = "#8DB821"
MINT = "#EEF7E6"
KUNING = "#F5C242"

# ---------- Navigasi sederhana ----------
if "halaman" not in st.session_state:
    st.session_state.halaman = "beranda"


def pindah(nama_halaman):
    st.session_state.halaman = nama_halaman


# ---------- Gaya tampilan (CSS) ----------
st.markdown(f"""
<style>
.block-container {{ padding-top: 2rem; padding-left: 4rem; padding-right: 4rem; max-width: 1500px; }}
.hero {{
    background: linear-gradient(135deg, {HIJAU_GELAP} 0%, {HIJAU_TUA} 55%, {HIJAU_MUDA} 100%);
    border-radius: 24px; padding: 36px 40px; color: white;
    display: flex; align-items: center; gap: 32px; flex-wrap: wrap;
}}
.hero .logo-box {{
    background: white; border-radius: 18px; padding: 14px 20px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}}
.hero .logo-box img {{ height: 70px; }}
.hero h1 {{ color: white; font-size: 2.2rem; margin: 0 0 8px 0; line-height: 1.2; }}
.hero p {{ color: #F2FAE9; font-size: 1.05rem; margin: 0; }}
.hero .tag {{
    display: inline-block; background: {KUNING}; color: #3b2f00;
    padding: 4px 14px; border-radius: 999px; font-weight: 700;
    font-size: 0.85rem; margin-bottom: 12px;
}}
.stat {{
    background: {MINT}; border-radius: 18px; padding: 18px; text-align: center;
    border: 1px solid #D9EBC8;
}}
.stat .angka {{ font-size: 2rem; font-weight: 800; color: {HIJAU_TUA}; }}
.stat .label {{ color: #3E5636; font-size: 0.9rem; }}
.judul-seksi {{ color: {HIJAU_TUA}; font-weight: 800; font-size: 1.5rem; margin: 28px 0 6px 0; }}
.sub-seksi {{ color: #5b6b54; margin-bottom: 14px; }}
.kartu {{
    background: white; border: 1px solid #D9EBC8; border-left: 6px solid {HIJAU_MUDA};
    border-radius: 16px; padding: 18px 20px; margin-bottom: 14px; min-height: 210px;
    box-shadow: 0 2px 8px rgba(46,139,10,0.06);
    transition: transform .2s ease, box-shadow .2s ease;
}}
.kartu:hover {{ transform: translateY(-4px); box-shadow: 0 10px 20px rgba(46,139,10,0.18); }}
.kartu .ikon {{ font-size: 1.8rem; }}
.kartu h4 {{ margin: 6px 0 6px 0; color: {HIJAU_GELAP}; }}
.kartu p {{ margin: 0; color: #3E4A39; font-size: 0.95rem; }}
.disclaimer {{
    background: #FFF8E1; border: 1px solid {KUNING}; border-radius: 14px;
    padding: 14px 18px; color: #5a4600; font-size: 0.93rem; margin-top: 18px;
}}
.bar-luar {{ background: #E6EFDD; border-radius: 999px; height: 22px; overflow: hidden; }}
.bar-isi {{ background: linear-gradient(90deg, {HIJAU_MUDA}, {HIJAU_TUA}); height: 100%; border-radius: 999px; }}
.hasil {{
    border-radius: 20px; padding: 24px; text-align: center; color: white;
    background: linear-gradient(135deg, {HIJAU_GELAP}, {HIJAU_TUA});
}}
.hasil .besar {{ font-size: 3rem; font-weight: 800; }}
.footer {{ text-align: center; color: #7a8a72; font-size: 0.85rem; margin-top: 36px; }}
div.stButton > button {{ border-radius: 999px; padding: 0.6rem 1.6rem; font-weight: 700; }}
.terbaik {{
    background: white; border: 1px solid #D9EBC8; border-top: 6px solid {HIJAU_MUDA};
    border-radius: 16px; padding: 16px 18px; min-height: 140px;
    box-shadow: 0 2px 8px rgba(46,139,10,0.06);
    transition: transform .2s ease, box-shadow .2s ease;
}}
.terbaik:hover {{ transform: translateY(-4px); box-shadow: 0 10px 20px rgba(46,139,10,0.18); }}
.terbaik .aspek {{ color: #5b6b54; font-size: 0.85rem; }}
.terbaik .nilai {{ color: {HIJAU_TUA}; font-size: 1.7rem; font-weight: 800; margin: 4px 0 8px 0; }}
.terbaik .ket {{ color: #3E4A39; font-size: 0.85rem; }}
</style>
""", unsafe_allow_html=True)


def logo_base64(path="Logo_Bank_Sampah_Digital.png"):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


DISCLAIMER = (
    "<b>Catatan:</b> Angka di sini adalah <b>perkiraan</b> berdasarkan 72 postingan "
    "Instagram Bank Sampah Digital tahun 2025, jadi bukan jaminan hasil. Makin banyak postingan yang "
    "kita catat, makin tepat perkiraannya. Anggap ini sebagai <b>panduan arah</b> "
    "untuk membantu memilih konten, lalu tetap uji langsung di lapangan."
)


# =====================================================================
# HALAMAN 1: BERANDA
# =====================================================================
def halaman_beranda():
    # --- Hero: logo + judul ---
    b64 = logo_base64()
    logo_html = (
        f'<div class="logo-box"><img src="data:image/png;base64,{b64}"></div>' if b64 else ""
    )
    st.markdown(
        f'<div class="hero">{logo_html}<div>'
        f'<span class="tag">#MulaiDariKita</span>'
        f'<h1>Cek Potensi Konten Instagram Sebelum Diposting</h1>'
        f'<p>Perkirakan seberapa menarik sebuah konten bagi audiens, lalu coba ubah tipe, '
        f'topik, atau waktu posting untuk melihat dampaknya.</p>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns([1.2, 1.2, 3])
    with c1:
        st.button("🚀 Mulai Prediksi", type="primary", on_click=pindah, args=("prediksi",))
    with c2:
        st.link_button("🌐 Website Bank Sampah Digital", "https://banksampahdigital.com/")

    # --- Angka ringkas ---
    s1, s2, s3 = st.columns(3)
    s1.markdown('<div class="stat"><div class="angka">72</div><div class="label">postingan dipelajari (2025)</div></div>', unsafe_allow_html=True)
    s2.markdown('<div class="stat"><div class="angka">8</div><div class="label">postingan masuk kategori viral (10% teratas)</div></div>', unsafe_allow_html=True)
    s3.markdown('<div class="stat"><div class="angka">4</div><div class="label">aspek konten dibandingkan: tipe, format, waktu, dan topik</div></div>', unsafe_allow_html=True)

    # --- Tips konten berpeluang viral (isi dari versi lama) ---
    st.markdown('<div class="judul-seksi">🏆 Tips Konten Berpeluang Viral</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-seksi">Viral = masuk 10% engagement tertinggi (≥ 205 interaksi): 8 dari 72 postingan. '
        'Peluang rata-rata 10%. Datanya sedikit, jadi ini pola, bukan jaminan.</div>',
        unsafe_allow_html=True,
    )
    terbaik = [
        ("Tipe konten", "Kolaborasi", 29, 14),
        ("Format", "Feed", 13, 38),
        ("Waktu posting", "Siang", 12, 48),
        ("Topik", "Bank Sampah", 12, 32),
    ]
    kolom_terbaik = st.columns(4)
    for kolom, (aspek, nilai, persen, n) in zip(kolom_terbaik, terbaik):
        kolom.markdown(
            f'<div class="terbaik"><div class="aspek">{aspek}</div>'
            f'<div class="nilai">{nilai}</div>'
            f'<div class="ket">{persen}% postingannya viral (dari {n} postingan)</div></div>',
            unsafe_allow_html=True,
        )

    # --- Tips viral ---
    st.markdown('<div class="judul-seksi">💡 Saran Praktis untuk Tim Media</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-seksi">Dirangkum dari pola postingan Bank Sampah Digital yang paling banyak mendapat respons.</div>', unsafe_allow_html=True)

    tips = [
        ("🤝", "Ajak berkolaborasi", "Konten kolaborasi dengan mitra, komunitas, sekolah, atau nasabah paling sering menjadi viral."),
        ("📣", "Beri ajakan yang jelas", "Konten dengan ajakan (setor sampah, daftar, ikut program) mendapat respons lebih tinggi dari konten informasi biasa."),
        ("🎯", "Isi lebih penting dari format", "Feed, Reels, atau Carousel hasilnya mirip. Fokuskan tenaga pada topik dan pesan yang menarik."),
        ("♻️", "Coba seri Daur Ulang", "Topik daur ulang tampak menjanjikan, tapi datanya baru sedikit. Layak diuji 3 sampai 5 postingan."),
    ]
    kol = st.columns(4)
    for i, (ikon, judul, isi) in enumerate(tips):
        kol[i].markdown(
            f'<div class="kartu"><div class="ikon">{ikon}</div><h4>{judul}</h4><p>{isi}</p></div>',
            unsafe_allow_html=True,
        )

    # --- Cek cepat interaktif (dari data nyata, bukan model) ---
    st.markdown('<div class="judul-seksi">🔎 Cek Cepat: Peluang Viral per Tipe Konten</div>', unsafe_allow_html=True)
    data_viral = {
        "Kolaborasi": (29, 14),
        "Edukasi": (13, 15),
        "Call-to-Action": (12, 8),
        "Informasi": (0, 13),
        "Hari Besar": (0, 10),
        "Dokumentasi Kegiatan": (0, 5),
    }
    pilihan = st.selectbox("Pilih tipe konten:", list(data_viral.keys()))
    persen, jumlah = data_viral[pilihan]
    st.markdown(
        f'<div class="bar-luar"><div class="bar-isi" style="width:{max(persen, 2)}%"></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**{persen}%** dari {jumlah} postingan tipe *{pilihan}* masuk kategori viral (10% teratas).")
    rata_rata = 8 / 72 * 100
    if persen > 0:
        st.markdown(f"Itu sekitar **{persen / rata_rata:.1f}x lebih sering viral** dibanding rata-rata semua postingan ({rata_rata:.0f}%).")
    else:
        st.markdown("Belum ada postingan tipe ini yang viral di data 2025.")
    # --- Disclaimer ---
    st.markdown(f'<div class="disclaimer">⚠️ {DISCLAIMER}</div>', unsafe_allow_html=True)

    st.write("")
    st.button("🚀 Coba Prediksi Konten Kamu", type="primary", on_click=pindah, args=("prediksi",), key="cta_bawah")
    st.markdown('<div class="footer">Dibuat oleh tim Final Project Intern Bank Sampah Digital · 2026</div>', unsafe_allow_html=True)


# =====================================================================
# HALAMAN 2: PREDIKSI
# =====================================================================
def kategori_hasil(estimasi):
    # Sesuaikan batas ini dengan fungsi kategori di kode lamamu
    if estimasi >= 86:
        return "🔥 Potensi Viral"
    if estimasi >= 47:
        return "⭐ Performa Tinggi"
    if estimasi >= 30:
        return "👍 Standar"
    return "📉 Perlu Ditingkatkan"


def halaman_prediksi():
    st.button("← Kembali ke Beranda", on_click=pindah, args=("beranda",))
    st.markdown('<div class="judul-seksi">🔮 Prediksi Performa Konten</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-seksi">Isi rencana konten kamu, lalu lihat perkiraannya. Coba ubah satu pilihan untuk melihat dampaknya.</div>', unsafe_allow_html=True)

    hari_map = {
        "Senin": "Monday", "Selasa": "Tuesday", "Rabu": "Wednesday", "Kamis": "Thursday",
        "Jumat": "Friday", "Sabtu": "Saturday", "Minggu": "Sunday",
    }

    kiri, kanan = st.columns(2)
    with kiri:
        st.markdown("##### Skenario A (rencana kamu)")
        fmt = st.selectbox("Format", ["Feed", "Reels", "Carousel"], key="a_fmt")
        tipe = st.selectbox("Tipe konten", ["Informasi", "Call-to-Action", "Edukasi", "Kolaborasi", "Hari Besar", "Dokumentasi Kegiatan", "Hiburan", "Testimoni"], key="a_tipe")
        topik = st.selectbox("Topik", ["Bank Sampah", "Lingkungan", "Sampah Plastik", "Sampah Organik", "Daur Ulang"], key="a_topik")
        slot = st.selectbox("Waktu posting", ["Pagi", "Siang", "Sore", "Malam"], index=1, key="a_slot")
        hari = st.selectbox("Hari posting", list(hari_map.keys()), key="a_hari")
        hashtag = st.slider("Jumlah hashtag", 0, 30, 10, key="a_hash")
        kata = st.slider("Panjang caption (jumlah kata)", 10, 180, 90, key="a_kata")
    with kanan:
        st.markdown("##### Skenario B (bandingkan, opsional)")
        fmt_b = st.selectbox("Format", ["Feed", "Reels", "Carousel"], key="b_fmt")
        tipe_b = st.selectbox("Tipe konten", ["Informasi", "Call-to-Action", "Edukasi", "Kolaborasi", "Hari Besar", "Dokumentasi Kegiatan", "Hiburan", "Testimoni"], index=3, key="b_tipe")
        topik_b = st.selectbox("Topik", ["Bank Sampah", "Lingkungan", "Sampah Plastik", "Sampah Organik", "Daur Ulang"], key="b_topik")
        slot_b = st.selectbox("Waktu posting", ["Pagi", "Siang", "Sore", "Malam"], index=1, key="b_slot")
        hari_b = st.selectbox("Hari posting", list(hari_map.keys()), key="b_hari")
        hashtag_b = st.slider("Jumlah hashtag", 0, 30, 10, key="b_hash")
        kata_b = st.slider("Panjang caption (jumlah kata)", 10, 180, 90, key="b_kata")

    if st.button("✨ Lihat Perkiraan", type="primary"):
        # ============================================================
        # TEMPEL LOGIKA PREDIKSI LAMAMU DI SINI
        # Isi 2 variabel ini untuk skenario A dan B:
        #   estimasi_a, bawah_a, atas_a
        #   estimasi_b, bawah_b, atas_b
        # Nilai input dari form: fmt, tipe, topik, slot, hari_map[hari], hashtag, kata
        # (dan versi _b untuk skenario B)
        # ============================================================
        estimasi_a, bawah_a, atas_a = 0, 0, 0   # <- ganti
        estimasi_b, bawah_b, atas_b = 0, 0, 0   # <- ganti

        h1, h2 = st.columns(2)
        for kolom, nama, est, bw, at in [
            (h1, "Skenario A", estimasi_a, bawah_a, atas_a),
            (h2, "Skenario B", estimasi_b, bawah_b, atas_b),
        ]:
            kolom.markdown(
                f'<div class="hasil"><div>{nama}</div>'
                f'<div class="besar">{est:,.0f}</div>'
                f'<div>perkiraan interaksi (like, komentar, share, save)</div>'
                f'<div style="margin-top:8px">Kisaran: {bw:,.0f} sampai {at:,.0f}</div>'
                f'<div style="margin-top:10px;font-weight:700">{kategori_hasil(est)}</div></div>',
                unsafe_allow_html=True,
            )

        if estimasi_a > 0:
            selisih = (estimasi_b - estimasi_a) / estimasi_a * 100
            arah = "lebih tinggi" if selisih >= 0 else "lebih rendah"
            st.info(f"Skenario B diperkirakan {abs(selisih):.0f}% {arah} dari Skenario A.")

    st.markdown(f'<div class="disclaimer">⚠️ {DISCLAIMER}</div>', unsafe_allow_html=True)


# ---------- Router ----------
if st.session_state.halaman == "beranda":
    halaman_beranda()
else:
    halaman_prediksi()
