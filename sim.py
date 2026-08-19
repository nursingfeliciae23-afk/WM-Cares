import streamlit as st
import pandas as pd
import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RS Widya Mandala - SimKep Integrated", layout="wide", page_icon="🏥")

# --- SYSTEM LOGIN AUTHENTICATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Login Sistem - RS Widya Mandala")
    st.subheader("Sistem Integrasi Terpadu Ruang Anyelir")
    
    col_login, _ = st.columns([1, 1])
    with col_login:
        with st.form("form_login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Masuk Sistem")
            
            if submit_login:
                if (username in ["admin", "perawat"]) and (password in ["admin123", "anyelir123"]):
                    st.session_state.authenticated = True
                    st.success("Login Berhasil! Memuat sistem...")
                    st.rerun()
                else:
                    st.error("Username atau Password tidak valid!")
    st.info("💡 **Petunjuk Akses:** Gunakan Username: `admin` & Password: `admin123`")
    st.stop()

# --- INISIALISASI DATABASE TERINTEGRASI ---
def init_session_states():
    if 'data_perawat' not in st.session_state:
        st.session_state.data_perawat = [
            {"NIP": "P001", "Nama": "Ns. Hendra, S.Kep", "Peran": "Kepala Ruangan (KARU)", "Kualifikasi": "S1 Ners", "Shift": "Pagi"},
            {"NIP": "P002", "Nama": "Ns. Ahmad Fauzi, S.Kep", "Peran": "Perawat Primer 1 (PP1)", "Kualifikasi": "S1 Ners", "Shift": "Pagi"},
            {"NIP": "P003", "Nama": "Ns. Dewi Ratna, S.Kep", "Peran": "Perawat Primer 2 (PP2)", "Kualifikasi": "S1 Ners", "Shift": "Sore"},
            {"NIP": "P004", "Nama": "Budi Santoso, AMK", "Peran": "Perawat Asosiet (PA)", "Kualifikasi": "D3 Keperawatan", "Shift": "Pagi"},
            {"NIP": "P005", "Nama": "Siti Aminah, AMK", "Peran": "Perawat Asosiet (PA)", "Kualifikasi": "D3 Keperawatan", "Shift": "Pagi"},
            {"NIP": "P006", "Nama": "Ns. Rina Astuti, S.Kep", "Peran": "Perawat Asosiet (PA)", "Kualifikasi": "S1 Ners", "Shift": "Sore"},
            {"NIP": "P007", "Nama": "Eko Prasetyo, AMK", "Peran": "Perawat Asosiet (PA)", "Kualifikasi": "D3 Keperawatan", "Shift": "Sore"},
            {"NIP": "P008", "Nama": "Ns. Grace Maria, S.Kep", "Peran": "Perawat Asosiet (PA)", "Kualifikasi": "S1 Ners", "Shift": "Malam"},
            {"NIP": "P009", "Nama": "Indah Permata, AMK", "Peran": "Perawat Asosiet (PA)", "Kualifikasi": "D3 Keperawatan", "Shift": "Malam"},
            {"NIP": "P010", "Nama": "Farhan Abdullah, AMK", "Peran": "Perawat Asosiet (PA)", "Kualifikasi": "D3 Keperawatan", "Shift": "Lepas/Libur"}
        ]

    if 'daftar_dpjp' not in st.session_state:
        st.session_state.daftar_dpjp = [
            "dr. Agus Prasetyo, Sp.PD",
            "dr. Ratna Juwita, Sp.JP",
            "dr. Hendro Satrio, Sp.S",
            "dr. Maya Indriani, Sp.A",
            "dr. Bambang Utama, Sp.B"
        ]

    if 'data_pasien' not in st.session_state:
        st.session_state.data_pasien = [
            {"No_RM": "RM-101", "Nama": "Tn. Bambang S.", "Kamar": "Anyelir 01/A", "DPJP": "dr. Agus Prasetyo, Sp.PD", "Ketergantungan": "Partial Care", "PPJA": "Ns. Ahmad Fauzi, S.Kep", "Diagnosis": "DM Tipe 2 + Gangren", "Status": "Rawat Inap", "Tgl_Masuk": "15/08/2026 09:00", "TTD_Perawat": "Ns. Ahmad"},
            {"No_RM": "RM-102", "Nama": "Ny. Siti Rahma", "Kamar": "Anyelir 01/B", "DPJP": "dr. Ratna Juwita, Sp.JP", "Ketergantungan": "Total Care", "PPJA": "Ns. Ahmad Fauzi, S.Kep", "Diagnosis": "CHF Stage III", "Status": "Rawat Inap", "Tgl_Masuk": "16/08/2026 11:30", "TTD_Perawat": "Ns. Ahmad"},
            {"No_RM": "RM-103", "Nama": "Tn. Kuncoro", "Kamar": "Anyelir 02/A", "DPJP": "dr. Hendro Satrio, Sp.S", "Ketergantungan": "Total Care", "PPJA": "Ns. Dewi Ratna, S.Kep", "Diagnosis": "Stroke Infark", "Status": "Rawat Inap", "Tgl_Masuk": "17/08/2026 14:15", "TTD_Perawat": "Ns. Dewi"},
            {"No_RM": "RM-104", "Nama": "An. Rizky", "Kamar": "Anyelir 03/A", "DPJP": "dr. Maya Indriani, Sp.A", "Ketergantungan": "Minimal Care", "PPJA": "Ns. Dewi Ratna, S.Kep", "Diagnosis": "DHF Grade II", "Status": "Rawat Inap", "Tgl_Masuk": "18/08/2026 08:20", "TTD_Perawat": "Ns. Dewi"},
            {"No_RM": "RM-105", "Nama": "Ny. Hj. Maryam", "Kamar": "Anyelir 04/B", "DPJP": "dr. Bambang Utama, Sp.B", "Ketergantungan": "Partial Care", "PPJA": "Ns. Ahmad Fauzi, S.Kep", "Diagnosis": "Post Op Laparotomi H-2", "Status": "Rawat Inap", "Tgl_Masuk": "18/08/2026 16:45", "TTD_Perawat": "Ns. Ahmad"}
        ]
    else:
        # AUTO-REPAIR: Tambahkan key 'DPJP' jika ada data lama yang belum memilikinya
        for p in st.session_state.data_pasien:
            if 'DPJP' not in p:
                p['DPJP'] = "dr. Agus Prasetyo, Sp.PD"

    if 'params_mutu' not in st.session_state:
        st.session_state.params_mutu = {
            "total_tt": 15,
            "periode_hari": 30,
            "hari_perawatan": 353,
            "pasien_keluar": 78,
            "kepuasan": 94.2,
            "perawat_on_duty": 6
        }

    if 'data_inventaris' not in st.session_state:
        st.session_state.data_inventaris = [
            {"Kode": "INV-01", "Barang": "Emergency Trolley Lengkap", "Jumlah": 2, "Kondisi": "Baik", "Kalibrasi": "10/2026"},
            {"Kode": "INV-02", "Barang": "Infus Pump Terumo", "Jumlah": 6, "Kondisi": "Baik", "Kalibrasi": "11/2026"},
            {"Kode": "INV-03", "Barang": "Syringe Pump Terumo", "Jumlah": 4, "Kondisi": "Baik", "Kalibrasi": "11/2026"},
            {"Kode": "INV-04", "Barang": "Bed Patient Electric", "Jumlah": 15, "Kondisi": "Baik", "Kalibrasi": "N/A"},
            {"Kode": "INV-05", "Barang": "Suction Pump Portable", "Jumlah": 3, "Kondisi": "Baik", "Kalibrasi": "09/2026"}
        ]

    if 'log_bhp_pasien' not in st.session_state:
        st.session_state.log_bhp_pasien = []
    if 'laporan_insiden' not in st.session_state:
        st.session_state.laporan_insiden = []
    if 'data_handover' not in st.session_state:
        st.session_state.data_handover = []
    if 'data_obat' not in st.session_state:
        st.session_state.data_obat = []
    if 'data_discharge' not in st.session_state:
        st.session_state.data_discharge = []
    if 'log_supervisi' not in st.session_state:
        st.session_state.log_supervisi = []
    if 'log_delegasi' not in st.session_state:
        st.session_state.log_delegasi = []
    if 'keuangan' not in st.session_state:
        st.session_state.keuangan = {"Pendapatan_Bulan_Ini": 145000000, "Pengeluaran_BHP": 38500000}

init_session_states()

# --- FUNGSI PERHITUNGAN OTOMATIS RUMUS INDIKATOR ---
def hitung_indikator():
    p = st.session_state.params_mutu
    tt = max(1, p["total_tt"])
    hari = max(1, p["periode_hari"])
    hp = p["hari_perawatan"]
    pk = max(1, p["pasien_keluar"])

    bor = (hp / (tt * hari)) * 100
    alos = hp / pk
    toi = ((tt * hari) - hp) / pk
    bto = pk / tt

    return round(bor, 1), round(alos, 1), round(toi, 1), round(bto, 1)

# --- NAVIGASI SIDEBAR ---
st.sidebar.title("🏥 RS Widya Mandala")
st.sidebar.caption("Sistem Integrasi Ruang Anyelir")

if st.sidebar.button("🚪 Logout / Keluar"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.divider()

menu_kategori = st.sidebar.radio(
    "Pilih Modul:",
    [
        "Menu", 
        "Kepegawaian", 
        "Bahan Habis Pakai & Pengeluaran", 
        "Indikator Mutu", 
        "Manajemen", 
        "Penerimaan Pasien Baru", 
        "Daftar & Kondisi Pasien", 
        "Timbang Terima (SBAR)", 
        "Sentralisasi Obat", 
        "Discharge Planning"
    ]
)

# ==========================================
# 1. HALAMAN MENU
# ==========================================
if menu_kategori == "Menu":
    st.title("📊 Sistem Integrasi Terpadu Ruang Anyelir")
    st.subheader("Rumah Sakit Widya Mandala")
    
    pasien_aktif_count = len([p for p in st.session_state.data_pasien if p.get('Status') == 'Rawat Inap'])
    total_pasien_terdaftar = len(st.session_state.data_pasien)
    bor_calc, alos_calc, toi_calc, bto_calc = hitung_indikator()
    bor_realtime = round((pasien_aktif_count / st.session_state.params_mutu["total_tt"]) * 100, 1)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Pasien Aktif Rawat", f"{pasien_aktif_count} Pasien", f"Total RM: {total_pasien_terdaftar}")
    col2.metric("Perawat On Duty", f"{st.session_state.params_mutu['perawat_on_duty']} Orang")
    col3.metric("BOR Real-time", f"{bor_realtime}%")
    col4.metric("BOR Periode", f"{bor_calc}%")
    col5.metric("Indeks Kepuasan", f"{st.session_state.params_mutu['kepuasan']}%")

    with st.expander("🛠️ Fast Update Parameter Ruangan (Real-time Input)"):
        with st.form("form_update_dashboard"):
            c_u1, c_u2, c_u3 = st.columns(3)
            new_duty = c_u1.number_input("Jumlah Perawat On Duty", min_value=1, value=int(st.session_state.params_mutu['perawat_on_duty']))
            new_tt = c_u2.number_input("Total Bed / Tempat Tidur Ruangan (TT)", min_value=1, value=int(st.session_state.params_mutu['total_tt']))
            new_sat = c_u3.number_input("Indeks Kepuasan Pasien (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.params_mutu['kepuasan']))
            
            if st.form_submit_button("Update Metrics"):
                st.session_state.params_mutu['perawat_on_duty'] = new_duty
                st.session_state.params_mutu['total_tt'] = new_tt
                st.session_state.params_mutu['kepuasan'] = new_sat
                st.success("Parameter Berhasil Diperbarui!")
                st.rerun()

    st.divider()
    st.subheader("📌 Status Quick Check Pelayanan")
    c1, c2, c3 = st.columns(3)
    c1.info(f"**Timbang Terima Hari Ini:** {len(st.session_state.data_handover)} Catatan Handover")
    c2.warning(f"**Obat Baru Disentralisasi:** {len(st.session_state.data_obat)} Resep Terdaftar")
    c3.success(f"**Jadwal Supervisi Bulan Ini:** {len(st.session_state.log_supervisi)} Kegiatan Terjadwal")

# ==========================================
# 2. KEPEGAWAIAN
# ==========================================
elif menu_kategori == "Kepegawaian":
    st.title("👥 Modul Kepegawaian & Sistem MAKP")
    tab1, tab2, tab3 = st.tabs(["Data Ketenagaan Ruangan", "Kelompok & Struktur MAKP Primer", "Kebutuhan Tenaga (Douglas)"])
    
    with tab1:
        st.subheader("Data Ketenagaan Perawat Ruang Anyelir")
        st.dataframe(pd.DataFrame(st.session_state.data_perawat), use_container_width=True)
        
        with st.expander("➕ Tambah Perawat Baru"):
            with st.form("form_perawat"):
                c1, c2 = st.columns(2)
                nip = c1.text_input("NIP/ID Perawat")
                nama = c2.text_input("Nama Lengkap & Gelar")
                peran = c1.selectbox("Peran MAKP", ["Kepala Ruangan (KARU)", "Perawat Primer 1 (PP1)", "Perawat Primer 2 (PP2)", "Perawat Asosiet (PA)"])
                kualifikasi = c2.selectbox("Pendidikan", ["D3 Keperawatan", "S1 Ners", "S2 Keperawatan"])
                shift = c1.selectbox("Shift", ["Pagi", "Sore", "Malam", "Lepas/Libur"])
                
                if st.form_submit_button("Simpan Data Pegawai"):
                    st.session_state.data_perawat.append({"NIP": nip, "Nama": nama, "Peran": peran, "Kualifikasi": kualifikasi, "Shift": shift})
                    st.success(f"Perawat {nama} berhasil ditambahkan!")
                    st.rerun()

    with tab2:
        st.subheader("Struktur Kelompok Asuhan Keperawatan (MAKP Primer)")
        st.success("👑 **Kepala Ruangan (KARU):** Ns. Hendra, S.Kep")
        st.divider()
        col_team1, col_team2 = st.columns(2)
        
        with col_team1:
            st.markdown("### 🟦 TIM PRIMER 1")
            st.markdown("**Perawat Primer (PP1):** Ns. Ahmad Fauzi, S.Kep")
            st.markdown("**Perawat Asosiet (PA):**\n- Budi Santoso, AMK\n- Siti Aminah, AMK")
            st.markdown("**Pasien Kelolaan Hari Ini:**")
            for p in [p for p in st.session_state.data_pasien if p.get('PPJA') == 'Ns. Ahmad Fauzi, S.Kep']:
                st.caption(f"• {p.get('Kamar', '-')} | {p.get('Nama', '-')} ({p.get('Diagnosis', '-')})")

        with col_team2:
            st.markdown("### 🟩 TIM PRIMER 2")
            st.markdown("**Perawat Primer (PP2):** Ns. Dewi Ratna, S.Kep")
            st.markdown("**Perawat Asosiet (PA):**\n- Ns. Rina Astuti, S.Kep\n- Eko Prasetyo, AMK")
            st.markdown("**Pasien Kelolaan Hari Ini:**")
            for p in [p for p in st.session_state.data_pasien if p.get('PPJA') == 'Ns. Dewi Ratna, S.Kep']:
                st.caption(f"• {p.get('Kamar', '-')} | {p.get('Nama', '-')} ({p.get('Diagnosis', '-')})")

    with tab3:
        st.subheader("Perhitungan Beban Kerja Perawat (Formula Douglas)")
        c_d1, c_d2, c_d3 = st.columns(3)
        min_care = c_d1.number_input("Jumlah Pasien Minimal Care", min_value=0, value=1)
        part_care = c_d2.number_input("Jumlah Pasien Partial Care", min_value=0, value=2)
        tot_care = c_d3.number_input("Jumlah Pasien Total Care", min_value=0, value=2)
        
        req_pagi = (min_care * 0.17) + (part_care * 0.27) + (tot_care * 0.36)
        st.warning(f"**Kebutuhan Tenaga Shift Pagi:** {round(req_pagi, 2)} ≈ {round(req_pagi)} Perawat")

# ==========================================
# 3. BAHAN HABIS PAKAI & PENGELUARAN
# ==========================================
elif menu_kategori == "Bahan Habis Pakai & Pengeluaran":
    st.title("📦 Modul Bahan Habis Pakai (BHP) & Pengeluaran")
    tab1, tab2, tab3 = st.tabs(["Inventaris Ruangan", "Input BHP Per Pasien", "Log Pengeluaran Ruangan"])
    
    with tab1:
        st.subheader("Daftar Inventaris Alkes Ruang Anyelir")
        st.dataframe(pd.DataFrame(st.session_state.data_inventaris), use_container_width=True)

    with tab2:
        st.subheader("Pencatatan Pemakaian BHP Selama Masa Perawatan Pasien")
        with st.form("form_bhp_pasien"):
            c1, c2 = st.columns(2)
            pasien_target = c1.selectbox("Pilih Pasien", [f"{p.get('No_RM', '-')} - {p.get('Nama', '-')} ({p.get('Kamar', '-')})" for p in st.session_state.data_pasien])
            item_bhp = c2.selectbox("Jenis Bahan Habis Pakai (BHP)", [
                "Abocath No. 20G", "Abocath No. 22G", "Infus Set Makro", "Infus Set Mikro", 
                "Blood Set", "Spuit 3cc", "Spuit 5cc", "Spuit 10cc", "Kassa Steril (Box)", 
                "Underpad", "Nasal Kanul O2", "Cateter Folley No. 16", "Urine Bag"
            ])
            jumlah_bhp = c1.number_input("Jumlah Pemakaian", min_value=1, value=1)
            perawat_input = c2.selectbox("Perawat Pelapor", [p["Nama"] for p in st.session_state.data_perawat])
            ttd_e = st.text_input("Tanda Tangan Elektronik", value="e-signed")
            
            if st.form_submit_button("Catat Pemakaian BHP"):
                st.session_state.log_bhp_pasien.append({
                    "Waktu": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Pasien": pasien_target,
                    "Item_BHP": item_bhp,
                    "Jumlah": jumlah_bhp,
                    "Perawat": perawat_input,
                    "TTD": ttd_e
                })
                st.success("Pemakaian BHP Pasien Berhasil Dicatat!")
                st.rerun()

        if st.session_state.log_bhp_pasien:
            st.divider()
            st.subheader("📋 Log Pemakaian BHP Pasien Real-Time")
            st.dataframe(pd.DataFrame(st.session_state.log_bhp_pasien), use_container_width=True)

    with tab3:
        st.subheader("Ringkasan Pengeluaran & Anggaran Unit")
        col_k1, col_k2 = st.columns(2)
        col_k1.metric("Pendapatan Unit (Est. Bulan Ini)", f"Rp {st.session_state.keuangan['Pendapatan_Bulan_Ini']:,}")
        col_k2.metric("Pengeluaran Operasional BHP", f"Rp {st.session_state.keuangan['Pengeluaran_BHP']:,}")

# ==========================================
# 4. INDIKATOR MUTU
# ==========================================
elif menu_kategori == "Indikator Mutu":
    st.title("📈 Modul Indikator Mutu Pelayanan & Efisiensi")
    tab1, tab2 = st.tabs(["Kalkulator Rumus Indikator (BOR, ALOS, TOI, BTO)", "Form Pelaporan Kejadian Insiden Mutu"])
    
    with tab1:
        st.subheader("⚡ Parameter Perhitungan Otomatis Indikator Efisiensi")
        st.caption("Masukan data variabel pelayanan, kalkulasi rumus BOR, ALOS, TOI, dan BTO akan dihitung secara otomatis.")
        
        with st.form("form_rumus_mutu"):
            cm1, cm2 = st.columns(2)
            val_tt = cm1.number_input("Jumlah Tempat Tidur (TT)", min_value=1, value=int(st.session_state.params_mutu['total_tt']))
            val_periode = cm2.number_input("Periode Waktu Perhitungan (Hari)", min_value=1, value=int(st.session_state.params_mutu['periode_hari']))
            val_hp = cm1.number_input("Jumlah Hari Perawatan (HP)", min_value=0, value=int(st.session_state.params_mutu['hari_perawatan']))
            val_pk = cm2.number_input("Jumlah Pasien Keluar (Hidup + Mati)", min_value=1, value=int(st.session_state.params_mutu['pasien_keluar']))
            
            if st.form_submit_button("🧮 Hitung & Simpan Indikator Otomatis"):
                st.session_state.params_mutu['total_tt'] = val_tt
                st.session_state.params_mutu['periode_hari'] = val_periode
                st.session_state.params_mutu['hari_perawatan'] = val_hp
                st.session_state.params_mutu['pasien_keluar'] = val_pk
                st.success("Perhitungan Rumus Indikator Berhasil Diperbarui!")
                st.rerun()

        bor_calc, alos_calc, toi_calc, bto_calc = hitung_indikator()

        st.divider()
        st.subheader("📊 Hasil Kalkulasi Indikator Mutu")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("BOR (Bed Occupancy Rate)", f"{bor_calc}%", "Standar Depkes: 60 - 85%")
        m2.metric("ALOS (Length of Stay)", f"{alos_calc} Hari", "Standar Depkes: 6 - 9 Hari")
        m3.metric("TOI (Turn Over Interval)", f"{toi_calc} Hari", "Standar Depkes: 1 - 3 Hari")
        m4.metric("BTO (Bed Turn Over)", f"{bto_calc} Kali", "Standar Depkes: 40 - 50 Kali")

    with tab2:
        st.subheader("Laporan Kronologi Kejadian Insiden Keselamatan Pasien")
        with st.form("form_insiden"):
            ci1, ci2 = st.columns(2)
            jenis_insiden = ci1.selectbox("Jenis Insiden Mutu", ["Kejadian Pasien Jatuh", "Kejadian Phlebitis", "Kejadian Decubitus"])
            pasien_insiden = ci2.selectbox("Pasien Terkait", [f"{p.get('No_RM', '-') } - {p.get('Nama', '-')}" for p in st.session_state.data_pasien])
            kronologi = st.text_area("Uraian Kronologi Kejadian Insiden Detail")
            tindakan_koreksi = st.text_area("Tindakan / Intervensi Penanganan Langsung")
            perawat_pelapor = ci1.selectbox("Perawat Pelapor", [p["Nama"] for p in st.session_state.data_perawat])
            ttd_insiden = ci2.text_input("Tanda Tangan Elektronik", value="e-signed")
            
            if st.form_submit_button("Laporkan Insiden Mutu"):
                st.session_state.laporan_insiden.append({
                    "Waktu": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Jenis": jenis_insiden,
                    "Pasien": pasien_insiden,
                    "Kronologi": kronologi,
                    "Tindakan": tindakan_koreksi,
                    "Pelapor": perawat_pelapor,
                    "TTD": ttd_insiden
                })
                st.success("Laporan insiden mutu berhasil terdokumentasi!")
                st.rerun()

        if st.session_state.laporan_insiden:
            st.divider()
            st.subheader("📋 Rekapitulasi Laporan Insiden Mutu Ruangan")
            st.dataframe(pd.DataFrame(st.session_state.laporan_insiden), use_container_width=True)

# ==========================================
# 5. MANAJEMEN
# ==========================================
elif menu_kategori == "Manajemen":
    st.title("📋 Modul Manajemen (Supervisi & Delegasi)")
    tab1, tab2, tab3 = st.tabs(["Jadwal & Paparan Supervisi", "Buku Log Delegasi Tugas", "Unduh SOP Kegiatan Supervisi"])
    
    with tab1:
        st.subheader("Jadwal Supervisi Keperawatan Ruang Anyelir")
        with st.form("form_supervisi"):
            cs1, cs2 = st.columns(2)
            tgl_sup = cs1.date_input("Tanggal Supervisi")
            perawat_sup = cs2.selectbox("Perawat Ter-supervisi", [p["Nama"] for p in st.session_state.data_perawat])
            fokus_sup = st.text_input("Fokus Tindakan (misal: Pemasangan Infus / Handover SBAR)")
            supervisor_name = cs1.selectbox("Supervisor", [p["Nama"] for p in st.session_state.data_perawat if "KARU" in p["Peran"] or "PP" in p["Peran"]])
            ttd_sup = cs2.text_input("Tanda Tangan Elektronik", value="e-signed")
            
            if st.form_submit_button("Simpan Jadwal Supervisi"):
                st.session_state.log_supervisi.append({
                    "Tanggal": str(tgl_sup),
                    "Waktu_Input": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Perawat": perawat_sup,
                    "Fokus_Tindakan": fokus_sup,
                    "Supervisor": supervisor_name,
                    "Status": "Terjadwal",
                    "TTD": ttd_sup
                })
                st.success("Jadwal Supervisi Berhasil Ditambahkan!")
                st.rerun()

        st.divider()
        st.subheader("Paparan Jadwal Supervisi Terdaftar")
        if st.session_state.log_supervisi:
            st.dataframe(pd.DataFrame(st.session_state.log_supervisi), use_container_width=True)

    with tab2:
        st.subheader("Pencatatan Delegasi Tugas Manajemen")
        with st.form("form_delegasi"):
            cd1, cd2 = st.columns(2)
            pemberi_d = cd1.selectbox("Pemberi Delegasi", [p["Nama"] for p in st.session_state.data_perawat])
            penerima_d = cd2.selectbox("Penerima Delegasi", [p["Nama"] for p in st.session_state.data_perawat])
            tugas_d = st.text_area("Rincian Tugas yang Didelegasikan")
            ttd_del = cd1.text_input("Tanda Tangan Elektronik Pemberi", value="e-signed")
            
            if st.form_submit_button("Simpan Log Delegasi"):
                st.session_state.log_delegasi.append({
                    "Waktu": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Pemberi": pemberi_d,
                    "Penerima": penerima_d,
                    "Tugas": tugas_d,
                    "Status": "Aktif / Terdelegasi",
                    "TTD": ttd_del
                })
                st.success("Pencatatan Delegasi Tugas Selesai!")
                st.rerun()

        if st.session_state.log_delegasi:
            st.divider()
            st.subheader("📜 Rekapitulasi Log Delegasi Tugas")
            st.dataframe(pd.DataFrame(st.session_state.log_delegasi), use_container_width=True)

    with tab3:
        st.subheader("Berkas Standar Operasional Prosedur (SOP) Supervisi")
        sop_infus = "SOP PEMASANGAN INFUS\n1. Cuci tangan 6 langkah\n2. Identifikasi pasien\n3. Siapkan alat steril & abocath\n4. Lakukan desinfeksi area penusukan..."
        sop_sbar = "SOP TIMBANG TERIMA SBAR\n1. Siapkan rekam medis\n2. S (Situation): Identitas & keluhan\n3. B (Background): Riwayat medis\n4. A (Assessment): TTV & Analisis\n5. R (Recommendation): Rencana..."
        
        c_down1, c_down2 = st.columns(2)
        c_down1.download_button("📥 Unduh SOP Pemasangan Infus (TXT)", data=sop_infus, file_name="SOP_Pemasangan_Infus.txt")
        c_down2.download_button("📥 Unduh SOP Handover SBAR (TXT)", data=sop_sbar, file_name="SOP_Handover_SBAR.txt")

# ==========================================
# 6. PENERIMAAN PASIEN BARU
# ==========================================
elif menu_kategori == "Penerimaan Pasien Baru":
    st.title("🛏️ Modul Penerimaan Pasien Baru (Admission)")
    
    with st.form("form_pasien_baru"):
        st.subheader("Formulir Registrasi Pasien Masuk")
        c1, c2 = st.columns(2)
        no_rm = c1.text_input("No. Rekam Medis (RM)")
        nama = c2.text_input("Nama Lengkap Pasien")
        kamar = c1.text_input("Nomor Kamar & Bed", value="Anyelir - ")
        
        dpjp_pilihan = c2.selectbox("Pilih DPJP (Dokter Penanggung Jawab Pelayanan)", st.session_state.daftar_dpjp + ["+ Tambah DPJP Baru..."])
        if dpjp_pilihan == "+ Tambah DPJP Baru...":
            dpjp_final = st.text_input("Masukkan Nama & Gelar DPJP Baru")
        else:
            dpjp_final = dpjp_pilihan
            
        ketergantungan = c1.selectbox("Tingkat Ketergantungan", ["Minimal Care", "Partial Care", "Total Care"])
        ppja = c2.selectbox("Perawat PPJA", [p["Nama"] for p in st.session_state.data_perawat if "PP" in p["Peran"] or "KARU" in p["Peran"]])
        dx = st.text_input("Diagnosis Medis Masuk")
        
        st.markdown("**Variasi Checklist Orientasi Pasien Baru:**")
        col_chk1, col_chk2 = st.columns(2)
        o1 = col_chk1.checkbox("Orientasi Denah Ruangan, Kamar Mandi, & Air Panas")
        o2 = col_chk1.checkbox("Edukasi Penggunaan Bel Nurse Call & Lampu")
        o3 = col_chk1.checkbox("Penjelasan Aturan Jam Besuk & Penunggu (Maks 1 Orang)")
        o4 = col_chk1.checkbox("Perkenalan Perawat PPJA, Katim, & DPJP")
        o5 = col_chk2.checkbox("Edukasi Kebersihan Tangan / Cuci Tangan 6 Langkah")
        o6 = col_chk2.checkbox("Penjelasan Hak & Kewajiban Pasien")
        o7 = col_chk2.checkbox("Pemasangan Gelang Identitas & Gelang Resiko Jatuh")
        o8 = col_chk2.checkbox("Informasi Jalur Evakuasi & Titik Kumpul Darurat")
        
        ttd_adm = st.text_input("Tanda Tangan Elektronik Perawat Penerima", value="e-signed")
        
        if st.form_submit_button("Daftarkan Pasien Baru"):
            if dpjp_pilihan == "+ Tambah DPJP Baru..." and dpjp_final and dpjp_final not in st.session_state.daftar_dpjp:
                st.session_state.daftar_dpjp.append(dpjp_final)
                
            waktu_registrasi = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            st.session_state.data_pasien.append({
                "No_RM": no_rm,
                "Nama": nama,
                "Kamar": kamar,
                "DPJP": dpjp_final,
                "Ketergantungan": ketergantungan,
                "PPJA": ppja,
                "Diagnosis": dx,
                "Status": "Rawat Inap",
                "Tgl_Masuk": waktu_registrasi,
                "TTD_Perawat": ttd_adm
            })
            st.success(f"Pasien {nama} berhasil terdaftar dengan DPJP {dpjp_final}!")
            st.rerun()

# ==========================================
# 7. DAFTAR & KONDISI PASIEN (DIAMANKAN DENGAN .get())
# ==========================================
elif menu_kategori == "Daftar & Kondisi Pasien":
    st.title("📑 Modul Rekapitulasi & Kondisi Pasien")
    st.markdown("Memunculkan seluruh data pasien terdaftar dan pasien input manual secara komprehensif.")
    
    if st.session_state.data_pasien:
        df_all_pasien = pd.DataFrame(st.session_state.data_pasien)
        st.dataframe(df_all_pasien, use_container_width=True)
        
        st.divider()
        st.subheader("🔍 Detail Kondisi Pasien Rawat Inap")
        for idx, p in enumerate(st.session_state.data_pasien, 1):
            with st.expander(f"Pasien #{idx}: {p.get('Kamar', '-')} - {p.get('Nama', '-')} ({p.get('No_RM', '-')})"):
                st.write(f"- **DPJP Utama:** {p.get('DPJP', 'Belum Diisi')}")
                st.write(f"- **Diagnosis:** {p.get('Diagnosis', '-')}")
                st.write(f"- **Tingkat Ketergantungan:** {p.get('Ketergantungan', '-')}")
                st.write(f"- **PPJA Responsible:** {p.get('PPJA', '-')}")
                st.write(f"- **Waktu Masuk Rawat:** {p.get('Tgl_Masuk', '-')}")
                st.write(f"- **Tanda Tangan Perawat Registrasi:** {p.get('TTD_Perawat', '-')}")
    else:
        st.info("Belum ada data pasien terdaftar.")

# ==========================================
# 8. TIMBANG TERIMA SBAR
# ==========================================
elif menu_kategori == "Timbang Terima (SBAR)":
    st.title("🔄 Modul Timbang Terima / Handover (SBAR)")
    
    if not st.session_state.data_pasien:
        st.warning("Belum ada pasien terdaftar.")
    else:
        pasien_pilih = st.selectbox("Pilih Pasien Terdaftar:", [f"{p.get('No_RM', '-')} - {p.get('Nama', '-')} ({p.get('Kamar', '-')}) - DPJP: {p.get('DPJP', '-')}" for p in st.session_state.data_pasien])
        
        with st.form("form_sbar"):
            st.subheader("Dokumentasi Komunikasi SBAR")
            s = st.text_area("S (Situation) - Keluhan Utama & Status Saat Ini")
            b = st.text_area("B (Background) - Riwayat Penyakit & Alergi Obat")
            a = st.text_area("A (Assessment) - Hasil TTV & Analisis Keperawatan")
            r = st.text_area("R (Recommendation) - Rencana Intervensi Lanjutan Shift Berikutnya")
            
            c_sbar1, c_sbar2 = st.columns(2)
            pemberi = c_sbar1.selectbox("Perawat Shift Lepas", [p["Nama"] for p in st.session_state.data_perawat])
            penerima = c_sbar2.selectbox("Perawat Shift Terima", [p["Nama"] for p in st.session_state.data_perawat])
            ttd_handover = c_sbar1.text_input("Tanda Tangan Elektronik Perawat", value="e-signed")
            
            if st.form_submit_button("Simpan Dokumentasi Handover"):
                waktu_ho = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                st.session_state.data_handover.append({
                    "Waktu": waktu_ho,
                    "Pasien": pasien_pilih,
                    "Situation": s,
                    "Background": b,
                    "Assessment": a,
                    "Recommendation": r,
                    "Pemberi": pemberi,
                    "Penerima": penerima,
                    "TTD": ttd_handover
                })
                st.success(f"Timbang terima SBAR berhasil disimpan pada {waktu_ho}!")
                st.rerun()

    if st.session_state.data_handover:
        st.divider()
        st.subheader("📜 Riwayat Catatan Timbang Terima SBAR")
        st.dataframe(pd.DataFrame(st.session_state.data_handover), use_container_width=True)
# ==========================================
# 9. SENTRALISASI OBAT (REVISI 19, 20, 22)
# ==========================================
elif menu_kategori == "Sentralisasi Obat":
    st.title("💊 Modul Sentralisasi & Pengelolaan Obat Pasien")
    
    tab1, tab2 = st.tabs(["Form Sentralisasi & ACC Farmasi", "Daftar & Status Obat Pasien"])
    
    with tab1:
        # REVISI 19: VERIFIKASI 6 BENAR OBAT & FORM ACC FARMASI & PERAWAT
        st.subheader("Formulir Penerimaan & Verifikasi Obat Pasien")
        
        with st.form("form_obat_6benar"):
            pasien_o = st.selectbox("Pasien", [f"{p['No_RM']} - {p['Nama']}" for p in st.session_state.data_pasien])
            nama_obat = st.text_input("Nama Obat, Dosis, & Frekuensi (misal: Ceftriaxone 2x1gr)")
            rute_o = st.selectbox("Rute Pemberian", ["IV / Injeksi", "Oral", "SC / IM", "Topikal", "Inhalasi"])
            stok_o = st.number_input("Jumlah Stok Obat Diterima", min_value=1, value=10)
            
            st.markdown("**Verifikasi Keamanan 6 Benar Obat:**")
            c_b1, c_b2 = st.columns(2)
            b1 = c_b1.checkbox("1. Benar Pasien")
            b2 = c_b1.checkbox("2. Benar Obat")
            b3 = c_b1.checkbox("3. Benar Dosis")
            b4 = c_b2.checkbox("4. Benar Rute Pemberian")
            b5 = c_b2.checkbox("5. Benar Waktu Pemberian")
            b6 = c_b2.checkbox("6. Benar Dokumentasi")
            
            st.markdown("**Persetujuan / ACC Verifikasi:**")
            c_acc1, c_acc2, c_acc3 = st.columns(3)
            acc_farmasi = c_acc1.text_input("Nama Apoteker / Farmasi ACC", value="apt. Sarah, S.Farm")
            acc_perawat = c_acc2.selectbox("Perawat Penerima", [p["Nama"] for p in st.session_state.data_perawat])
            status_o = c_acc3.selectbox("Status Awal Obat", ["Diterima", "Sedang Dalam Proses", "Habis"])
            ttd_o = st.text_input("Tanda Tangan Elektronik Perawat", value="e-signed")
            
            if st.form_submit_button("Simpan Data Sentralisasi Obat"):
                if b1 and b2 and b3 and b4 and b5 and b6:
                    st.session_state.data_obat.append({
                        "Waktu": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Pasien": pasien_o,
                        "Obat": nama_obat,
                        "Rute": rute_o,
                        "Stok": stok_o,
                        "Status": status_o,
                        "ACC_Farmasi": acc_farmasi,
                        "Perawat_Penerima": acc_perawat,
                        "TTD": ttd_o
                    })
                    st.success("Obat berhasil diverifikasi 6 Benar dan disimpan!")
                    st.rerun()
                else:
                    st.error("Gagal! Seluruh prinsip 6 Benar Obat wajib dicentang untuk keamanan pasien.")

    with tab2:
        # REVISI 20: STATUS DAFTAR OBAT SETIAP PASIEN
        st.subheader("Daftar Obat Pasien & Status Ketersediaan Real-Time")
        if st.session_state.data_obat:
            st.dataframe(pd.DataFrame(st.session_state.data_obat), use_container_width=True)
            
            st.divider()
            st.markdown("### Update Status Obat Pasien")
            with st.form("form_update_status_obat"):
                idx_o = st.selectbox("Pilih Urutan Obat untuk Di-update", range(len(st.session_state.data_obat)), format_func=lambda x: f"{st.session_state.data_obat[x]['Pasien']} - {st.session_state.data_obat[x]['Obat']}")
                new_st = st.selectbox("Update Status Terbaru", ["Diterima", "Sedang Dalam Proses", "Habis"])
                if st.form_submit_button("Update Status Obat"):
                    st.session_state.data_obat[idx_o]['Status'] = new_st
                    st.success("Status Obat Diperbarui!")
                    st.rerun()
        else:
            st.info("Belum ada data obat tersentralisasi.")

# ==========================================
# 10. DISCHARGE PLANNING (REVISI 21, 22)
# ==========================================
elif menu_kategori == "Discharge Planning":
    st.title("🚪 Modul Discharge Planning (Perencanaan Pulang)")
    
    if st.session_state.data_pasien:
        with st.form("form_discharge"):
            st.subheader("Formulir Perencanaan Pulang Pasien")
            pasien_dc = st.selectbox("Pilih Pasien Rencana Pulang", [f"{p['No_RM']} - {p['Nama']} ({p['Diagnosis']})" for p in st.session_state.data_pasien])
            tgl_pulang = st.date_input("Rencana Tanggal Pulang")
            
            # REVISI 21: VARIASI EDUKASI DISCHARGE PLANNING
            st.markdown("**Variasi Edukasi & Check-list Kesiapan Kepulangan Pasien:**")
            cd1, cd2 = st.columns(2)
            e1 = cd1.checkbox("Edukasi Aturan, Aturan Dosis, & Efek Samping Obat Pulang")
            e2 = cd1.checkbox("Edukasi Diit Khusus & Nutrisi di Rumah")
            e3 = cd1.checkbox("Edukasi Perawatan Luka / Perawatan Alat Medis di Rumah")
            e4 = cd2.checkbox("Edukasi Batasan Aktivitas Fisik & Mobilisasi")
            e5 = cd2.checkbox("Edukasi Tanda-Tanda Bahaya & Kapan Harus ke IGD")
            e6 = cd2.checkbox("Penjadwalan Kontrol Ulang Poli Spesialis")
            
            catatan_dc = st.text_area("Catatan Khusus Resume Kepulangan Pasien")
            perawat_dc = cd1.selectbox("Perawat Edukator", [p["Nama"] for p in st.session_state.data_perawat])
            ttd_dc = cd2.text_input("Tanda Tangan Elektronik", value="e-signed")
            
            if st.form_submit_button("Simpan Discharge Planning"):
                waktu_dc = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                st.session_state.data_discharge.append({
                    "Waktu_Input": waktu_dc,
                    "Pasien": pasien_dc,
                    "Tgl_Pulang": str(tgl_pulang),
                    "Status_Edukasi": "Lengkap" if (e1 and e2 and e3 and e4 and e5 and e6) else "Belum Lengkap",
                    "Catatan": catatan_dc,
                    "Perawat": perawat_dc,
                    "TTD": ttd_dc
                })
                st.success(f"Discharge planning pasien berhasil diproses pada {waktu_dc}!")
                st.rerun()

    if st.session_state.data_discharge:
        st.divider()
        st.subheader("📋 Log Perencanaan Kepulangan Pasien (Discharge Planning)")
        st.dataframe(pd.DataFrame(st.session_state.data_discharge), use_container_width=True)