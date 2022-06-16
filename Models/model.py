import sqlite3
from xmlrpc.client import DateTime

from Controllers.controller import desbloquear_utilizador
con = sqlite3.connect('projeto.db')
cur = con.cursor()

def inserir_utilizador(username, password, role):
    cur.execute(f"INSERT INTO Users VALUES ('{username}', '{password}', '{role}', NULL)")
    con.commit()    

def inserir_espetaculo(name):
    cur.execute(f"INSERT INTO Espetaculos (nome) VALUES('{name}')")
    con.commit()

def inserir_nova_data(name, date):
    cur.execute(f"INSERT INTO Datas_espetaculo (data, espetaculo) VALUES('{DateTime(date)}', '{name}')")
    con.commit()

def change_password(username, password):
    cur.execute(f"UPDATE Users SET password='{password}' WHERE username='{username}'")
    con.commit()
    
def apagar_reserva(reserva):
    cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE reserva='{reserva}'")
    cur.execute(f"DELETE FROM Reservas WHERE id='{reserva}'")
    con.commit()

def bloquear_utilizador(username):
    cur.execute(f"UPDATE Users SET blocked = 'True' WHERE username='{username}'")
    con.commit()

def desbloquear_utilizador(username):
    cur.execute(f"UPDATE Users SET blocked = NULL WHERE username='{username}'")
    con.commit()
