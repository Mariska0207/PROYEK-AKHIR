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

# Admin: tambah produk
# - Auto-increment ID berdasarkan kolom 'id' terbesar pada produk.csv
# - Validasi input angka untuk harga dan stok
# - Validasi pilihan enumerasi untuk gender dan kategori
# - Tampilkan ringkasan setelah penambahan

def tambah_produk():
    columns = ["id", "nama", "kategori", "harga", "gender", "stok"]
    try:
        df = pd.read_csv('produk.csv')
        # Pastikan kolom minimum ada, jika tidak, sesuaikan
        for col in columns:
            if col not in df.columns:
                raise ValueError("Struktur produk.csv tidak sesuai: kolom '" + col + "' tidak ditemukan")
    except FileNotFoundError:
        # Jika belum ada file, mulai dengan DataFrame kosong
        df = pd.DataFrame(columns=columns)
    except ValueError as e:
        print(str(e))
        return

    # Tentukan id baru
    if df.empty:
        next_id = 1
    else:
        try:
            next_id = int(df['id'].max()) + 1
        except Exception:
            print("Kolom id mengandung nilai tidak valid.")
            return

    # Input interaktif
    nama = input("Masukkan nama produk: ").strip()
    if not nama:
        print("Nama produk tidak boleh kosong.")
        return

    kategori_choices = ["atasan", "bawahan", "sepatu", "pelengkap"]
    gender_choices = ["pria", "wanita", "unisex"]

    kategori_prompt = [
        inquirer.List("kategori", message="Pilih kategori", choices=[f"{i+1}. {v}" for i, v in enumerate(kategori_choices)])
    ]
    kategori_ans = inquirer.prompt(kategori_prompt)["kategori"]
    kategori = kategori_choices[int(kategori_ans.split(".")[0]) - 1]

    gender_prompt = [
        inquirer.List("gender", message="Pilih gender", choices=[f"{i+1}. {v}" for i, v in enumerate(gender_choices)])
    ]
    gender_ans = inquirer.prompt(gender_prompt)["gender"]
    gender = gender_choices[int(gender_ans.split(".")[0]) - 1]

    try:
        harga = int(input("Masukkan harga (angka): ").strip())
        if harga <= 0:
            print("Harga harus > 0.")
            return
    except ValueError:
        print("Harga harus berupa angka.")
        return

    try:
        stok = int(input("Masukkan stok (angka): ").strip())
        if stok < 0:
            print("Stok tidak boleh negatif.")
            return
    except ValueError:
        print("Stok harus berupa angka.")
        return

    # Susun baris baru dan simpan
    new_row = {"id": next_id, "nama": nama, "kategori": kategori, "harga": harga, "gender": gender, "stok": stok}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    try:
        df.to_csv('produk.csv', index=False)
        print("Produk berhasil ditambahkan:")
        table = PrettyTable()
        table.field_names = ["id", "nama", "kategori", "harga", "gender", "stok"]
        table.add_row([next_id, nama, kategori, harga, gender, stok])
        print(table)
    except Exception as e:
        print(f"Gagal menyimpan produk: {e}")

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

# Admin: hapus user
# - Menampilkan daftar user dari akun.csv
# - Memilih user berdasarkan id atau username
# - Validasi agar admin tidak terhapus
# - Simpan perubahan ke akun.csv

def hapus_user():
    akun_cols = ["id", "username", "password", "role", "saldo"]
    try:
        df = pd.read_csv('akun.csv')
        for c in akun_cols:
            if c not in df.columns:
                raise ValueError("Struktur akun.csv tidak sesuai: kolom '" + c + "' tidak ditemukan")
    except FileNotFoundError:
        print("File akun.csv tidak ditemukan.")
        return
    except ValueError as e:
        print(str(e))
        return

    if df.empty:
        print("Tidak ada data user.")
        return

    # Tampilkan tabel user
    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for _, row in df.iterrows():
        table.add_row(row.tolist())
    print(table)

    # Pilih metode hapus
    pilih_prompt = [
        inquirer.List("metode", message="Hapus berdasarkan", choices=["1. id", "2. username"])
    ]
    metode = inquirer.prompt(pilih_prompt)["metode"]

    if metode.startswith("1"):
        try:
            id_str = input("Masukkan ID user yang akan dihapus: ").strip()
            target_id = int(id_str)
        except ValueError:
            print("ID harus berupa angka.")
            return

        if target_id not in df['id'].values:
            print("ID user tidak ditemukan.")
            return

        # Cegah hapus admin
        if any((df['id'] == target_id) & (df['role'] == 'admin')):
            print("Akun admin tidak boleh dihapus.")
            return

        username = df.loc[df['id'] == target_id, 'username'].values[0]
        konfirmasi = input(f"Yakin hapus user '{username}' (ID {target_id})? [y/N]: ").strip().lower()
        if konfirmasi != 'y':
            print("Penghapusan dibatalkan.")
            return

        df_baru = df[df['id'] != target_id]
    else:
        username = input("Masukkan username yang akan dihapus: ").strip()
        if username == "":
            print("Username tidak boleh kosong.")
            return
        if username not in df['username'].values:
            print("Username tidak ditemukan.")
            return
        if any((df['username'] == username) & (df['role'] == 'admin')):
            print("Akun admin tidak boleh dihapus.")
            return
        konfirmasi = input(f"Yakin hapus user '{username}'? [y/N]: ").strip().lower()
        if konfirmasi != 'y':
            print("Penghapusan dibatalkan.")
            return
        df_baru = df[df['username'] != username]

    try:
        df_baru.to_csv('akun.csv', index=False)
        print("User berhasil dihapus.")
    except Exception as e:
        print(f"Gagal menghapus user: {e}")


def hapus_produk():
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