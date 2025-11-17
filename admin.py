from prettytable import PrettyTable
from create import lihatproduk,judul
from USER import antriTopUp
import pandas as pd
import inquirer
import os


LP = {}

def tambahproduk():
    columns_required = ["id", "nama", "kategori", "harga", "gender", "stok"]
    try:
        df = pd.read_csv('produk.csv')
        for col in columns_required:
            if col not in df.columns:
                raise ValueError("Struktur produk.csv tidak sesuai: kolom '" + col + "' tidak ditemukan")
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns_required)
    except ValueError as e:
        print(str(e))
        return

    if df.empty:
        next_id = 1
    else:
        try:
            next_id = int(df['id'].max()) + 1
        except Exception:
            print("Kolom id mengandung nilai tidak valid.")
            return

    nama = input("Masukkan nama produk: ").strip()
    if not nama:
        print("Nama produk tidak boleh kosong.")
        return
    kategori_choices = ["atasan", "bawahan", "sepatu", "pelengkap"]
    gender_choices = ["pria", "wanita", "unisex"]
    kategori_prompt = [
        inquirer.List("kategori", message="Pilih kategori", choices=[f"{i+1}. {v}" for i, v in enumerate(kategori_choices)])
    ]
    ans = inquirer.prompt(kategori_prompt)
    if not ans:
        return
    kategori_ans = ans["kategori"]
    kategori = kategori_choices[int(kategori_ans.split(".")[0]) - 1]
    gender_prompt = [
        inquirer.List("gender", message="Pilih gender", choices=[f"{i+1}. {v}" for i, v in enumerate(gender_choices)])
    ]
    ans = inquirer.prompt(gender_prompt)
    if not ans:
        return
    gender_ans = ans["gender"]
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
    new_row = {"id": next_id, "nama": nama, "kategori": kategori, "harga": harga, "gender": gender, "stok": stok}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    try:
        df.to_csv('produ.csv', index=False)
        print("Produk berhasil ditambahkan:")
        table = PrettyTable()
        table.field_names = ["id", "nama", "kategori", "harga", "gender", "stok"]
        table.add_row([next_id, nama, kategori, harga, gender, stok])
        print(table)
    except Exception as e:
        print(f"Gagal menyimpan produk: {e}")

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

    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for _, row in df.iterrows():
        table.add_row(row.tolist())
    print(table)

    pilih_prompt = [
        inquirer.List("metode", message="Hapus berdasarkan", choices=["1. id", "2. username"])
    ]
    ans = inquirer.prompt(pilih_prompt)
    if not ans:
        return
    metode = ans["metode"]

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