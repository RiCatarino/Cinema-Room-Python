import sqlite3
from tkinter import Menu
from unicodedata import name
from Models import model
from Controllers import controller
con = sqlite3.connect('projeto.db')
cur = con.cursor()

def main():
    while True:
        print("\n-----COOLISEU-----")
        print("1. Iniciar Sessão")
        print("2. Registar Utilizador")
        option = input("Opção ( Número ): ")
        if int(option) == 1:
             login()
        elif int(option) == 2:
            signup("user")
             
            
             

def menuAdmin():
    print("\n1. Inserir Espetáculo\n2. Inserir nova data do espetáculo\n3. Alterar password de um cliente\n4. Alterar password\n5. Registar novo administrador")
    optionstr = input("Opção: ")
    option = int(optionstr)
    if option == 1:
        inserir_espetaculo()
    elif option == 2:
        print("Alterar")
    elif option == 3:
        print("Cancelar")
    elif option == 4:
        print("Password")
    

def menuUser():
    print("\n1. Reservar bilhetes\n2. Alterar Reserva\n3. Cancelar Reserva\n4. Alterar password")
    option = input("Opção: ")
    if int(option) == 1:
        print("toma")
        
def login():
    username = input("Username: ")
    password = input("Password: ")
    if model.checkUser(username, password):
        if model.checkAdmin(username, password):
            print(f"\n---------- Olá {username}, administrador ----------")
            menuAdmin()
            
        else:
            print(f"\n---------- Olá {username} ----------")
            menuUser()
    else:
        print("Utilizador ou Password incorretos.")
        login()
        

def signup(role):
    username = input("Username: ")
    password = input("Password: ")
    cur.execute(f"INSERT INTO Users VALUES ('{username}', '{password}', '{role}')")
    con.commit()
    

def inserir_espetaculo():
    name = input("\nNome do novo espetáculo: ")
    cur.execute(f"INSERT INTO Espetaculos (nome) VALUES('{name}')")
    con.commit()
    
    option = input("Pretende inserir datas para este espetáculo?: (Sim / Não):  ")
    if option == "Sim":
        newdate = input("Nova Data 'dd/mm/yyyy': ")
        controller.inserir_nova_data(name, newdate)
        # controller.inserir_nova_data()
            
