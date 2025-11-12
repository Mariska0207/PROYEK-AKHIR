from create import lihatproduk
import pandas as pd
import inquirer

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