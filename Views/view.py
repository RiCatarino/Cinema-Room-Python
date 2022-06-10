import sqlite3
from Models import model as mod
from Controllers import controller as cont

con = sqlite3.connect('projeto.db', isolation_level=None)
cur = con.cursor()
has_txn_open = False

currentuser = ""


def main():
    print("\n-----COOLISEU-----")
    menu_inicial()


def menu_inicial():
    print("1. Iniciar Sessão")
    print("2. Registar Utilizador")
    option = input("\nOpção ( Número ): ")
    if int(option) == 1:
        cont.login()
    elif int(option) == 2:
        cont.signup("User")
        menu_inicial()


def menuAdmin():
    print(
        "\n1. Inserir Espetáculo\n2. Inserir nova data do espetáculo\n3. Ver sala por sessão \n4. Bilheteira  \n5. Alterar password de um cliente\n6. Alterar password\n7. Registar novo administrador\n8. Sair")
    option = int(input("\nOpção:"))
    if option == 1:
        cont.inserir_espetaculo()
    elif option == 2:
        cont.inserir_nova_data(None)
    elif option == 3:
        cont.ver_sala()
    elif option == 4:
        menuBilheteira()
    elif option == 5:
        cont.alterar_password_by_utilizador(False, None)
    elif option == 6:
        cont.alterar_password()
    elif option == 7:
        cont.signup("admin")
    elif option == 8:
        menu_inicial()


def menuBilheteira():
    print(
        "\n1. Valor por dia \n2. Valor por mês\n3. Valor por ano \n4. Valor por espetáculo \n5. Valor por sessão\n")
    option = int(input("\nOpção:"))
    if option == 1:
        cont.bilheteira_por_dia()
    elif option == 2:
        cont.bilheteira_por_mes()
    elif option == 3:
        cont.bilheteira_por_ano()
    elif option == 4:
        cont.bilheteira_por_espetaculo()
    elif option == 5:
        cont.bilheteira_por_sessao()


def menuUser():
    global has_txn_open
    while True:
        if has_txn_open:
            con.rollback()
            has_txn_open = False
        print("\n1. Reservar bilhetes\n2. Alterar Reserva\n3. Cancelar Reserva\n4. Alterar password\n5. Sair")
        option = input("\nOpção: ")
        try:
            if int(option) == 1:
                cont.reservar_bilhetes(None, None)
            elif int(option) == 2:
                cont.alterar_reserva()
            elif int(option) == 3:
                cont.cancelar_reserva()
            elif int(option) == 4:
                cont.alterar_password()
            elif int(option) == 5:
                menu_inicial()
            else:
                print("Opção não existe.")
        except:
            print("Opção não existe.")
