from autentikasi import login, registrasi
import inquirer
import os

while True:
    os.system("cls || clear")
    menu = [
        inquirer.List("opsi",
                    message="TOKO PRODUK FASHION",
                    choices=["1. registrasi", "2. login", "3. keluar"],
                ),
    ]
    answer = inquirer.prompt(menu)
    menu = answer["opsi"]
    os.system("cls || clear")

    if "1" in menu:
        registrasi()
        input("enter untuk kembali ke menu....")

    elif "2" in menu:
        login()

    else:
        break
        
os.system('cls || clear')
print("ANDA TELAH KELUAR".center(50))
print("TERIMA KASIH SUDAH MENGGUNAKAN PROGRAM INI".center(50))

