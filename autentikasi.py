from create import judul,info
from USER import loginuser
from admin import loginadmin
from colorama import Style, Fore, Back, init
import pandas as pd
import os
import re

kesempatanlogin = 3
init(autoreset=True)

def registrasi():
    judul("REGISTRASI")
    try:
        userbaru = input("Username(3-10 karakter) : ")
        if len(userbaru) < 3 or len(userbaru) > 10:
            raise ValueError(Fore.RED + "Username harus 3-10 karakter")
        if " " in userbaru:
            raise ValueError(Fore.RED + "Username tidak boleh mengandung spasi")
        if userbaru == "":
            raise ValueError(Fore.RED + "Input tidak boleh kosong")
        if not re.match("^[A-Za-z0-9]+$", userbaru):
            raise ValueError(Fore.RED + "Username hanya boleh huruf dan angka")
        try:
            df = pd.read_csv('akun.csv', dtype={'id': int, 'username': str, 'password': str, 'role': str, 'saldo': int})
        except FileNotFoundError:
            df = pd.DataFrame(columns=["id", "username", "password", "role", "saldo"])

        if userbaru in df['username'].values:
            input(Fore.RED + "Username sudah terdaftar! Tekan enter untuk melanjutkan...")
            return

        pwbaru = input("Password(4-10 karakter) : ")
        if len(pwbaru) < 4 or len(pwbaru) > 10:
            raise ValueError(Fore.RED + "Password harus 4-10 karakter")
        if pwbaru == "":
            raise ValueError(Fore.RED + "Input tidak boleh kosong")
        if " " in pwbaru:
            raise ValueError(Fore.RED + "Password tidak boleh mengandung spasi")
        if not re.match("^[A-Za-z0-9]+$", pwbaru):
            raise ValueError(Fore.RED + "Password hanya boleh huruf dan angka")
        
        try:
            saldo = int(input("saldo: "))
            if saldo < 0:
                raise ValueError(Fore.RED + "Saldo tidak boleh negatif")
        except ValueError:
            raise ValueError(Fore.RED + "Saldo harus berupa angka")
        
        if df.empty:
            idbaru = 1
        else:
            idbaru = df["id"].max() + 1
        akunbaru = {
            "id":idbaru,
            "username":userbaru,
            "password":pwbaru,
            "role":"user",
            "saldo": saldo
        }
        df = pd.concat([df, pd.DataFrame([akunbaru])], ignore_index=True)
        df.to_csv('akun.csv', index=False)
        info(f"Berhasil, username {userbaru} telah terdaftar")
    except ValueError as e: 
        print(e)

def login():
    global kesempatanlogin
    try:
        user = input("Username: ")
        if user == "":
            raise ValueError(Fore.RED + "Input tidak boleh kosong")
        if not re.match("^[A-Za-z0-9]+$", user):
            raise ValueError(Fore.RED + "username hanya boleh huruf dan angka")
        pw = input("Password: ")
        if pw == "":
            raise ValueError(Fore.RED + "Input tidak boleh kosong")
        if not re.match("^[A-Za-z0-9]+$", pw):
            raise ValueError(Fore.RED + "Password hanya boleh huruf dan angka")
    except ValueError as e:
        print(e)
        input("Enter untuk kembali ke menu....")
        return
    
    try:
        df = pd.read_csv('akun.csv', dtype=str)
    except FileNotFoundError:
        print(Fore.RED + "File tidak ditemukan")
        return
    
    role = None 
    for index, row in df.iterrows():
        if row["username"] == user and row["password"] == pw:
            role = row["role"]
            break
    if role is not None: 
        info(Fore.GREEN + f"Anda berhasil login sebagai {role}")
        if role == "admin":
            input("Enter untuk lanjut....")
            loginadmin(user)
        elif role == "user":
            input("Enter untuk lanjut....")
            loginuser(user)
    else:
        kesempatanlogin -= 1
        if kesempatanlogin > 0:
            print(Fore.RED + f"Login Anda gagal, kesempatan login tersisa {kesempatanlogin}")
            input("Enter untuk kembali ke menu....")
            os.system("cls || clear")
        else:
            print(Fore.RED + "Kesempatan Anda habis")
            input("Enter untuk keluar")
            os.system('cls || clear')
            print(Fore.YELLOW + "ANDA TELAH KELUAR".center(50))
            print(Fore.YELLOW + "TERIMA KASIH SUDAH MENGGUNAKAN PROGRAM INI".center(50))
            exit()