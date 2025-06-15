import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(layout="wide")
st.sidebar.title("📘 Instruksi")
st.sidebar.markdown("""
Aplikasi ini memiliki 4 model matematika di bidang industri:

1. *Optimasi Produksi (Linear Programming)*  
2. *Model Persediaan (EOQ)*  
3. *Model Antrian (M/M/1)*
4. *Break-even Analysis*

Silakan pilih tab di atas untuk mulai menggunakan model.
""")

# Tab Navigasi
menu = st.tabs(["🔧 Optimasi Produksi", "📦 Model Persediaan (EOQ)", "⏳ Model Antrian (M/M/1)", "💰 Analisis Break-even"])

# ===============================
# 1. Linear Programming (Optimasi Produksi)
# ===============================

# Judul aplikasi
st.title("Optimasi Produksi Meja dan Kursi")
st.write("PT. Satyamitra Kemas Lestari ingin memaksimalkan keuntungan dari produksi meja dan kursi.")

# Input dari user (dapat diubah)
keuntungan_meja = st.number_input("Keuntungan per Meja (Rp)", value=20000)
keuntungan_kursi = st.number_input("Keuntungan per Kursi (Rp)", value=10000)
waktu_meja = st.number_input("Waktu Produksi per Meja (menit)", value=45)
waktu_kursi = st.number_input("Waktu Produksi per Kursi (menit)", value=30)
total_waktu = st.number_input("Total Waktu Produksi per Minggu (jam)", value=48)

# Konversi jam ke menit
total_menit = total_waktu * 60

# Fungsi objektif (dikalikan -1 karena linprog melakukan minimisasi)
c = [-keuntungan_meja, -keuntungan_kursi]

# Kendala: 45x + 30y ≤ 2880
A = [[waktu_meja, waktu_kursi]]
b = [total_menit]

# Batasan X >= 0, Y >= 0
x_bounds = (0, None)
y_bounds = (0, None)

# Optimasi
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# Tampilkan hasil
if result.success:
    x = result.x[0]
    y = result.x[1]
    total_profit = keuntungan_meja * x + keuntungan_kursi * y

    st.subheader("Hasil Optimasi:")
    st.write(f"Jumlah Meja yang diproduksi: *{x:.2f}* unit")
    st.write(f"Jumlah Kursi yang diproduksi: *{y:.2f}* unit")
    st.write(f"Total keuntungan maksimal: *Rp {total_profit:,.0f}*")
else:
    st.error("Optimasi gagal dilakukan.")

# ===============================
# 2. EOQ Model
# ===============================
with menu[1]:
    st.header("📦 Model Persediaan - Economic Order Quantity (EOQ)")

    D = st.number_input("Permintaan Tahunan (D)", min_value=1.0, value=1000.0)
    S = st.number_input("Biaya Pemesanan per Order (S)", min_value=0.0, value=50.0)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", min_value=0.1, value=2.0)

    if st.button("📈 Hitung EOQ"):
        try:
            Q = np.sqrt((2 * D * S) / H)
            st.success(f"EOQ: {Q:.2f} unit per order")
            N = D / Q
            st.write(f"Frekuensi Pemesanan: {N:.2f} kali per tahun")

            # Visualisasi
            Q_vals = np.linspace(1, 2*Q, 200)
            TC = (D/Q_vals)*S + (Q_vals/2)*H
            fig, ax = plt.subplots()
            ax.plot(Q_vals, TC, label='Total Cost')
            ax.axvline(Q, color='red', linestyle='--', label='EOQ')
            ax.set_xlabel('Order Quantity')
            ax.set_ylabel('Total Cost')
            ax.set_title('EOQ vs Total Cost')
            ax.legend()
            st.pyplot(fig)
        except:
            st.error("Input tidak valid.")

# ===============================
# 3. Model Antrian M/M/1
# ===============================
with menu[2]:
    st.header("⏳ Model Antrian (M/M/1)")
    arrival = st.number_input("Laju Kedatangan (λ)", min_value=0.0, value=2.0)
    service = st.number_input("Laju Pelayanan (μ)", min_value=0.1, value=4.0)

    if st.button("📊 Hitung Kinerja Antrian"):
        if arrival >= service:
            st.error("Sistem tidak stabil: λ harus < μ")
        else:
            rho = arrival / service
            L = rho / (1 - rho)
            Lq = rho**2 / (1 - rho)
            W = 1 / (service - arrival)
            Wq = arrival / (service * (service - arrival))

            st.success("Hasil Perhitungan:")
            st.write(f"Tingkat Utilisasi (ρ): {rho:.2f}")
            st.write(f"Jumlah rata-rata dalam sistem (L): {L:.2f}")
            st.write(f"Jumlah rata-rata dalam antrian (Lq): {Lq:.2f}")
            st.write(f"Waktu rata-rata dalam sistem (W): {W:.2f} satuan waktu")
            st.write(f"Waktu rata-rata dalam antrian (Wq): {Wq:.2f} satuan waktu")

            # Visualisasi
            lambdas = np.linspace(0.1, service - 0.01, 100)
            Lqs = (lambdas**2) / (service * (service - lambdas))
            fig, ax = plt.subplots()
            ax.plot(lambdas, Lqs)
            ax.set_title("Lq terhadap Laju Kedatangan")
            ax.set_xlabel("Laju Kedatangan (λ)")
            ax.set_ylabel("Lq")
            st.pyplot(fig)

# ===============================
# 4. Break-even Analysis
# ===============================
with menu[3]:
    st.header("💰 Break-even Analysis")

    FC = st.number_input("Fixed Cost (Biaya Tetap)", value=10000.0)
    VC = st.number_input("Variable Cost per unit (Biaya Variabel)", value=50.0)
    P = st.number_input("Selling Price per unit (Harga Jual)", value=100.0)

    if st.button("🧮 Hitung Break-even Point"):
        if P <= VC:
            st.error("Harga jual harus lebih besar dari biaya variabel!")
        else:
            BEP_units = FC / (P - VC)
            st.success(f"Break-even Point: {BEP_units:.2f} unit")

            x = np.linspace(0, BEP_units*2, 100)
            total_cost = FC + VC * x
            total_revenue = P * x

            fig, ax = plt.subplots()
            ax.plot(x, total_cost, label='Total Cost')
            ax.plot(x, total_revenue, label='Total Revenue')
            ax.axvline(BEP_units, color='red', linestyle='--', label='Break-even Point')
            ax.set_xlabel('Jumlah Unit')
            ax.set_ylabel('Rupiah')
            ax.set_title('Analisis Break-even')
            ax.legend()
            st.pyplot(fig)
