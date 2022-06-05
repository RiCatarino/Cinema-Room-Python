import sqlite3
from xmlrpc.client import DateTime
con = sqlite3.connect('projeto.db', isolation_level=None)
cur = con.cursor()

def checkUser(username, password):
        cur.execute(f"SELECT * FROM Users WHERE username='{username}' AND password='{password}'")
        if cur.fetchone() != None:
            return True
        else:
            return False

def checkAdmin(username, password):
    cur.execute(f"SELECT role FROM Users WHERE username='{username}' AND password='{password}'")
    if cur.fetchone()[0] == "admin":
        return True
    else:
        return False
    
def inserir_nova_data(name, date):
    cur.execute(f"INSERT INTO Datas (data, espetaculo) VALUES('{DateTime(date)}', '{name}')")
    
def change_password(username, password):
    print(username)
    cur.execute(f"UPDATE Users SET password='{password}' WHERE username='{username}'")
