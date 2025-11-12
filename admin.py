from prettytable import PrettyTable
from create import lihatproduk,judul
from update import updateproduk
import pandas as pd
import inquirer
import os

def tambahproduk():
    print("tambah produk.")

def hapusproduk():
    print("hapus produk")

def verifikasitopup():
    print("verifikasi top up")

def laporanpenjualan():
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