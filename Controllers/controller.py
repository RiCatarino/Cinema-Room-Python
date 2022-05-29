import sqlite3
from xmlrpc.client import DateTime

con = sqlite3.connect('projeto.db')
cur = con.cursor()


def inserir_nova_data(name, date):
    cur.execute(f"INSERT INTO Datas (data, espetaculo) VALUES('{DateTime(date)}', '{name}')")
    con.commit()

def get_espetaculos():
    for espetaculo in cur.execute("SELECT id, nome FROM Espetaculos"):
        print(f"\nID: {espetaculo[0]} Nome: {espetaculo[1]} ")