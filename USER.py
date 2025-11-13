from prettytable import PrettyTable
from create import lihatproduk,tambahpesanan,judul
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

def hapuspesanan():
    print("hapus pesanan")

def konfirmasipesanan(username):
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
