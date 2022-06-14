import sqlite3
from xmlrpc.client import DateTime
con = sqlite3.connect('projeto.db')
cur = con.cursor()

def inserir_utilizador(username, password, role):
    cur.execute(f"INSERT INTO Users VALUES ('{username}', '{password}', '{role}')")
    con.commit()    

def inserir_espetaculo(name):
    cur.execute(f"INSERT INTO Espetaculos (nome) VALUES('{name}')")
    con.commit()

def inserir_nova_data(name, date):
    cur.execute(f"INSERT INTO Datas_espetaculo (data, espetaculo) VALUES('{DateTime(date)}', '{name}')")

def change_password(username, password):
    cur.execute(f"UPDATE Users SET password='{password}' WHERE username='{username}'")
    
def apagar_reserva(reserva):
    cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE reserva='{reserva}'")