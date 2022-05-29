from pickle import NONE
import sqlite3
from xmlrpc.client import DateTime
from Models import model
from Controllers import controller
con = sqlite3.connect('projeto.db')
cur = con.cursor()

currentuser = ""
letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
sala = []


def main():
    while True:
        print("\n-----COOLISEU-----")
        print("1. Iniciar Sessão")
        print("2. Registar Utilizador")
        option = input("Opção ( Número ): ")
        if int(option) == 1:
             login()
        elif int(option) == 2:
            signup("User")
             
            
def menuAdmin():
    print("\n1. Inserir Espetáculo\n2. Inserir nova data do espetáculo\n3. Alterar password de um cliente\n4. Alterar password\n5. Registar novo administrador")
    optionstr = input("Opção:")
    option = int(optionstr)
    if option == 1:
        inserir_espetaculo()
    elif option == 2:
        inserir_nova_data(None)
    elif option == 3:
        alterar_password_by_utilizador(False, None)
    elif option == 4:
        alterar_password()
    elif option == 5:
        signup("Admin")
    

def menuUser():
    print("\n1. Reservar bilhetes\n2. Alterar Reserva\n3. Cancelar Reserva\n4. Alterar password")
    option = input("Opção: ")
    if int(option) == 1:
        reservar_bilhetes()
        
def login():
    global currentuser
    username = input("Username: ")
    password = input("Password: ")
    if model.checkUser(username, password):
        if model.checkAdmin(username, password):

            currentuser = username
            print(f"\n---------- Olá {currentuser}, administrador ----------")
            menuAdmin()
        else:
            currentuser = username
            print(f"\n---------- Olá {currentuser} ----------")
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
        menuAdmin()

def listar_espetaculos():
    i = 0
    print("\n------Lista de Espetáculos------")
    espetaculos = []
    for espetaculo in cur.execute("SELECT nome FROM Espetaculos"):
        i+=1
        espetaculos.append(espetaculo[0])
        print(f"{i}: {espetaculo[0]} ")
    print("---------------------------------")    
    option = input("Escolha o Espetáculo: ")
    selected = espetaculos[int(option)-1]
    return selected

def listar_datas_espetaculo(nome):
    print(f"\n------ Datas do espetáculo {nome} ----")
    print("\n\t--------------")
    for date in cur.execute(f"SELECT data FROM Datas WHERE espetaculo='{nome}'"):
        print(f"\t| {date[0]} |")
    print("\t--------------")

def listar_datas_espetaculo_para_reserva(nome):
    print(f"\n------ Datas do espetáculo {nome} ----")
    print("\n\t--------------")
    datas = []
    for date in cur.execute(f"SELECT data FROM Datas WHERE espetaculo='{nome}'"):
        datas.append(date[0])
    for i in range(0, len(datas)):
        print(f"\t| {i+1}: {datas[i]} |")
    print("\t--------------")
    option = input("\n Qual data pretende? ")
    return datas[int(option)-1]

def inserir_nova_data(nome_espetaculo):
    if nome_espetaculo == None:
        nome_espetaculo = listar_espetaculos()
        listar_datas_espetaculo(nome_espetaculo)
    novadata = input("\nNova Data 'dd/mm/yyyy': ")
    if controller.inserir_nova_data(nome_espetaculo, novadata):
        print("\n---------- Sessão adicionada com sucesso. ----------")
        menuAdmin()
    else:
        inserir_nova_data(nome_espetaculo)

def listar_utilizadores():
    print("\n------ Utilizadores ------\n")
    for user in cur.execute("SELECT username FROM Users WHERE role='User'"):
        print(f"\t{user[0]}")
        print("\t--------------")

def alterar_password_by_utilizador(error, username):
    if not error:
        listar_utilizadores()
    if username == None:
        username = input("\nEscolha o utilizador: ")
    if controller.check_utilizador(username):
        password = input("\nNova password: ")
        repeatpassword = input("\nRepita a nova password: ")
        if password == repeatpassword:
            model.change_password(username, password)
            print("\n------Password Alterada com sucesso.------\n")
            menuAdmin()
        else:
            print("\n------As password não coincidem.------\n")
            alterar_password_by_utilizador(True, username)
    else:
        print("\nEsse Utilizador não existe.")
        alterar_password_by_utilizador(True, None)
        
def alterar_password():
    password = input("\nNova password: ")
    repeatpassword = input("\nRepita a nova password: ")
    print(f"user {currentuser}")
    if password == repeatpassword:
        model.change_password(currentuser, password)
        print("\n------Password Alterada com sucesso.------\n")
        main()
    else:
        print("\n------As password não coincidem.------\n")
        alterar_password()


def mostrar_sala(result):
    for i in range (0, 11):
        sala.append([" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "])
    for i in range(0, 11):
        for k in range(1):
            if i == 5:
                print(letras[i] sala[i][k], sala[i][k+1], "              ", "VIP", "VIP", "VIP", "VIP", "              ", sala[i][k+12], sala[i][k+13])
                print()
            elif i == 10:
                print() 
                print(sala[i][k], sala[i][k+1], "              ", "VIP", "VIP", "VIP", "VIP", "              ", sala[i][k+12], sala[i][k+13])
            else:
                print(sala[i][k], sala[i][k+1], "  ", sala[i][k+2], sala[i][k+3], sala[i][k+4], sala[i][k+5], sala[i][k+6], sala[i][k+7], sala[i][k+8], sala[i][k+9], sala[i][k+10], sala[i][k+11], "  ", sala[i][k+12], sala[i][k+13])

def reservar_bilhetes():
    espetaculo = listar_espetaculos()
    data = listar_datas_espetaculo_para_reserva(espetaculo)
    cur.execute(f"SELECT reservas FROM Datas WHERE data='{DateTime(data)}' AND espetaculo='{espetaculo}'")
    result = cur.fetchall()
    print(result)
    mostrar_sala(result)
    lugares = []
    quantidade = int(input("Quantos lugares pretende reservar? "))
    for i in range(0, quantidade+1):
        lugar = input("Escola o lugar: ")
        lugares.append(lugar)