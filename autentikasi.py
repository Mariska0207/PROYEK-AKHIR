from create import judul,info
from USER import loginuser
from admin import loginadmin
import pandas as pd
import os
import re

kesempatanlogin = 3

def registrasi():
    judul("REGISTRASI")
    try:
        userbaru = input("Username(3-10 karakter) : ")
        if len(userbaru) < 3 or len(userbaru) > 10:
            raise ValueError("username harus 3-10 karakter")
        if userbaru == "":
            raise ValueError("input tidak boleh kosong")
        if not re.match("^[A-Za-z0-9]+$", userbaru):
            raise ValueError("username hanya boleh huruf dan angka")
        try:
            df = pd.read_csv('akun.csv', dtype={'id': int, 'username': str, 'password': str, 'role': str, 'saldo': int})
        except FileNotFoundError:
            df = pd.DataFrame(columns=["id", "username", "password", "role", "saldo"])

        if userbaru in df['username'].values:
            input("Username sudah terdaftar! Tekan Enter untuk melanjutkan...")
            return

        pwbaru = input("Password(4-10 karakter) : ")
        if len(pwbaru) < 4 or len(pwbaru) > 10:
            raise ValueError("password harus 6-10 karakter")
        if pwbaru == "":
            raise ValueError("input tidak boleh kosong")
        if not re.match("^[A-Za-z0-9]+$", pwbaru):
            raise ValueError("password hanya boleh huruf dan angka")
        
        try:
            saldo = int(input("saldo: "))
            if saldo < 0:
                raise ValueError("saldo tidak boleh negatif")
        except ValueError:
            raise ValueError("saldo harus berupa angka")
        
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
        user = input("username: ")
        if user == "":
            raise ValueError("input tidak boleh kosong")
        if not re.match("^[A-Za-z0-9]+$", user):
            raise ValueError("username hanya boleh huruf dan angka")
        pw = input("password: ")
        if pw == "":
            raise ValueError("input tidak boleh kosong")
        if not re.match("^[A-Za-z0-9]+$", pw):
            raise ValueError("password hanya boleh huruf dan angka")
    except ValueError as e:
        print(e)
        input("enter untuk kembali ke menu....")
        return
    
    try:
        df = pd.read_csv('akun.csv', dtype=str)
    except FileNotFoundError:
        print("file tidak ditemukan")
        return
    
    role = None 
    for index, row in df.iterrows():
        if row["username"] == user and row["password"] == pw:
            role = row["role"]
            break
    if role is not None: 
        info(f"anda berhasil login sebagai {role}")
        if role == "admin":
            loginadmin(user)
        elif role == "user":
            loginuser(user)
    else:
        kesempatanlogin -= 1
        if kesempatanlogin > 0:
            print(f"Login anda Gagal, kesempatan login tersisa {kesempatanlogin}")
            input("enter untuk kembali ke menu....")
            os.system("cls || clear")
        else:
            print("kesempatan anda habis")
            input("enter untuk keluar")
            os.system('cls || clear')
            print("ANDA TELAH KELUAR".center(50))
            print("TERIMA KASIH SUDAH MENGGUNAKAN PROGRAM INI".center(50))
            exit()