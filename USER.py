from prettytable import PrettyTable
from create import lihatproduk,judul
from datetime import datetime
import pandas as pd
import inquirer
import os

pesanan = {}
antriTopUp = []
waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

current_user = None

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
    print("pesanan berhasil dihapus")

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
    print()
    opsi = [
        inquirer.List("konfirmasi",
                message="Apakah Anda yakin ingin mengonfirmasi pesanan ini?",
                choices=["1. Ya", "2. Tidak"],
            ),
    ]
    answer = inquirer.prompt(opsi)
    if "2" in answer["konfirmasi"]:
        print("Konfirmasi pesanan dibatalkan.")
        return

    df_akun.loc[df_akun['username'] == username, 'saldo'] = saldo_user - total_semua
    df_akun.to_csv("akun.csv", index=False)

    try:
        df_produk = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("File produk.csv tidak ditemukan.")
        return

    for item in pesanan.values():
        produk_id = item['id']
        jumlah = item['jumlah']
        if produk_id in df_produk['id'].values:
            current_stok = df_produk.loc[df_produk['id'] == produk_id, 'stok'].values[0]
            if current_stok < jumlah:
                print(f"Stok produk '{item['nama']}' tidak cukup saat konfirmasi.")
                print("Konfirmasi pesanan dibatalkan.")
                return
            df_produk.loc[df_produk['id'] == produk_id, 'stok'] = current_stok - jumlah

    df_produk.to_csv('produk.csv', index=False)

    try:
        df_riwayat = pd.read_csv("riwayat.csv")
    except FileNotFoundError:
        df_riwayat = pd.DataFrame(columns=["username", "nama_produk", "jumlah", "total", "tanggal"])

    for item in pesanan.values():
        total = item['jumlah'] * item['harga']
        df_riwayat.loc[len(df_riwayat)] = {
            "username": username,
            "nama_produk": item['nama'],
            "jumlah": item['jumlah'],
            "total": total,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    df_riwayat.to_csv("riwayat.csv", index=False)
    pesanan.clear()
    print("pesanan berhasil dikonfirmasi")

def historipembelianTopUp():
    judul("PEMBELIAN & TOP UP")
    opsi = [
        inquirer.List("pilih",
                message="Pilih histori yang ingin dilihat",
                choices=["1. Pembelian", "2. Top up"],
            ),
    ]
    answer = inquirer.prompt(opsi)
    pilih = answer["pilih"]
    os.system("cls || clear")

    def riwayatPembelian():
        global current_user
        if current_user is None:
            print("Tidak ada pengguna yang sedang login.")
            return
        try:
            df = pd.read_csv('riwayat.csv')
        except FileNotFoundError:
            print("File riwayat.csv tidak ditemukan.")
            return

        riwayat = df[df['username'] == current_user]

        if riwayat.empty:
            print("Anda belum memiliki riwayat pembelian.")
            return

        table = PrettyTable()
        table.field_names = ["Nama Produk", "Jumlah", "Total Harga", "Waktu Pembelian"]
        for _, row in riwayat.iterrows():
            waktu_pembelian = row['waktu'] if 'waktu' in riwayat.columns else 'N/A'
            table.add_row([row['nama_produk'], row['jumlah'], row['total'], waktu_pembelian])

        judul("RIWAYAT PEMBELIAN ANDA")
        print(table)

    def historiTopUp():
        global current_user
        if current_user is None:
            print("Tidak ada pengguna yang sedang login.")
            return
        try:
            df = pd.read_csv('topup.csv')
        except FileNotFoundError:
            print("File topup.csv tidak ditemukan.")
            return

        topup = df[df['username'] == current_user]

        if topup.empty:
            print("Anda belum melakukan top up.")
            return

        table = PrettyTable()
        table.field_names = ["No.", "Username", "Jumlah Top Up", "Waktu Top Up"]
        for _, row in topup.iterrows():
            id_row = row['id'] if 'id' in topup.columns else 'N/A'
            username_row = row['username'] if 'username' in topup.columns else 'N/A'
            jumlah_row = row['top_up'] if 'top_up' in topup.columns else row.get('top up', 'N/A')
            waktu_row = row['waktu'] if 'waktu' in topup.columns else 'N/A'
            table.add_row([id_row, username_row, jumlah_row, waktu_row])

        judul("HISTORI TOP UP ANDA")
        print(table)

    if "1" in pilih:
        riwayatPembelian()
    else:
        historiTopUp()

def topup(username):
    from datetime import datetime
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

    try:
        df_topup = pd.read_csv('topup.csv')
    except FileNotFoundError:
        df_topup = pd.DataFrame(columns=['id', 'username', 'top_up', 'waktu'])

    new_id = 1
    if not df_topup.empty:
        new_id = df_topup['id'].max() + 1

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df_topup.loc[len(df_topup)] = {
        'id': new_id,
        'username': username,
        'top_up': nominal,
        'waktu': waktu
    }
    df_topup.to_csv('topup.csv', index=False)

    table = PrettyTable()
    table.field_names = ['Username', 'Nominal', 'Status']
    for item in antriTopUp:
        table.add_row([item['username'], item['nominal'], item['status']])
    print("\nDaftar Antrian Top Up:")
    print(table)
    print("\nSilahkan tunggu konfirmasi dari admin. Jangan lupa cek status top up Anda.")

def loginuser(username):
    global current_user
    current_user = username
    while True:
        os.system("cls || clear")
        menuuser = [
            inquirer.List("opsi",
                message="SILAHKAN PILIH OPSI",
                choices=["1. Lihat saldo", "2. Lihat produk", "3. Tambah pesanan", "4. Hapus pesanan", "5. Konfirmasi pesanan", "6. Histori pembelian & top up", "7. Top up saldo", "8. Keluar"],
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
            historipembelianTopUp()
            input("enter untuk kembali ke menu....")
        elif "7" in menuuser:
            judul("TOP UP SALDO")
            topup(username)
            input("enter untuk kembali ke menu....")
        else:
            break
