import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data hasil gabungan dan cleaning
merged_df = pd.read_csv("dashboard/all_data.csv", parse_dates=['order_purchase_timestamp'])

# Judul Dashboard
st.title("Dashboard Analisis E-Commerce Publik")
st.markdown("Dashboard ini menampilkan insight dari transaksi pelanggan berdasarkan kota, metode pembayaran, dan pola transaksi.")

# ======================================
# SIDEBAR: FILTER INTERAKTIF
# ======================================
st.sidebar.header("Filter Data")

# Filter Tanggal
min_date = merged_df['order_purchase_timestamp'].min().date()
max_date = merged_df['order_purchase_timestamp'].max().date()
date_range = st.sidebar.date_input("Pilih Rentang Tanggal:", [min_date, max_date])

# Filter Metode Pembayaran
available_payments = [p for p in merged_df['payment_type'].unique().tolist() if p != 'not_defined']
available_payments.insert(0, 'All')
selected_payment = st.sidebar.selectbox("Pilih Metode Pembayaran:", options=available_payments)

# ======================================
# FILTER DATAFRAME
# ======================================
# Filter tanggal terlebih dahulu
filtered_df = merged_df[
    (merged_df['order_purchase_timestamp'].dt.date >= date_range[0]) &
    (merged_df['order_purchase_timestamp'].dt.date <= date_range[1])
]

# Filter metode pembayaran
if selected_payment != 'All':
    filtered_df = filtered_df[filtered_df['payment_type'] == selected_payment]

# Tampilkan jumlah data
st.caption(f"Jumlah data setelah filter: {len(filtered_df)}")

# Jika tidak ada data
if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    # ===============================
    # Statistik Deskriptif
    # ===============================
    st.subheader(f"📊 Statistik untuk Metode Pembayaran: {selected_payment}")
    st.write(filtered_df[['payment_value', 'payment_installments']].describe())

    # ===============================
    # SECTION 1: Top 10 Kota
    # ===============================
    st.header("Top 10 Kota dengan Frekuensi Pembelian Terbanyak")

    top_cities = filtered_df['customer_city'].value_counts().head(10)

    if top_cities.empty:
        st.info("Tidak ada kota dengan transaksi pada filter yang dipilih.")
    else:
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        sns.barplot(x=top_cities.index, y=top_cities.values, palette='Blues_d', ax=ax1)
        plt.xticks(rotation=45)
        plt.xlabel("Kota")
        plt.ylabel("Jumlah Pembelian")
        plt.title("Top 10 Kota Berdasarkan Transaksi")
        for i, v in enumerate(top_cities.values):
            ax1.text(i, v + 0.5, str(v), ha='center')
        st.pyplot(fig1)

    # ===============================
    # SECTION 2: Metode Pembayaran
    # ===============================
    st.header("💳 Metode Pembayaran Paling Sering Digunakan")

    payment_counts = filtered_df[filtered_df['payment_type'] != 'not_defined']['payment_type'].value_counts()

    if payment_counts.empty:
        st.info("Tidak ada data metode pembayaran untuk ditampilkan.")
    else:
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        colors = plt.cm.Set3.colors
        wedges, texts, autotexts = ax2.pie(
            payment_counts,
            labels=[f"{label} ({value})" for label, value in zip(payment_counts.index, payment_counts.values)],
            autopct='%1.1f%%',
            startangle=140,
            textprops={'color': 'black'},
            labeldistance=1.15,
            colors=colors
        )
        ax2.axis('equal')
        st.pyplot(fig2)

    # ===============================
    # SECTION 3: Clustering Customer
    # ===============================
    st.header("👥 Distribusi Customer Berdasarkan Jumlah Transaksi")

    customer_freq = filtered_df['customer_id'].value_counts().reset_index()
    customer_freq.columns = ['customer_id', 'jumlah_transaksi']

    def group_customer(freq):
        if freq <= 2:
            return 'Low'
        elif freq <= 5:
            return 'Medium'
        else:
            return 'High'

    customer_freq['cluster_group'] = customer_freq['jumlah_transaksi'].apply(group_customer)

    if customer_freq.empty:
        st.info("Tidak ada data customer untuk ditampilkan.")
    else:
        fig3, ax3 = plt.subplots()
        sns.countplot(x='cluster_group', data=customer_freq, order=['Low', 'Medium', 'High'], palette='Blues', ax=ax3)
        for p in ax3.patches:
            ax3.annotate(f'{p.get_height()}', 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom')
        plt.title("Distribusi Customer berdasarkan Cluster Transaksi")
        plt.xlabel("Cluster")
        plt.ylabel("Jumlah Customer")
        st.pyplot(fig3)

# Footer
st.markdown("---")
st.markdown("**Dibuat oleh Jeriko Gormantara - Proyek Analisis Data**")