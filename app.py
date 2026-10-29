import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title='What-if Simulator Konten', layout='wide')

@st.cache_resource
def muat():
    return joblib.load('app_artifacts.pkl')

A = muat()
model = A['model']
HARI = {'Senin': 'Monday', 'Selasa': 'Tuesday', 'Rabu': 'Wednesday', 'Kamis': 'Thursday',
        'Jumat': 'Friday', 'Sabtu': 'Saturday', 'Minggu': 'Sunday'}
Q = A['kuartil']

def kategori(x):
    if x < Q['Q1']: return 'Low Engagement'
    if x < Q['Q2']: return 'Standard'
    if x < Q['Q3']: return 'High Performance'
    return 'Potential Viral'

def tampil_kategori(wadah, x):
    k = kategori(x)
    if k == 'Low Engagement':
        wadah.error(f'Kategori: {k}')
    elif k == 'Standard':
        wadah.info(f'Kategori: {k}')
    elif k == 'High Performance':
        wadah.success(f'Kategori: {k}')
    else:
        wadah.success(f'🔥 Kategori: {k}')

def prediksi(s):
    est = max(0.0, float(model.predict(pd.DataFrame([s])[A['fitur']])[0]))
    return {'est': est, 'lo': max(0.0, est - A['mae']), 'hi': est + A['mae']}

def idx(daftar, nilai):
    return daftar.index(nilai) if nilai in daftar else 0

def form(k):
    d, o, r = A['default'], A['opsi'], A['rentang']
    fmt = st.selectbox('Format konten', o['Content_Format'],
                       index=idx(o['Content_Format'], d['Content_Format']), key=f'fmt_{k}')
    tipe = st.selectbox('Tipe konten', o['Content_Type'],
                        index=idx(o['Content_Type'], d['Content_Type']), key=f'tipe_{k}')
    topik = st.selectbox('Topik', o['Topik'],
                         index=idx(o['Topik'], d['Topik']), key=f'topik_{k}')
    hari = st.selectbox('Hari posting', list(HARI), index=2, key=f'hari_{k}')
    slot_post = st.selectbox('Waktu posting', o['Time_Slot'],
                             index=idx(o['Time_Slot'], d['Time_Slot']), key=f'slot_{k}')
    st.caption('Pagi < 11.00 | Siang 11.00-14.59 | Sore 15.00-17.59 | Malam ≥ 18.00')
    kata = st.slider('Jumlah kata caption', r['Caption_Word_Count'][0], r['Caption_Word_Count'][1],
                     d['Caption_Word_Count'], key=f'kata_{k}')
    tag = st.slider('Jumlah hashtag', r['Hashtag_Count'][0], r['Hashtag_Count'][1],
                    d['Hashtag_Count'], key=f'tag_{k}')
    return {'Content_Format': fmt, 'Content_Type': tipe, 'Topik': topik,
            'Time_Slot': slot_post, 'Day_Name': HARI[hari],
            'Caption_Word_Count': kata, 'Hashtag_Count': tag}

st.title('What-if Simulator: Estimasi Engagement Konten')
m = A['metrik']
st.info(f"Model XGBoost ini dilatih dari {A['n_data']} postingan dan merupakan versi awal (baseline model). "
        f"Pada {m['n_test']} postingan uji, model mencapai R² {m['R2_test']:.2f}, jauh di atas tebakan "
        f"sederhana (R² {m['R2_baseline']:.2f}). Dengan data postingan yang lebih banyak, tingkat "
        f"kepercayaan model akan semakin tinggi. Gunakan hasil sebagai rentang kemungkinan, bukan angka pasti.")

ca, cb = st.columns(2)
with ca:
    st.subheader('Skenario A (dasar)')
    sa = form('a')
with cb:
    st.subheader('Skenario B (diubah)')
    sb = form('b')

ra, rb = prediksi(sa), prediksi(sb)
delta = (rb['est'] / max(ra['est'], 1) - 1) * 100
tumpang = not (rb['lo'] > ra['hi'] or ra['lo'] > rb['hi'])

st.divider()
ma, mb = st.columns(2)
with ma:
    st.metric('Estimasi engagement A', f"{ra['est']:,.0f}")
    st.caption(f"Rentang perkiraan: {ra['lo']:,.0f} - {ra['hi']:,.0f}")
    tampil_kategori(st, ra['est'])
with mb:
    st.metric('Estimasi engagement B', f"{rb['est']:,.0f}", delta=f'{delta:+.1f}%')
    st.caption(f"Rentang perkiraan: {rb['lo']:,.0f} - {rb['hi']:,.0f}")
    tampil_kategori(st, rb['est'])

if tumpang:
    st.warning('Rentang A dan B saling tumpang tindih: selisih ini masih dalam batas ketidakpastian model.')
else:
    st.success('Rentang A dan B tidak tumpang tindih: selisihnya relatif lebih meyakinkan.')

# ---------- Tips Konten Berpeluang Viral ----------
V = A['viral']
st.divider()
st.header('Tips Konten Berpeluang Viral')
st.caption(f"Viral = masuk 10% engagement tertinggi (≥ {V['batas']:,.0f} interaksi): "
           f"{V['n_viral']} dari {V['n_total']} postingan. Peluang rata-rata 10%. "
           f"Pola ini akan makin tajam seiring bertambahnya data.")

kolom = st.columns(len(V['ringkas']))
for c, r in zip(kolom, V['ringkas'].itertuples()):
    c.metric(r.Aspek, r.Terbaik)
    c.caption(f"{r.Persen_Viral:.0f}% postingannya viral (dari {r.Jumlah} postingan)")

unggul = V['ringkas'][V['ringkas']['Persen_Viral'] > 10]
if len(unggul):
    st.success('Paling sering muncul di konten viral: ' +
               ', '.join(f"{r.Aspek.lower()} {r.Terbaik}" for r in unggul.itertuples()) + '.')
else:
    st.info('Belum ada atribut yang jelas menonjol di data ini.')

with st.expander('Lihat detail per atribut'):
    atribut = st.selectbox('Atribut', V['profil']['Atribut'].unique().tolist())
    tabel = V['profil'][V['profil']['Atribut'] == atribut].drop(columns='Atribut')
    st.dataframe(tabel, use_container_width=True, hide_index=True)
