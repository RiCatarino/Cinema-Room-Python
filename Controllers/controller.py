import sqlite3
from xmlrpc.client import DateTime
from Models import model
from Views import view
con = sqlite3.connect('projeto.db')
cur = con.cursor()


def inserir_nova_data(name, date):
    cur.execute(f"SELECT * FROM Datas_espetaculo WHERE data='{DateTime(date)}' AND espetaculo='{name}'")
    result = cur.fetchone()
    if result:
        print("Este espetáculo já tem uma sessão nessa data.")
        return False
    model.inserir_nova_data(name, date)
    return True

def get_espetaculos():
    for espetaculo in cur.execute("SELECT id, nome FROM Espetaculos"):
        print(f"\nID: {espetaculo[0]} Nome: {espetaculo[1]} ")

def check_utilizador(username):
    cur.execute(f"SELECT * FROM Users WHERE username='{username}' AND role='User'")
    result = cur.fetchone()
    if result:
        return True
    return False

def check_letra(input):
    letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    if input[0][0] not in letras:
        return False
    if len(input) > 3:
        return False
    if int(input[1:3]) <1 or int(input[1:3]) > 14:
        return False
    return True 


def convert_letters_in_numbers(lista, letras):
    for i in range(0, len(lista)):
        for k in range (0, len(letras)):
            if lista[i][:1] == letras[k]:
                lista[i] = lista[i].replace(str(letras[k]), str(letras.index(letras[k])) + " ")
    list_to_print =[]
    view.sala = view.sala_backup
    for item in range(0, len(lista)):
        list_to_print.append(str(lista[item]).split(" "))
    for item in range(0, len(list_to_print)):
        if list_to_print[item] != ['']:
                view.sala[int(list_to_print[item][0])][int(list_to_print[item][1])-1] = "\033[91m x \033[0m"

def check_if_is_full():
    for i in range(0, 11):
        for j in range(0, 13):
            if view.sala[i][j] == " ▢ ":
                return False
    return True

def get_total_bilheteira(datas):
    reservas = []
    total = 0
    for i in range(0, len(datas)):
        for item in cur.execute(f"SELECT lugar FROM User_espetaculo_lugar WHERE data_espetaculo='{datas[i]}'"):
            reservas.append(item[0])    
    for item in reservas:
        if item == "F6" or item == "F7" or item == "F8" or item == "F8" or item == "A6" or item == "A7" or item == "A8" or item == "A9":
            total += 12
        else: 
            total += 4        
    return total