import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data hasil gabungan dan cleaning
merged_df = pd.read_csv("./all_data.csv")
# Judul Dashboard
st.title("Dashboard Analisis E-Commerce Publik")
st.markdown("Dashboard ini menampilkan insight dari transaksi pelanggan berdasarkan kota, metode pembayaran, dan pola transaksi.")

# ======================================
# SECTION 1: TOP 10 KOTA DENGAN PEMBELIAN TERBANYAK
# ======================================
st.header("Top 10 Kota dengan Frekuensi Pembelian Terbanyak")

top_cities = merged_df['customer_city'].value_counts().head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_cities.index, y=top_cities.values, palette='Blues_d', ax=ax1)
plt.xticks(rotation=45)
plt.xlabel("Kota")
plt.ylabel("Jumlah Pembelian")
plt.title("Top 10 Kota Berdasarkan Transaksi")

# Tambahkan angka di atas batang
for i, v in enumerate(top_cities.values):
    ax1.text(i, v + 100, str(v), ha='center')

st.pyplot(fig1)

# ======================================
# SECTION 2: METODE PEMBAYARAN TERPOPULER
# ======================================
st.header("💳 Metode Pembayaran Paling Sering Digunakan")

payment_counts = merged_df['payment_type'].value_counts()

fig2, ax2 = plt.subplots(figsize=(4,4.5))
ax2.pie(payment_counts, labels=[f"{label} ({value})" for label, value in zip(payment_counts.index, payment_counts.values)],
        autopct='%1.1f%%', startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig2)

# ======================================
# SECTION 3: CLUSTERING BERDASARKAN JUMLAH TRANSAKSI
# ======================================
st.header("👥 Distribusi Customer Berdasarkan Jumlah Transaksi")

# Hitung frekuensi transaksi per customer
customer_freq = merged_df['customer_id'].value_counts().reset_index()
customer_freq.columns = ['customer_id', 'jumlah_transaksi']

# Manual grouping / binning
def group_customer(freq):
    if freq <= 2:
        return 'Low'
    elif freq <= 5:
        return 'Medium'
    else:
        return 'High'

customer_freq['cluster_group'] = customer_freq['jumlah_transaksi'].apply(group_customer)

# Visualisasi
fig3, ax3 = plt.subplots()
sns.countplot(x='cluster_group', data=customer_freq, order=['Low', 'Medium', 'High'], palette='Blues', ax=ax3)

# Tambahkan label angka
for p in ax3.patches:
    ax3.annotate(f'{p.get_height()}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom')

plt.title("Distribusi Customer berdasarkan Cluster Transaksi")
plt.xlabel("Cluster")
plt.ylabel("Jumlah Customer")

st.pyplot(fig3)

# ======================================
# FOOTER
# ======================================
st.markdown("---")
st.markdown("**Dibuat oleh Jeriko Gormantara - Proyek Analisis Data**")
