import sqlite3
from xmlrpc.client import DateTime
from Models import model
con = sqlite3.connect('projeto.db')
cur = con.cursor()


def inserir_nova_data(name, date):
    cur.execute(f"SELECT * FROM Datas WHERE data='{DateTime(date)}' AND espetaculo='{name}'")
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

