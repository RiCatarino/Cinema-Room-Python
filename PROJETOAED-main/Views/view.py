from pickle import NONE
from posixpath import split
from pydoc import apropos
import sqlite3
from xmlrpc.client import DateTime
from Models import model
from Controllers import controller
import numpy as np

con = sqlite3.connect('projeto.db', isolation_level=None)
cur = con.cursor()

currentuser = ""
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


def main():
    print("\n-----COOLISEU-----")
    menu_inicial()


def menu_inicial():
    print("1. Iniciar Sessão")
    print("2. Registar Utilizador")
    option = input("Opção ( Número ): ")
    if int(option) == 1:
        login()
    elif int(option) == 2:
        signup("User")
        menu_inicial()


def menuAdmin():
    print(
        "\n1. Inserir Espetáculo\n2. Inserir nova data do espetáculo\n3. Alterar password de um cliente\n4. Alterar password\n5. Registar novo administrador")
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
    while True:
        print("\n1. Reservar bilhetes\n2. Alterar Reserva\n3. Cancelar Reserva\n4. Alterar password")
        option = input("Opção: ")
        if int(option) == 1:
            reservar_bilhetes()
        elif int(option) == 2:
            alterar_reserva()
        elif int(option) == 3:
            cancelar_reserva()


def login():
    global currentuser
    username = input("Username: ")
    password = input("Password: ")
    if model.checkUser(username, password):
        currentuser = username
        if model.checkAdmin(username, password):
            print(f"\n---------- Olá {currentuser}, administrador ----------")
            menuAdmin()
        else:
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
        i += 1
        espetaculos.append(espetaculo[0])
        print(f"{i}: {espetaculo[0]} ")
    print("---------------------------------")
    option = input("Escolha o Espetáculo: ")
    selected = espetaculos[int(option) - 1]
    return selected


def listar_datas_espetaculo(nome):
    print(f"\n------ Datas do espetáculo {nome} ----")
    print("\n\t--------------")
    for date in cur.execute(f"SELECT data FROM Datas WHERE espetaculo='{nome}'"):
        print(f"\t| {date[0]} |")
    print("\t--------------")


def listar_datas_espetaculo_para_reserva(nome):
    datas = []
    for data in cur.execute(f"SELECT id, data FROM Datas_espetaculo WHERE espetaculo='{nome}'"):
        datas.append({"id": data[0], "data": data[1]})

    if datas:
        print(f"\n------ Datas do espetáculo {nome} ----")
        print("\n\t--------------")
        for i in range(0, len(datas)):
            print(f"\t| {i + 1}: {datas[i]['data']} |")
        print("\t--------------")
        option = input("\n Qual data pretende? ")
        return datas[int(option) - 1]['id']
    else:
        print("Não há datas para este evento.")


def inserir_nova_data(nome_espetaculo):
    if nome_espetaculo is None:
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
    if username is None:
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


def lugares_sala():
    cur.execute(
        f"SELECT id FROM Lugares")
    return [item[0] for item in cur.fetchall()]


def lugares_sala_reservados(data_espetaculo):
    cur.execute(
        f"SELECT lugar FROM User_espetaculo_lugar WHERE data_espetaculo='{data_espetaculo}'")
    return [item[0] for item in cur.fetchall()]


def escolha_quantidade(lugares_possiveis):
    while True:
        quantidade = input("\nQuantos lugares pretende reservar? ")
        if quantidade.isnumeric():
            if int(quantidade) > 0:
                if int(quantidade) <= lugares_possiveis:
                    return int(quantidade)
                else:
                    print("\033[91mNão existem lugares disponíveis suficientes.\033[0m")
            else:
                print("\033[91mTem de inserir um número maior que 0.\033[0m")
        else:
            print("\033[91mTem de inserir um número válido.\033[0m")


def inserir_novas_reservas(novareserva, data_espetaculo):
    ultima_reserva = cur.execute(f"INSERT INTO Reservas DEFAULT VALUES ").lastrowid


    for lugar in novareserva:
        cur.execute(
            f"INSERT INTO User_espetaculo_lugar(user, data_espetaculo, lugar, reserva) VALUES('{currentuser}', '{data_espetaculo}', '{lugar}', '{ultima_reserva}')")

    print("\n----------Lugares reservados com sucesso----------")


def reservar_bilhetes():
    # cur.execute(
    #    f"SELECT reservas FROM User_Espetaculos_Reservas WHERE data='{DateTime(data)}' AND espetaculo='{espetaculo}'")
    # result = cur.fetchall()
    # result_merged = [""]
    # for i in range(0, len(result)):
    #    result_merged[0] += (result[i][0])
    # lugares = []
    # if len(result) > 0:
    #    lugaresreservados = result_merged[0].split(" ")
    #    lugares = result_merged[0].split(" ")
    #    controller.convert_letters_in_numbers(lugaresreservados, letras)
    ##else:
    #    global sala
    #    sala = sala_backup
    # if not controller.check_if_is_full():
    #     mostrar_sala()
    #    isnum = False
    #   while not isnum:
    #      quantidade = input("\nQuantos lugares pretende reservar? ")
    #      if quantidade.isnumeric():
    #          if int(quantidade) > 0:
    #              quantidade = int(quantidade)
    #              isnum = True
    #          else:
    #              print("\033[91mTem de inserir um número maior que 0.\033[0m")
    #      else:
    #          print("\033[91mTem de inserir um número válido.\033[0m")

    #  manual_or_auto = input("Pretende a escolha manual ou automática? (Manual/Auto):")
    #  if manual_or_auto == "Manual":
    #      novareserva = escolha_manual(quantidade, lugares)
    #  elif manual_or_auto == "Auto":
    #      novareserva = escolha_auto(quantidade)

    # tosql = ""
    # for item in novareserva:
    #     if tosql == "":
    #         tosql += item
    #     else:
    #         tosql += " " + item
    # cur.execute(
    #     f"INSERT INTO User_Espetaculos_Reservas(username, espetaculo, data, reservas) VALUES('{currentuser}', '{espetaculo}', '{DateTime(data)}', '{tosql} ')")
    # print("\n----------Lugares reservados com sucesso----------")
    # menuUser()
    # else:
    #    print("\n\033[91mPedimos desculpa, mas a sala encontra-se esgotada.\033[0m")

    espetaculo = listar_espetaculos()
    data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    lugares = lugares_sala()
    lugares_reservados = lugares_sala_reservados(data_espetaculo)
    lugares_disponiveis = [x for x in lugares if x not in lugares_reservados]

    if lugares_disponiveis:
        controller.convert_letters_in_numbers(lugares_reservados, letras)
    else:
        print("\n\033[91mPedimos desculpa, mas a sala encontra-se esgotada.\033[0m")

    if len(lugares_disponiveis) > 0:
        mostrar_sala()
        quantidade = escolha_quantidade(len(lugares_disponiveis))
        manual_or_auto = input("Pretende a escolha manual ou automática? (Manual/Auto):")
        if manual_or_auto == "Manual":
            novareserva = escolha_manual(quantidade, lugares, lugares_disponiveis)
        elif manual_or_auto == "Auto":
            novareserva = escolha_auto(quantidade, lugares_disponiveis)

        inserir_novas_reservas(novareserva, data_espetaculo)
    else:
        print("\n\033[91mPedimos desculpa, mas a sala encontra-se esgotada.\033[0m")


def escolha_manual(quantidade, lugares, lugares_disponiveis):
    novareserva = []
    for i in range(0, quantidade):
        while True:
            lugar = input("Escolha o lugar: ").upper()
            if lugar not in lugares:
                print("\n\033[91mALERTA: Esse lugar não existe.\n\033[0m")
            else:
                if lugar not in lugares_disponiveis or lugar in novareserva:
                    print("\n\033[91mALERTA: Esse lugar já está escolhido.\n\033[0m")
                else:
                    novareserva.append(lugar)
                    break;
    return novareserva
        #count_to_approve = 0
        #while count_to_approve < 3:
        #    lugar = input("Escolha o lugar: ")
        #    if controller.check_letra(lugar):
        #        if lugar in lugares or lugar in novareserva:
        #            print("\n\033[91mALERTA: Esse lugar já está escolhido.\n\033[0m")
        #        else:
        #            count_to_approve += 1
        #        if ((lugar[0] == "A" or lugar[0] == "F") and ((int(lugar[1:3]) > 2 and int(lugar[1:3]) < 6) or (
        #                int(lugar[1:3]) > 9 and int(lugar[1:3]) < 13))):
        #            print("\n\033[91mALERTA: Esse lugar não existe.\n\033[0m")
        #        else:
        #            count_to_approve += 1
        #        novareserva.append(lugar)
        #        count_to_approve += 1
        #    else:
        #        print("\n\033[91mO lugar que inseriu não está correto.\n\033[0m")


    return novareserva


def escolha_auto(quantidade):
    novareserva = []
    if quantidade == 1:
        novareserva = look_for_one(quantidade)
        return novareserva
    elif quantidade % 2 == 0 and quantidade > 1:
        novareserva = look_for_even(quantidade)
        return novareserva
    elif quantidade % 2 != 0 and quantidade > 1:
        novareserva = look_for_odd(quantidade)
        print(novareserva)
        return novareserva
    else:
        input()


def look_for_one(quantidade):
    novareserva = []
    for i in range(0, 11):
        for j in range(0, 13):
            if sala[i][j] == " ▢ ":
                novareserva.append(f"{letras[i]}{j + 1}")
                return novareserva
    return False


def look_for_even(quantidade):
    novareserva = []
    count = 0
    for i in range(0, 11):
        if sala[i][0] == " ▢ " and sala[i][1] == " ▢ ":
            novareserva.append(f"{letras[i]}{1}")
            novareserva.append(f"{letras[i]}{2}")
            count += 2
        if count == quantidade:
            return novareserva
    for i in range(0, 11):
        if sala[i][12] == " ▢ " and sala[i][13] == " ▢ ":
            novareserva.append(f"{letras[i]}{13}")
            novareserva.append(f"{letras[i]}{14}")
            count += 2
        if count == quantidade:
            return novareserva
    for i in range(0, 11):
        for j in range(2, 12):
            if (sala[i][j] == " ▢ " and sala[i][j + 1] == " ▢ ") or (sala[i][j] == "VIP" and sala[i][j + 1] == "VIP"):
                if f"{letras[i]}{j + 1}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{letras[i]}{j + 1}")
                    novareserva.append(f"{letras[i]}{j + 2}")
                    count += 2
            if count == quantidade:
                return novareserva
    for i in range(0, 11):
        for j in range(0, 13):
            if sala[i][j] == " ▢ ":
                novareserva.append(f"{letras[i]}{j + 1}")
                count += 1
            if count == quantidade:
                return novareserva


def look_for_odd(quantidade):
    novareserva = []
    count = 0

    countall = 0
    for i in range(0, 11):
        for j in range(2, 12):
            if j + quantidade < 12:
                countall = 0
                for k in range(j, j + quantidade):
                    if (sala[i][j] == " ▢ " or sala[i][j] == "VIP"):
                        countall += 1
                    if countall == quantidade:
                        for n in range(j, j + quantidade):
                            novareserva.append(f"{letras[i]}{n + 1}")
                        return novareserva

    print(novareserva)
    for i in range(0, 11):
        for j in range(2, 12):
            if (sala[i][j] == " ▢ " and sala[i][j + 1] == " ▢ ") or (sala[i][j] == "VIP" and sala[i][j + 1] == "VIP"):
                if f"{letras[i]}{j + 1}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{letras[i]}{j + 1}")
                    novareserva.append(f"{letras[i]}{j + 2}")
                    count += 2
            if count == quantidade:
                return novareserva
    print("center:", novareserva)

    if (quantidade - count) % 2 != 0 and (quantidade - count) > 1:
        for i in range(0, 11):
            if (quantidade - count) > 1:  # SE AINDA SOBRAR MAIS QUE UMA PESSOA
                if sala[i][0] == " ▢ " and sala[i][1] == " ▢ ":
                    novareserva.append(f"{letras[i]}{1}")
                    novareserva.append(f"{letras[i]}{2}")
                    count += 2
                if count == quantidade:
                    return novareserva
            else:
                if sala[i][0] == " ▢ ":
                    novareserva.append(f"{letras[i]}{1}")
                    return novareserva
                elif sala[i][0] == " ▢ ":
                    novareserva.append(f"{letras[i]}{2}")
                    return novareserva
        print("left:", novareserva)

        for i in range(0, 11):
            if (quantidade - count) > 1:  # SE AINDA SOBRAR MAIS QUE UMA PESSOA
                if sala[i][12] == " ▢ " and sala[i][13] == " ▢ ":
                    novareserva.append(f"{letras[i]}{13}")
                    novareserva.append(f"{letras[i]}{14}")
                    count += 2
                if count == quantidade:
                    return novareserva
            else:
                if sala[i][0] == " ▢ ":
                    novareserva.append(f"{letras[i]}{1}")
                    return novareserva
                elif sala[i][0] == " ▢ ":
                    novareserva.append(f"{letras[i]}{2}")
                    return novareserva
        print("right:", novareserva)

        for i in range(0, 11):
            for j in range(0, 13):
                if sala[i][j] == " ▢ ":
                    novareserva.append(f"{letras[i]}{j + 1}")
                    count += 1
                if count == quantidade:
                    return novareserva
    else:
        for i in range(0, 11):
            if sala[i][0] == " ▢ " and sala[i][1] == " ▢ ":
                novareserva.append(f"{letras[i]}{1}")
                novareserva.append(f"{letras[i]}{2}")
                count += 2
            if count == quantidade:
                return novareserva

        for i in range(0, 11):
            if sala[i][12] == " ▢ " and sala[i][13] == " ▢ ":
                novareserva.append(f"{letras[i]}{13}")
                novareserva.append(f"{letras[i]}{14}")
                count += 2
            if count == quantidade:
                return novareserva
        for i in range(0, 11):
            for j in range(0, 13):
                if sala[i][j] == " ▢ ":
                    novareserva.append(f"{letras[i]}{j + 1}")
                    count += 1
                if count == quantidade:
                    return novareserva
    print(novareserva)


def data_espetaculo_de_reserva(reserva):
    return cur.execute(
        f"SELECT data_espetaculo FROM User_espetaculo_lugar WHERE reserva='{reserva}'").fetchone()[0]



def alterar_reserva():
    espetaculo = listar_espetaculos_user()
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo)
        lugares = lugares_sala()
        data_espetaculo = data_espetaculo_de_reserva(reserva)
        apagar_reserva(reserva)
        lugares_reservados = lugares_sala_reservados(data_espetaculo)
        lugares_disponiveis = [x for x in lugares if x not in lugares_reservados]
        quantidade = escolha_quantidade(len(lugares_disponiveis))
        novareserva = escolha_manual(quantidade, lugares, lugares_disponiveis)
        inserir_novas_reservas(novareserva, data_espetaculo)


def apagar_reserva(reserva):
    cur.execute(
        f" DELETE FROM User_espetaculo_lugar WHERE reserva = '{reserva}'")
    cur.execute(
        f" DELETE FROM Reservas WHERE id = '{reserva}'")


def cancelar_reserva():
    espetaculo = listar_espetaculos_user()
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo)
        apagar_reserva(reserva)



def listar_espetaculos_user():
    i = 0
    espetaculos = []
    for espetaculo in cur.execute(
            f"SELECT DISTINCT espetaculo FROM User_espetaculo_lugar uel INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id WHERE user='{currentuser}'"):
        if i == 0:
            print("\n------Lista de Espetáculos------")
        i += 1
        espetaculos.append(espetaculo[0])
        print(f"{i}: {espetaculo[0]} ")
    if len(espetaculos) == 0:
        print("\n------Não tem espetáculos reservados------")
        return None
    print("---------------------------------")
    option = input("Escolha o Espetáculo: ")
    selected = espetaculos[int(option) - 1]
    return selected


def listar_reservas_utilizador(espetaculo):
    i = 0
    reservas = []
    print("\n------Lista de Reservas------")
    mapa_reservas = mapa_datas_lugares(espetaculo)
    for reserva in mapa_reservas.keys():
        i += 1
        print(f"{i}: Data- {mapa_reservas.get(reserva)[0]} Bilhetes- {mapa_reservas.get(reserva)[1]}")
        reservas.append(reserva)
    print("---------------------------------")
    option = input("Escolha a Reserva: ")
    return reservas[int(option) - 1]


def mapa_datas_lugares(espetaculo):
    map = {}
    for item in cur.execute(
            f"SELECT de.data, uel.lugar, uel.reserva "
            f"FROM User_espetaculo_lugar uel "
            f"INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id "
            f"INNER JOIN Lugares l ON uel.lugar = l.id "
            f"WHERE uel.user='{currentuser}' AND espetaculo='{espetaculo}' "
            f"ORDER BY l.fila, l.coluna"):
        if map.get(item[2]) is None:
            map[item[2]] = [item[0], item[1]]
        else:
            temp = map[item[2]]
            temp[1] = temp[1] + " " + item[1]
            map[item[2]] = temp
    return map
