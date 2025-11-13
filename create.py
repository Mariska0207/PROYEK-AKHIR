from prettytable import PrettyTable
import pandas as pd
import inquirer
import os
import csv

pesanan = {}

garis2 = "="*50
def judul(teks):
    print(garis2)
    print(teks.center(50))
    print(garis2)

garis1 = "^"*50
def info(teks):
    print(garis1)
    print(teks.center(50))
    print(garis1)

def lihatproduk():
    try:
        df = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return None
    opsi = [
        inquirer.List("opsi",
                    message="PILIH GENDER",
                    choices=["1. pria", "2. wanita", "3. unisex"],
                ),
    ]
    answer = inquirer.prompt(opsi)
    gender = answer["opsi"]
    if "1" in gender:
        gender = "pria"
    elif "2" in gender:
        gender = "wanita"
    else:
        gender = "unisex"
    
    os.system("cls || clear")
    
    pilih = [
        inquirer.List("opsi",
                    message="PILIH KATEGORI",
                    choices=["1. atasan", "2. bawahan", "3. sepatu", "4. pelengkap"],
                ),
    ]
    answer = inquirer.prompt(pilih)
    kategori = answer["opsi"]
    if "1" in kategori:
        kategori = "atasan"
    elif "2" in kategori:
        kategori = "bawahan"
    elif "3" in kategori:
        kategori = "sepatu"
    else:
        kategori = "pelengkap"
    os.system("cls || clear")
    filtered_df = df[(df["gender"] == gender) & (df["kategori"] == kategori)]
    if filtered_df.empty:
        print("produk tidak ditemukan")
        return None
    table = PrettyTable()
    table.field_names = filtered_df.columns.tolist()
    for i, j in filtered_df.iterrows():
        table.add_row(j.tolist())
    print(table)
    return filtered_df

def tambahpesanan():
    global pesanan
    try:
        df = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    filtered_df = lihatproduk()
    if filtered_df is None:
        return

    try:
        pesan_id = int(input("masukkan ID pesanan anda: "))
    except ValueError:
        print("Input harus berupa angka.")
        return

    if pesan_id not in filtered_df['id'].values:
        print("ID produk tidak valid.")
        return

    produk = df[df['id'] == pesan_id]

    stok = produk['stok'].values[0]
    if stok <= 0:
        print("Stok produk habis.")
        return

    nama = produk['nama'].values[0]
    harga = produk['harga'].values[0]
    kategori = produk['kategori'].values[0]
    gender = produk['gender'].values[0]

    try:
        jumlah_input = int(input(f"Masukkan jumlah untuk '{nama}': "))
    except ValueError:
        print("Input jumlah harus berupa angka.")
        return

    if jumlah_input <= 0:
        print("Jumlah harus lebih dari 0.")
        return

    if jumlah_input > stok:
        print("Jumlah melebihi stok tersedia.")
        return

    produk_ada = False
    for key, item in pesanan.items():
        if item['id'] == pesan_id:
            item['jumlah'] += jumlah_input
            produk_ada = True
            break

    if not produk_ada:
        pesanan_len = len(pesanan) + 1
        pesanan[pesanan_len] = {
            'id': pesan_id,
            'nama': nama,
            'kategori': kategori,
            'harga': harga,
            'gender': gender,
            'jumlah': jumlah_input
        }

    df.loc[df['id'] == pesan_id, 'stok'] -= jumlah_input
    df.to_csv('produk.csv', index=False)

    os.system("cls || clear")
    table = PrettyTable()
    table.field_names = ["No", "Nama Produk", "Kategori", "Harga", "Gender", "Jumlah"]
    for no, item in pesanan.items():
        table.add_row([no, item['nama'], item['kategori'], item['harga'], item['gender'], item['jumlah']])
    print(table)
    print(f"Pesanan '{nama}' telah ditambahkan.")

def hapus_produk():
    """
    Hapus produk dari produk.csv berdasarkan ID yang dimasukkan admin.
    - Menampilkan daftar produk terlebih dahulu agar ID mudah dipilih.
    - Validasi ID dan handle error file tidak ada.
    """
    # Tampilkan semua produk agar admin bisa melihat ID
    try:
        df = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("File produk.csv tidak ditemukan.")
        return

    if df.empty:
        print("Tidak ada data produk.")
        return

    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for _, row in df.iterrows():
        table.add_row(row.tolist())
    print(table)

    # Minta input ID produk yang akan dihapus
    try:
        id_str = input("Masukkan ID produk yang akan dihapus: ").strip()
        id_produk = int(id_str)
    except ValueError:
        print("ID harus berupa angka valid.")
        return

    if id_produk not in df['id'].values:
        print("ID produk tidak ditemukan.")
        return

    # Konfirmasi
    nama_produk = df.loc[df['id'] == id_produk, 'nama'].values[0]
    konfirmasi = input(f"Yakin hapus produk '{nama_produk}' (ID {id_produk})? [y/N]: ").strip().lower()
    if konfirmasi != 'y':
        print("Penghapusan dibatalkan.")
        return

    # Hapus baris dengan ID tersebut dan simpan kembali
    try:
        df_baru = df[df['id'] != id_produk]
        df_baru.to_csv('produk.csv', index=False)
        print(f"Produk dengan ID {id_produk} berhasil dihapus.")
    except Exception as e:
        print(f"Gagal menghapus produk: {e}")
