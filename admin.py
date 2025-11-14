from prettytable import PrettyTable
from create import lihatproduk,judul
from USER import antriTopUp
import pandas as pd
import inquirer
import os


LP = {}

def tambahproduk():
    print("tambah produk.")

def updateproduk(username):
    try:
        df = pd.read_csv('produk.csv')
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    filtered_df = lihatproduk()
    if filtered_df is None:
        return

    try:
        pesan_id = int(input("Masukkan ID produk yang mau diubah: "))
    except ValueError:
        print("Input harus berupa angka.")
        return
    
    if pesan_id not in filtered_df['id'].values:
        print("ID produk tidak valid.")
        return

    produk = df[df['id'] == pesan_id]
    stok = produk['stok'].values[0]
    print()
    indeks = produk.index[0]
    pilih = [
            inquirer.List("opsi",
                    message="PILIH KATEGORI YANG MAU DIUBAH",
                    choices=["1. nama", "2. kategori", "3. stok", "4. harga", "5. gender"],
                ),
    ]
    answer = inquirer.prompt(pilih)
    ubah = answer["opsi"]
    if "1" in ubah:
        nama_baru = input("Masukkan nama baru produk: ")
        if nama_baru != produk['nama'].values[0]:
            df.at[indeks, 'nama'] = nama_baru
            df.to_csv('produk.csv', index=False)
            print("Produk berhasil diupdate!")
        else:
            print("Nama sama dengan sebelumnya, tidak diubah.")
    elif "2" in ubah:
        menu = [
            inquirer.List("opsi",
                message="UBAH KATEGORI",
                choices=["1. atasan", "2. bawahan", "3. sepatu", "4. pelengkap"],
            ),
        ]
        answer = inquirer.prompt(menu)
        kategori_baru = answer["opsi"]
        if "1" in kategori_baru:
            kategori_baru = "atasan"
        elif "2" in kategori_baru:
            kategori_baru = "bawahan"
        elif "3" in kategori_baru:
            kategori_baru = "sepatu"
        else:
            kategori_baru = "pelengkap"
        if kategori_baru != produk['kategori'].values[0]:
            df.at[indeks, 'kategori'] = kategori_baru
            df.to_csv('produk.csv', index=False)
            print("Produk berhasil diupdate!")
        else:
            print("Kategori sama dengan sebelumnya, tidak diubah.")
    elif "3" in ubah:
        try:
            stok_baru = int(input("Masukkan stok baru produk: "))
        except ValueError:
            print("Stok harus berupa angka.")
            return
        if stok >= 0 and stok_baru != produk['stok'].values[0]:
            df.at[indeks, 'stok'] = stok_baru
            df.to_csv('produk.csv', index=False)
            print("Produk berhasil diupdate!")
        else:
            print("Stok sama dengan sebelumnya, tidak diubah.")
    elif "4" in ubah:
        try:
            harga_baru = int(input("Masukkan harga baru produk: "))
        except ValueError:
            print("Harga harus berupa angka.")
            return
        if harga_baru != produk['harga'].values[0]:
            df.at[indeks, 'harga'] = harga_baru
            df.to_csv('produk.csv', index=False)
            print("Produk berhasil diupdate!")
        else:
            print("Harga sama dengan sebelumnya, tidak diubah.")
    else:
        menu = [
            inquirer.List("opsi",
                message="UBAH GENDER",
                choices=["pria", "wanita", "unisex"],
            ),
        ]
        answer = inquirer.prompt(menu)
        gender_baru = answer["opsi"]
        if gender_baru != produk['gender'].values[0]:
            df.at[indeks, 'gender'] = gender_baru
            df.to_csv('produk.csv', index=False)
            print("Produk berhasil diupdate!")
        else:
            print("Gender sama dengan sebelumnya, tidak diubah.")

def hapusproduk():
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
    try:
        id_str = input("Masukkan ID produk yang akan dihapus: ").strip()
        id_produk = int(id_str)
    except ValueError:
        print("ID harus berupa angka valid.")
        return
    if id_produk not in df['id'].values:
        print("ID produk tidak ditemukan.")
        return
    nama_produk = df.loc[df['id'] == id_produk, 'nama'].values[0]
    konfirmasi = input(f"Yakin hapus produk '{nama_produk}' (ID {id_produk})? [y/N]: ").strip().lower()
    if konfirmasi != 'y':
        print("Penghapusan dibatalkan.")
        return
    
    try:
        df_baru = df[df['id'] != id_produk]
        df_baru.to_csv('produk.csv', index=False)
        print(f"Produk dengan ID {id_produk} berhasil dihapus.")
    except Exception as e:
        print(f"Gagal menghapus produk: {e}")

    print("hapus produk")

def verifikasitopup():
    if not antriTopUp:
        print("Tidak ada antrian top up.")
        return

    table = PrettyTable()
    table.field_names = ['No', 'Username', 'Nominal', 'Status']
    pending= [i for i, req in enumerate(antriTopUp) if req['status'] == 'pending']

    for i, j in enumerate(pending):
        req = antriTopUp[j]
        table.add_row([i + 1, req['username'], req['nominal'], req['status']])
    print("Daftar Antrian Top Up (Pending):")
    print(table)

    try:
        pilihan = int(input("Pilih nomor antrian untuk diverifikasi (0 untuk batal): "))
        if pilihan == 0:
            return
        if not (1 <= pilihan <= len(pending)):
            print("Pilihan tidak valid.")
            return
        
        id = pending[pilihan - 1]
        verifikasi = antriTopUp[id]

        action_question = [
            inquirer.List("action",
                        message=f"Verifikasi top up untuk {verifikasi['username']} sebesar {verifikasi['nominal']}",
                        choices=["Setujui", "Tolak"],
            ),
        ]
        answer = inquirer.prompt(action_question)    
        action = answer["action"]

        if action == "Setujui":
            df_akun = pd.read_csv('akun.csv')
            user_index = df_akun.index[df_akun['username'] == verifikasi['username']].tolist()
            if user_index:
                df_akun.loc[user_index[0], 'saldo'] += verifikasi['nominal']
                df_akun.to_csv('akun.csv', index=False)
                verifikasi['status'] = 'approved'
                print(f"Top up untuk {verifikasi['username']} sebesar {verifikasi['nominal']} telah disetujui.")
        elif action == "Tolak":
            verifikasi['status'] = 'gagal'
            print(f"Top up untuk {verifikasi['username']} sebesar {verifikasi['nominal']} telah ditolak.")

    except (ValueError, IndexError, TypeError):
        print("Input tidak valid.")

def laporanpenjualan():
    print(LP)
    print("laporan penjualan")

def hapususer():
    print("hapus user")

def loginadmin(username):
    while True:
        os.system("cls || clear")
        menuuser = [
            inquirer.List("opsi",
                    message="SILAHKAN PILIH OPSI",
                    choices=["1. tambah produk", "2. lihat produk", "3. update produk", "4. hapus produk", "5. verifikasi top up", "6. laporan penjualan", "7. hapus user", "8. keluar"],
                ),
        ]
        answer = inquirer.prompt(menuuser)
        menuuser = answer["opsi"]
        os.system("cls || clear")

        if "1" in menuuser:
            judul("TAMBAH PRODUK")
            tambahproduk()
            input("enter untuk kembali ke menu....")
        elif "2" in menuuser:
            judul("LIHAT PRODUK")
            lihatproduk()
            input("enter untuk kembali ke menu....")
        elif "3" in menuuser:
            judul("UPDATE PRODUK")
            updateproduk(username)
            input("\nenter untuk kembali ke menu....")
        elif "4" in menuuser:
            judul("HAPUS PRODUK")
            hapusproduk()
            input("enter untuk kembali ke menu....")
        elif "5" in menuuser:
            judul("VERIFIKASI TOP UP")
            verifikasitopup()
            input("enter untuk kembali ke menu....")
        elif "6" in menuuser:
            judul("LAPORAN PENJUALAN")
            laporanpenjualan()
            input("enter untuk kembali ke menu....")
        elif "7" in menuuser:
            judul("HAPUS USER")
            hapususer()
            input("enter untuk kembali ke menu....")
        else:
            break