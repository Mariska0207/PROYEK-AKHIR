from prettytable import PrettyTable
from create import lihatproduk,judul
import pandas as pd
import inquirer
import os

pesanan = {}
antriTopUp = []

def lihatsaldo(username):
    try:
        df = pd.read_csv('akun.csv')
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return
    saldo = "Tidak ditemukan."
    for i, j in df.iterrows():
        if j["username"] == username:
            saldo = j["saldo"]
    print(f"Saldo anda: {saldo}")

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

def hapuspesanan():
    global pesanan
    
    if not pesanan:
        print("Tidak ada pesanan.")
        return
    
    table = PrettyTable()
    table.field_names = ["No", "Nama Produk", "Kategori", "Gender", "Jumlah", "Harga Total"]
    
    for no, item in pesanan.items():
        total = item['harga'] * item['jumlah']
        table.add_row([no, item['nama'], item['kategori'], item['gender'], item['jumlah'], total])

    print("\n=== DAFTAR PESANAN ===")
    print(table)

    try:
        pilih = int(input("Masukkan nomor pesanan yang ingin dihapus: "))
    except ValueError:
        print("Input harus angka.")
        return

    if pilih not in pesanan:
        print("Nomor pesanan tidak ditemukan.")
        return

    item = pesanan[pilih]
    produk_id = item['id']
    jumlah_dihapus = item['jumlah']

    del pesanan[pilih]

    pesanan = {i+1: v for i, v in enumerate(pesanan.values())}

    df = pd.read_csv('produk.csv')

    if produk_id in df['id'].values:
        df.loc[df['id'] == produk_id, 'stok'] += jumlah_dihapus
        df.to_csv('produk.csv', index=False)
    print("hapus pesanan")

def konfirmasipesanan(username):
    global pesanan
    
    if not pesanan:
        print("Tidak ada pesanan yang perlu dikonfirmasi.")
        return
    
    table = PrettyTable()
    table.field_names = ["No", "Nama Produk", "Kategori", "Gender", "Jumlah", "Harga Satuan", "Total"]
    
    total_semua = 0
    for no, item in pesanan.items():
        total = item['jumlah'] * item['harga']
        table.add_row([no, item['nama'], item['kategori'], item['gender'], item['jumlah'], item['harga'], total])
        total_semua += total
        
    print("=== KONFIRMASI PESANAN ===")
    print(table)
    print(f"Total yang harus dibayar: {total_semua}")
    
    try:
        df_akun = pd.read_csv("akun.csv")
    except FileNotFoundError:
        print("File akun.csv tidak ditemukan.")
        return
    
    if username not in df_akun['username'].values:
        print("Akun tidak ditemukan.")
        return
    
    saldo_user = int(df_akun.loc[df_akun['username'] == username, 'saldo'].iloc[0])
    print(f"Saldo anda: {saldo_user}")
    
    if saldo_user < total_semua:
        print("Saldo tidak cukup. Silakan top up terlebih dahulu.")
        return
    
    pilihan = input("Konfirmasi pesanan? (y/n): ").lower()
    if pilihan != "y":
        print("Pesanan dibatalkan.")
        return
    
    df_akun.loc[df_akun['username'] == username, 'saldo'] = saldo_user - total_semua
    df_akun.to_csv("akun.csv", index=False)
    
    try:
        df_riwayat = pd.read_csv("riwayat.csv")
    except FileNotFoundError:
        df_riwayat = pd.DataFrame(columns=["username", "nama_produk", "jumlah", "total"])
        
    for item in pesanan.values():
        total = item['jumlah'] * item['harga']
        df_riwayat.loc[len(df_riwayat)] = {
            "username": username,
            "nama_produk": item['nama'],
            "jumlah": item['jumlah'],
            "total": total
        }
        
    df_riwayat.to_csv("riwayat.csv", index=False)
    pesanan.clear()
    print("konfirmasi pesanan")

def historipembelian():
    print("histori")

def topup(username):
    try:
        df = pd.read_csv('akun.csv')
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return
    saldo = "Tidak ditemukan."
    for i, j in df.iterrows():
        if j["username"] == username:
            saldo = j["saldo"]
    print(f"Saldo anda: {saldo}")
    try:
        nominal = int(input("Masukkan nominal top up: "))
        if nominal <= 0:
            print("Nominal harus lebih dari 0.")
            return
    except ValueError:
        print("Masukkan angka yang valid.")
        return
    antriTopUp.append({'username': username, 'nominal': nominal, 'status': 'pending'})
    table = PrettyTable()
    table.field_names = ['Username', 'Nominal', 'Status']
    for item in antriTopUp:
        table.add_row([item['username'], item['nominal'], item['status']])
    print("\nDaftar Antrian Top Up:")
    print(table)
    print("\nSilahkan tunggu konfirmasi dari admin. Jangan lupa cek status top up Anda.")
    
def loginuser(username):
    while True:
        os.system("cls || clear")
        menuuser = [
            inquirer.List("opsi",
                    message="SILAHKAN PILIH OPSI",
                    choices=["1. lihat saldo", "2. lihat produk", "3. tambah pesanan", "4. hapus pesanan", "5. konfirmasi pesanan", "6. histori pembelian", "7. top up saldo", "8. keluar"],
                ),
        ]
        answer = inquirer.prompt(menuuser)
        menuuser = answer["opsi"]
        os.system("cls || clear")

        if "1" in menuuser:
            judul("LIHAT SALDO")
            lihatsaldo(username)
            input("enter untuk kembali ke menu....")
        elif "2" in menuuser:
            judul("LIHAT PRODUK")
            lihatproduk()
            input("enter untuk kembali ke menu....")
        elif "3" in menuuser: 
            judul("TAMBAH PESANAN")
            tambahpesanan()
            input("enter untuk kembali ke menu....")
        elif "4" in menuuser: 
            judul("HAPUS PESANAN")
            hapuspesanan()
            input("enter untuk kembali ke menu....")
        elif "5" in menuuser:
            judul("KONFIRMASI PESANAN")
            konfirmasipesanan(username)
            input("enter untuk kembali ke menu....")
        elif "6" in menuuser: 
            judul("HISTORI PEMBELIAN")
            historipembelian()
            input("enter untuk kembali ke menu....")
        elif "7" in menuuser:
            judul("TOP UP SALDO")
            topup(username)
            input("enter untuk kembali ke menu....")
        else:
            break
