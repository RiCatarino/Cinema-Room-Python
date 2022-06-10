import sqlite3
from xmlrpc.client import DateTime

con = sqlite3.connect('projeto.db', isolation_level=None)
cur = con.cursor()

letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
letras.reverse()

sala = []

sala_backup = [[" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", "   ", "   ", "   ", "VIP", "VIP", "VIP", "VIP", "   ", "   ", "   ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ ", " ▢ "],
               [" ▢ ", " ▢ ", "   ", "   ", "   ", "VIP", "VIP", "VIP", "VIP", "   ", "   ", "   ", " ▢ ", " ▢ "],
               ]


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
    cur.execute(f"INSERT INTO Datas_espetaculo (data, espetaculo) VALUES('{DateTime(date)}', '{name}')")


def change_password(username, password):
    cur.execute(f"UPDATE Users SET password='{password}' WHERE username='{username}'")


def mostrar_sala():
    print("\n\t\t\t\033[95m   ESTADO DA SALA")
    print("\033[94m|---------------------------------------------------------------------|")
    print("|     1   2      3   4   5   6   7   8   9   10  11  12     13  14    |")
    for i in range(0, 11):
        for k in range(1):
            if i == 6 or i == 10:
                print()
            print("|", letras[i], "\033[0m", sala[i][k], sala[i][k + 1], "  ", sala[i][k + 2], sala[i][k + 3],
                  sala[i][k + 4], sala[i][k + 5], sala[i][k + 6], sala[i][k + 7], sala[i][k + 8], sala[i][k + 9],
                  sala[i][k + 10], sala[i][k + 11], "  ", sala[i][k + 12], sala[i][k + 13], "\033[94m", letras[i], "|")
    print("\n\t   |----------------------------------------------------------|")
    print("\t   |\t\t\t\t\t\t\t      |")
    print("\t   |\t\t\t PALCO \t\t\t\t      |")
    print("\t   |\t\t\t\t\t\t\t      |")
    print("\t   |----------------------------------------------------------|\033[0m")
