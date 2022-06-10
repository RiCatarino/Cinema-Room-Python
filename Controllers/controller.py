import sqlite3
from xmlrpc.client import DateTime
from Models import model as mod
from Views import view

con = sqlite3.connect('projeto.db')
cur = con.cursor()

has_txn_open = False


def inserir_nova_data(name, date):
    cur.execute(f"SELECT * FROM Datas_espetaculo WHERE data='{DateTime(date)}' AND espetaculo='{name}'")
    result = cur.fetchone()
    if result:
        print("Este espetáculo já tem uma sessão nessa data.")
        return False
    mod.inserir_nova_data(name, date)
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
    if int(input[1:3]) < 1 or int(input[1:3]) > 14:
        return False
    return True


def convert_letters_in_numbers(lista, letras):
    for i in range(0, len(lista)):
        for k in range(0, len(letras)):
            if lista[i][:1] == letras[k]:
                lista[i] = lista[i].replace(str(letras[k]), str(letras.index(letras[k])) + " ")
    list_to_print = []
    mod.sala = mod.sala_backup
    for item in range(0, len(lista)):
        list_to_print.append(str(lista[item]).split(" "))
    for item in range(0, len(list_to_print)):
        if list_to_print[item] != ['']:
            mod.sala[int(list_to_print[item][0])][int(list_to_print[item][1]) - 1] = "\033[91m x \033[0m"


def check_if_is_full():
    for i in range(0, 11):
        for j in range(0, 13):
            if mod.sala[i][j] == " ▢ ":
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


def get_total_reserva(novareserva):
    total = 0
    for item in novareserva:
        if item == "F6" or item == "F7" or item == "F8" or item == "F8" or item == "A6" or item == "A7" or item == "A8" or item == "A9":
            total += 12
        else:
            total += 4
    return total


def login():
    global currentuser
    username = input("Username: ")
    password = input("Password: ")
    if mod.checkUser(username, password):
        currentuser = username
        if mod.checkAdmin(username, password):
            print(f"\n---------- Olá {currentuser}, administrador ----------")
            view.menuAdmin()
        else:
            print(f"\n---------- Olá {currentuser} ----------")
            view.menuUser()
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
        inserir_nova_data(name, newdate)
        view.menuAdmin()


def listar_espetaculos():
    i = 0
    print("\n------Lista de Espetáculos------")
    espetaculos = []
    for espetaculo in cur.execute("SELECT nome FROM Espetaculos"):
        i += 1
        espetaculos.append(espetaculo[0])
        print(f"{i}: {espetaculo[0]} ")
    print("---------------------------------")
    option = handle_inp("Escolha o Espetáculo: ")
    selected = espetaculos[int(option) - 1]
    return selected


def listar_datas_espetaculo(nome):
    print(f"\n------ Datas do espetáculo {nome} ----")
    print("\n\t--------------")
    for date in cur.execute(f"SELECT data FROM Datas_espetaculo WHERE espetaculo='{nome}'"):
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
        option = handle_inp("\n Qual data pretende? ")
        return datas[int(option) - 1]['id']
    else:
        print("Não há datas para este evento.")


def inserir_nova_data(nome_espetaculo):
    if nome_espetaculo is None:
        nome_espetaculo = listar_espetaculos()
        listar_datas_espetaculo(nome_espetaculo)
    ano = pedir_ano()
    mes = pedir_mes()
    dia = pedir_dia()

    novadata = f"{str(dia).zfill(2)}/{str(mes).zfill(2)}/{str(ano).zfill(2)}"
    if inserir_nova_data(nome_espetaculo, novadata):
        print("\n---------- Sessão adicionada com sucesso. ----------")
        view.menuAdmin()
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
    if check_utilizador(username):
        password = input("\nNova password: ")
        repeatpassword = input("\nRepita a nova password: ")
        if password == repeatpassword:
            mod.change_password(username, password)
            print("\n------Password Alterada com sucesso.------\n")
            view.menuAdmin()
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
        mod.change_password(currentuser, password)
        print("\n------Password Alterada com sucesso.------\n")
        view.main()
    else:
        print("\n------As password não coincidem.------\n")
        alterar_password()


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
        quantidade = handle_inp("\nQuantos lugares pretende reservar? ")
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
    lugares = ""

    for lugar in novareserva:
        cur.execute(
            f"INSERT INTO User_espetaculo_lugar(user, data_espetaculo, lugar, reserva) VALUES('{currentuser}', '{data_espetaculo}', '{lugar}', '{ultima_reserva}')")
        lugares += lugar + " "
    con.commit()
    print(f"Lugares reservados: {lugares}")
    print("\n----------Lugares reservados com sucesso----------")


def ver_sala():
    espetaculo = listar_espetaculos()
    data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    lugares_reservados = lugares_sala_reservados(data_espetaculo)
    convert_letters_in_numbers(lugares_reservados, mod.letras)
    mod.mostrar_sala()
    input("\n Para voltar prima 'Enter'...")
    ver_sala()


def reservar_bilhetes(espetaculo, data_espetaculo):
    global novareserva
    if espetaculo is None:
        espetaculo = listar_espetaculos()
        data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    lugares = lugares_sala()
    lugares_reservados = lugares_sala_reservados(data_espetaculo)
    lugares_disponiveis = [x for x in lugares if x not in lugares_reservados]
    if lugares_disponiveis:
        convert_letters_in_numbers(lugares_reservados, mod.letras)
    else:
        print("\n\033[91mPedimos desculpa, mas a sala encontra-se esgotada.\033[0m")
        reservar_bilhetes(None, None)

    if lugares_disponiveis:
        mod.mostrar_sala()
        quantidade = escolha_quantidade(len(lugares_disponiveis))
        manual_or_auto = handle_inp("Pretende a escolha manual ou automática? (Manual/Auto):")
        if manual_or_auto == "Manual":
            novareserva = escolha_manual(quantidade, lugares, lugares_disponiveis)
        elif manual_or_auto == "Auto":
            novareserva = escolha_auto(quantidade)
        decisao = handle_inp(
            f"O total da sua reserva é {get_total_reserva(novareserva)}€, pretende continuar? (Sim/Não)")

        if decisao == "Sim":
            pass
        else:
            view.menuUser()

        inserir_novas_reservas(novareserva, data_espetaculo)
    else:
        print("\n\033[91mPedimos desculpa, mas a sala encontra-se esgotada.\033[0m")


def escolha_manual(quantidade, lugares, lugares_disponiveis):
    novareserva = []
    for i in range(0, quantidade):
        lugar = handle_inp("Escolha o lugar: ").upper()
        if lugar not in lugares:
            print("\n\033[91mALERTA: Esse lugar não existe.\n\033[0m")
        else:
            if lugar not in lugares_disponiveis or lugar in novareserva:
                print("\n\033[91mALERTA: Esse lugar já está escolhido.\n\033[0m")
            else:
                novareserva.append(lugar)
    return novareserva


def escolha_auto(quantidade):
    novareserva = []
    for i in range(0, 11):
        for j in range(2, 11):
            if quantidade - len(novareserva) > 1:
                all = 0
                for k in range(2, 11):
                    if mod.sala[i][k] == " ▢ ":
                        all += 1
                if all >= quantidade:
                    for k in range(2, 11):
                        if (mod.sala[i][k] == " ▢ ") and f"sala[i]{k + 1}" not in novareserva:
                            novareserva.append(f"{mod.letras[i]}{k + 1}")
                            if quantidade == len(novareserva):
                                return novareserva
                elif (mod.sala[i][j] == " ▢ " and mod.sala[i][j + 1] == " ▢ ") or (
                        mod.sala[i][j] == "VIP" and mod.sala[i][j + 1] == "VIP"):
                    if f"{mod.letras[i]}{j + 1}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{mod.letras[i]}{j + 1}")
                        novareserva.append(f"{mod.letras[i]}{j + 2}")
            else:
                break

    for i in range(0, 11):
        if quantidade - len(novareserva) > 1:
            if mod.sala[i][0] == " ▢ " and mod.sala[i][1] == " ▢ ":
                if f"{mod.letras[i]}{1}" in novareserva or f"{mod.letras[i]}{2}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{mod.letras[i]}{1}")
                    novareserva.append(f"{mod.letras[i]}{2}")
        else:
            break
    for i in range(0, 11):
        if quantidade - len(novareserva) > 1:
            if mod.sala[i][12] == " ▢ " and mod.sala[i][13] == " ▢ ":
                if f"{mod.letras[i]}{13}" in novareserva or f"{mod.letras[i]}{14}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{mod.letras[i]}{13}")
                    novareserva.append(f"{mod.letras[i]}{14}")
        else:
            break
            ##PROCURA NO MEIO POR UM LUGAR VAZIO ENTRE 2 OCUPADOS
    for i in range(0, 11):
        for j in range(2, 12):
            if 2 < j < 11:
                if mod.sala[i][j - 1] != " ▢ " and mod.sala[i][j] == " ▢ " and mod.sala[i][j + 1] != " ▢ ":
                    if f"{mod.letras[i]}{j + 1}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{mod.letras[i]}{j + 1}")
            # SE ESTIVER NAS PONTAS DO MEIO
            elif j == 2:
                if mod.sala[i][j] == " ▢ " and mod.sala[i][j + 1] != " ▢ ":
                    if f"{mod.letras[i]}{j + 1}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{mod.letras[i]}{j + 1}")
            elif j == 11:
                if mod.sala[i][j] == " ▢ " and mod.sala[i][j - 1] != " ▢ ":
                    if f"{mod.letras[i]}{j + 1}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{mod.letras[i]}{j + 1}")
            if len(novareserva) == quantidade:
                return novareserva
    for i in range(0, 11):
        if mod.sala[i][0] == " ▢ " and mod.sala[i][1] != " ▢ ":
            if f"{mod.letras[i]}{1}" in novareserva:
                pass
            else:
                novareserva.append(f"{mod.letras[i]}{1}")
        elif mod.sala[i][0] != " ▢ " and mod.sala[i][1] == " ▢ ":
            if f"{mod.letras[i]}{2}" in novareserva:
                pass
            else:
                novareserva.append(f"{mod.letras[i]}{2}")
        if len(novareserva) == quantidade:
            return novareserva
    for i in range(0, 11):
        if mod.sala[i][12] == " ▢ " and mod.sala[i][13] != " ▢ ":
            if f"{mod.letras[i]}{13}" in novareserva:
                pass
            else:
                novareserva.append(f"{mod.letras[i]}{13}")
        elif mod.sala[i][12] != " ▢ " and mod.sala[i][13] == " ▢ ":
            if f"{mod.letras[i]}{14}" in novareserva:
                pass
            else:
                novareserva.append(f"{mod.letras[i]}{14}")
        if len(novareserva) == quantidade:
            return novareserva
    for i in range(0, 11):
        for j in range(0, 13):
            if mod.sala[i][j] == " ▢ ":
                if f"{mod.letras[i]}{j + 1}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{mod.letras[i]}{j + 1}")
                if len(novareserva) == quantidade:
                    return novareserva


def data_espetaculo_de_reserva(reserva):
    return cur.execute(
        f"SELECT data_espetaculo FROM User_espetaculo_lugar WHERE reserva='{reserva}'").fetchone()[0]


def apagar_reserva(reserva):
    cur.execute(
        f" DELETE FROM User_espetaculo_lugar WHERE reserva = '{reserva}'")
    cur.execute(
        f" DELETE FROM Reservas WHERE id = '{reserva}'")



def alterar_reserva():
    global has_txn_open
    espetaculo = listar_espetaculos_user()
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo)
        cur.execute(f"SELECT data_espetaculo FROM User_espetaculo_lugar WHERE reserva ='{reserva}'")
        data_espetaculo = cur.fetchone()[0]
        cur.execute("begin")
        has_txn_open = True
        apagar_reserva(reserva)
        reservar_bilhetes(espetaculo, data_espetaculo)
        con.commit()
        has_txn_open = False


def cancelar_reserva():
    espetaculo = listar_espetaculos_user()
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo)
        apagar_reserva(reserva)
        con.commit()
        view.menuUser()


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
    option = handle_inp("Escolha o Espetáculo: ")
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
    option = handle_inp("Escolha a Reserva: ")
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


def pedir_ano():
    while True:
        ano = input("Por favor, insira o ano: ")
        try:
            ano = int(ano)
            if ano == 2022 or ano == 2023:
                return ano
        except:
            print("\033[91m Por favor insira o ano em formato numérico.\033[0m")


def pedir_mes():
    while True:
        mes = input("Por favor, insira o mês(0-12): ")
        try:
            mes = int(mes)
            if mes > 0 and mes < 13:
                return mes
        except:
            print("\033[91m Por favor insira um mês válido.\033[0m")


def pedir_dia():
    while True:
        dia = input("Por favor, insira o dia(0-31): ")
        try:
            dia = int(dia)
            if dia > 0 and dia < 32:
                return dia
        except:
            print("\033[91m Por favor insira um dia válido.\033[0m")


def bilheteira_por_dia():
    ano = pedir_ano()
    mes = pedir_mes()
    dia = pedir_dia()
    datas = []
    for item in cur.execute(
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}' AND strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{mes.zfill(2)}' AND strftime('%d', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{dia.zfill(2)}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)
    print(f"Total no dia {dia}/{mes}/{ano}: {total}€")
    view.menuBilheteira()


def bilheteira_por_mes():
    ano = pedir_ano()
    mes = pedir_mes()
    datas = []
    for item in cur.execute(
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}' AND strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{mes.zfill(2)}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)
    print(f"Total no mês {mes}/{ano}: {total}€")
    view.menuBilheteira()


def bilheteira_por_ano():
    ano = pedir_ano()
    datas = []
    total = 0
    for item in cur.execute(
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)
    print(f"Total no ano {ano}: {total}€")
    view.menuBilheteira()


def bilheteira_por_espetaculo():
    espetaculo = listar_espetaculos()
    datas = []
    total = 0
    for item in cur.execute(f"SELECT id FROM Datas_espetaculo WHERE espetaculo='{espetaculo}'"):
        datas.append(item[0])

    total = get_total_bilheteira(datas)
    print(f"Total do espetaculo '{espetaculo}': {total}€")
    view.menuBilheteira()


def bilheteira_por_sessao():
    espetaculo = listar_espetaculos()
    data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    lugares_reservados = lugares_sala_reservados(data_espetaculo)
    total = 0
    for item in lugares_reservados:
        if item == "F6" or item == "F7" or item == "F8" or item == "F8" or item == "A6" or item == "A7" or item == "A8" or item == "A9":
            total += 12
        else:
            total += 4
    print(f"Total da sessão: {total}€")
    view.menuBilheteira()


def handle_inp(message):
    user_input = input(message)
    if user_input.upper() == "EXIT":
        if check_utilizador(currentuser):
            view.menuUser()
        else:
            view.menuAdmin()
    return user_input
