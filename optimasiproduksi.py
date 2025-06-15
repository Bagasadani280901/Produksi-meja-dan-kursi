import streamlit as st
from scipy.optimize import linprog

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
