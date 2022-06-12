import sqlite3
from xmlrpc.client import DateTime
from Models import model as mod
from Views import view

<<<<<<< HEAD
con = sqlite3.connect('projeto.db')
=======
con = sqlite3.connect('projeto.db', isolation_level=None)
>>>>>>> 7fc5202 (Final)
cur = con.cursor()

has_txn_open = False



def check_user_exists(username):
    cur.execute(f"SELECT * FROM Users WHERE username='{username}'")
    if cur.fetchone() != None:
        return True
    else:
        return False


def checkUserLogin(username, password):
    cur.execute(f"SELECT * FROM Users WHERE username='{username}' AND password='{password}'")
    if cur.fetchone() != None:
        return True
    else:
        return False

def checkAdminLogin(username):
    cur.execute(f"SELECT role FROM Users WHERE username='{username}'")
    if cur.fetchone()[0] == "admin":
        return True
    else:
        return False

def verificar_data_duplicada(name, date):
    cur.execute(f"SELECT * FROM Datas_espetaculo WHERE data='{DateTime(date)}' AND espetaculo='{name}'")
    result = cur.fetchone()
<<<<<<< HEAD
    if result:
        print("Este espetáculo já tem uma sessão nessa data.")
        return False
    mod.inserir_nova_data(name, date)
    return True
=======
    return result    
>>>>>>> 7fc5202 (Final)


def get_espetaculos():
    for espetaculo in cur.execute("SELECT id, nome FROM Espetaculos"):
        print(f"\nID: {espetaculo[0]} Nome: {espetaculo[1]} ")

<<<<<<< HEAD

def check_utilizador(username):
    cur.execute(f"SELECT * FROM Users WHERE username='{username}' AND role='User'")
    result = cur.fetchone()
    if result:
        return True
    return False


=======
>>>>>>> 7fc5202 (Final)
def check_letra(input):
    letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    if input[0][0] not in letras:
        return False
    if len(input) > 3:
        return False
    if int(input[1:3]) < 1 or int(input[1:3]) > 14:
        return False
    return True
<<<<<<< HEAD

=======
>>>>>>> 7fc5202 (Final)

def convert_letters_in_numbers(lista, letras):
    for i in range(0, len(lista)):
        for k in range(0, len(letras)):
            if lista[i][:1] == letras[k]:
                lista[i] = lista[i].replace(str(letras[k]), str(letras.index(letras[k])) + " ")
    list_to_print = []
<<<<<<< HEAD
    mod.sala = mod.sala_backup
=======
    view.sala = view.sala_backup
>>>>>>> 7fc5202 (Final)
    for item in range(0, len(lista)):
        list_to_print.append(str(lista[item]).split(" "))
    for item in range(0, len(list_to_print)):
        if list_to_print[item] != ['']:
<<<<<<< HEAD
            mod.sala[int(list_to_print[item][0])][int(list_to_print[item][1]) - 1] = "\033[91m x \033[0m"

=======
            view.sala[int(list_to_print[item][0])][int(list_to_print[item][1]) - 1] = "\033[91m x \033[0m"
>>>>>>> 7fc5202 (Final)

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
<<<<<<< HEAD
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
=======
    username = view.pedir_username()
    password = view.pedir_password()
    if checkUserLogin(username, password):
        view.currentuser = username
        if checkAdminLogin(username):
            view.menuAdmin()
        else:
            view.menuUser()
    else:
        view.print_password_errada()
>>>>>>> 7fc5202 (Final)
        login()


def signup(role):
<<<<<<< HEAD
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
=======
    username = view.pedir_username()
    password = view.pedir_password()
    repeatpassword = view.pedir_repeat_nova_password()
    while password != repeatpassword:
        view.print_password_diferentes()
        repeatpassword = view.pedir_repeat_nova_password()
    mod.inserir_utilizador(username, password, role)
    view.print_registo_admin_sucesso()

def inserir_espetaculo():
    name = view.pedir_nome_espetaculo()
    mod.inserir_espetaculo(name)
    option = view.questao_novo_espetaculo()
    if option == "Sim":
        inserir_nova_data(name)
    else:
        view.menuAdmin()

def listar_espetaculos():
    i = 0
    view.print_cabecalho_lista_espetaculos()
>>>>>>> 7fc5202 (Final)
    espetaculos = []
    for espetaculo in cur.execute("SELECT nome FROM Espetaculos"):
        i += 1
        espetaculos.append(espetaculo[0])
<<<<<<< HEAD
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

=======
        view.print_lista_espetaculos(i, espetaculo)
    view.print_line()
    option = view.pedir_escolha_espetaculo()
    selected = espetaculos[int(option) - 1]
    return selected

def listar_datas_espetaculo(nome):
    view.print_cabecalho_lista_datas(nome)
    view.print_line()
    for date in cur.execute(f"SELECT data FROM Datas_espetaculo WHERE espetaculo='{nome}'"):
        view.print_lista_datas(date)
    view.print_line()
>>>>>>> 7fc5202 (Final)

def listar_datas_espetaculo_para_reserva(nome):
    datas = []
    for data in cur.execute(f"SELECT id, data FROM Datas_espetaculo WHERE espetaculo='{nome}'"):
        datas.append({"id": data[0], "data": data[1]})
<<<<<<< HEAD

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

=======
    if datas:
        view.print_cabecalho_lista_datas(nome)
        view.print_line()
        for i in range(0, len(datas)):
            view.print_lista_datas_para_reserva(i, datas)
        view.print_line()
        option = view.pedir_escolha_data_espetaculo()
        return datas[int(option) - 1]['id']
    else:
        view.print_sem_datas()
        reservar_bilhetes(None, None)
>>>>>>> 7fc5202 (Final)

def inserir_nova_data(nome_espetaculo):
    if nome_espetaculo is None:
        nome_espetaculo = listar_espetaculos()
        listar_datas_espetaculo(nome_espetaculo)
<<<<<<< HEAD
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

=======
    ano = view.pedir_ano()
    mes = view.pedir_mes()
    dia = view.pedir_dia()
    
    novadata = f"{str(dia).zfill(2)}/{str(mes).zfill(2)}/{str(ano).zfill(2)}"
    if verificar_data_duplicada(nome_espetaculo, novadata):
        view.print_data_duplicada()
        inserir_nova_data(nome_espetaculo)
    else:
        mod.inserir_nova_data(nome_espetaculo, novadata)
        view.print_sessoa_adicionada_sucesso()
        view.askforenter()
        view.menuAdmin()

def listar_utilizadores():
    view.print_cabecalho_lista_users()
    for user in cur.execute("SELECT username FROM Users WHERE role='User'"):
        view.print_users(user)
        view.print_line()
>>>>>>> 7fc5202 (Final)

def alterar_password_by_utilizador(error, username):
    if not error:
        listar_utilizadores()
    if username is None:
<<<<<<< HEAD
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
=======
        username = view.pedir_username()
    if check_user_exists(username):
        password = view.pedir_nova_password()
        repeatpassword = view.pedir_repeat_nova_password()
        if password == repeatpassword:
            mod.change_password(username, password)
            view.print_password_sucesso()
            view.askforenter()
            view.menuAdmin()
        else:
            view.print_password_diferentes()
            alterar_password_by_utilizador(True, username)
    else:
        view.print_user_nao_existe()
>>>>>>> 7fc5202 (Final)
        alterar_password_by_utilizador(True, None)


def alterar_password():
<<<<<<< HEAD
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


=======
    password = view.pedir_nova_password()
    repeatpassword = view.pedir_repeat_nova_password()
    if password == repeatpassword:
        mod.change_password(view.currentuser, password)
        view.print_password_sucesso()
        view.askforenter()
        view.main()
    else:
        view.print_password_diferentes()
        alterar_password()

>>>>>>> 7fc5202 (Final)
def lugares_sala():
    cur.execute(
        f"SELECT id FROM Lugares")
    return [item[0] for item in cur.fetchall()]

<<<<<<< HEAD

=======
>>>>>>> 7fc5202 (Final)
def lugares_sala_reservados(data_espetaculo):
    cur.execute(
        f"SELECT lugar FROM User_espetaculo_lugar WHERE data_espetaculo='{data_espetaculo}'")
    return [item[0] for item in cur.fetchall()]

<<<<<<< HEAD

def escolha_quantidade(lugares_possiveis):
    while True:
        quantidade = handle_inp("\nQuantos lugares pretende reservar? ")
=======
def escolha_quantidade(lugares_possiveis):
    while True:
        quantidade = view.pedir_quantidade_bilhetes()
>>>>>>> 7fc5202 (Final)
        if quantidade.isnumeric():
            if int(quantidade) > 0:
                if int(quantidade) <= lugares_possiveis:
                    return int(quantidade)
                else:
<<<<<<< HEAD
                    print("\033[91mNão existem lugares disponíveis suficientes.\033[0m")
            else:
                print("\033[91mTem de inserir um número maior que 0.\033[0m")
        else:
            print("\033[91mTem de inserir um número válido.\033[0m")

=======
                    view.print_sem_lugares_disponiveis()
            else:
                view.print_maior_que_zero()
        else:
            view.print_numero_invalido()
>>>>>>> 7fc5202 (Final)

def inserir_novas_reservas(novareserva, data_espetaculo):
    ultima_reserva = cur.execute(f"INSERT INTO Reservas DEFAULT VALUES ").lastrowid
    lugares = ""
<<<<<<< HEAD

    for lugar in novareserva:
        cur.execute(
            f"INSERT INTO User_espetaculo_lugar(user, data_espetaculo, lugar, reserva) VALUES('{currentuser}', '{data_espetaculo}', '{lugar}', '{ultima_reserva}')")
        lugares += lugar + " "
    con.commit()
    print(f"Lugares reservados: {lugares}")
    print("\n----------Lugares reservados com sucesso----------")

=======
    for lugar in novareserva:
        cur.execute(
            f"INSERT INTO User_espetaculo_lugar(user, data_espetaculo, lugar, reserva) VALUES('{view.currentuser}', '{data_espetaculo}', '{lugar}', '{ultima_reserva}')")
        lugares += lugar + " "
    view.print_lugares_reservados(lugares)
    view.print_reserva_sucesso()
    view.askforenter()
>>>>>>> 7fc5202 (Final)

def ver_sala():
    espetaculo = listar_espetaculos()
    data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    lugares_reservados = lugares_sala_reservados(data_espetaculo)
<<<<<<< HEAD
    convert_letters_in_numbers(lugares_reservados, mod.letras)
    mod.mostrar_sala()
    input("\n Para voltar prima 'Enter'...")
    ver_sala()

=======
    convert_letters_in_numbers(lugares_reservados, view.letras)
    view.mostrar_sala()
    
>>>>>>> 7fc5202 (Final)

def reservar_bilhetes(espetaculo, data_espetaculo):
    global novareserva
    if espetaculo is None:
        espetaculo = listar_espetaculos()
        data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    lugares = lugares_sala()
    lugares_reservados = lugares_sala_reservados(data_espetaculo)
<<<<<<< HEAD
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
=======

    lugares_disponiveis = [x for x in lugares if x not in lugares_reservados]
    if lugares_disponiveis:
        convert_letters_in_numbers(lugares_reservados, view.letras)
        view.mostrar_sala()
        quantidade = escolha_quantidade(len(lugares_disponiveis))
        manual_or_auto = view.pedir_manual_auto()
>>>>>>> 7fc5202 (Final)
        if manual_or_auto == "Manual":
            novareserva = escolha_manual(quantidade, lugares, lugares_disponiveis)
        elif manual_or_auto == "Auto":
            novareserva = escolha_auto(quantidade)
<<<<<<< HEAD
        decisao = handle_inp(
            f"O total da sua reserva é {get_total_reserva(novareserva)}€, pretende continuar? (Sim/Não)")

        if decisao == "Sim":
            pass
        else:
            view.menuUser()

        inserir_novas_reservas(novareserva, data_espetaculo)
    else:
        print("\n\033[91mPedimos desculpa, mas a sala encontra-se esgotada.\033[0m")

=======
        decisao = view.pedir_confirmacao_total_reserva(novareserva)
        if decisao != "Sim":
            view.menuUser()
        inserir_novas_reservas(novareserva, data_espetaculo)
        view.menuUser()
    else:
        view.print_sala_esgotada()
        reservar_bilhetes(None, None)
>>>>>>> 7fc5202 (Final)

def escolha_manual(quantidade, lugares, lugares_disponiveis):
    novareserva = []
    for i in range(0, quantidade):
<<<<<<< HEAD
        lugar = handle_inp("Escolha o lugar: ").upper()
        if lugar not in lugares:
            print("\n\033[91mALERTA: Esse lugar não existe.\n\033[0m")
        else:
            if lugar not in lugares_disponiveis or lugar in novareserva:
                print("\n\033[91mALERTA: Esse lugar já está escolhido.\n\033[0m")
=======
        lugar = view.pedir_lugar()
        if lugar not in lugares:
            view.print_lugar_inexistente()
        else:
            if lugar not in lugares_disponiveis or lugar in novareserva:
                view.print_lugar_ja_escolhido()
>>>>>>> 7fc5202 (Final)
            else:
                novareserva.append(lugar)
    return novareserva

<<<<<<< HEAD

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

=======
def escolha_auto(quantidade):
    novareserva = []
    if quantidade == 2:
        for i in range(0, 11):
            if view.sala[i][0] == " ▢ " and view.sala[i][1] == " ▢ ":
                if f"{view.letras[i]}{1}" in novareserva or f"{view.letras[i]}{2}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{view.letras[i]}{1}")
                    novareserva.append(f"{view.letras[i]}{2}")
                    return novareserva
        for i in range(0, 11):
                if view.sala[i][12] == " ▢ " and view.sala[i][13] == " ▢ ":
                    if f"{view.letras[i]}{13}" in novareserva or f"{view.letras[i]}{14}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{view.letras[i]}{13}")
                        novareserva.append(f"{view.letras[i]}{14}")
                        return novareserva
    
    else:
        for i in range(0, 11):
            if quantidade - len(novareserva) > 1:
                all = 0
                for k in range(2, 12):
                    if view.sala[i][k] == " ▢ ":
                        all += 1
                if all >= quantidade or all == 10:
                    for k in range(2, 12):
                        if (view.sala[i][k] == " ▢ ") and f"sala[i]{k + 1}" not in novareserva:
                            novareserva.append(f"{view.letras[i]}{k + 1}")
                            if quantidade == len(novareserva):
                                return novareserva

        for i in range(0, 11):
            for j in range(2, 12):
                if quantidade - len(novareserva) > 1:
                    if (view.sala[i][j] == " ▢ " and view.sala[i][j + 1] == " ▢ ") or (
                            view.sala[i][j] == "VIP" and view.sala[i][j + 1] == "VIP"):
                        if f"{view.letras[i]}{j + 1}" in novareserva:
                            pass
                        else:
                            novareserva.append(f"{view.letras[i]}{j + 1}")
                            novareserva.append(f"{view.letras[i]}{j + 2}")
                                
        for i in range(0, 11):
            if quantidade - len(novareserva) > 1:
                if view.sala[i][0] == " ▢ " and view.sala[i][1] == " ▢ ":
                    if f"{view.letras[i]}{1}" in novareserva or f"{view.letras[i]}{2}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{view.letras[i]}{1}")
                        novareserva.append(f"{view.letras[i]}{2}")
            else:
                break
        for i in range(0, 11):
            if quantidade - len(novareserva) > 1:
                if view.sala[i][12] == " ▢ " and view.sala[i][13] == " ▢ ":
                    if f"{view.letras[i]}{13}" in novareserva or f"{view.letras[i]}{14}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{view.letras[i]}{13}")
                        novareserva.append(f"{view.letras[i]}{14}")
            else:
                break
                ##PROCURA NO MEIO POR UM LUGAR VAZIO ENTRE 2 OCUPADOS
        for i in range(0, 11):
            for j in range(2, 12):
                if 2 < j < 11:
                    if view.sala[i][j - 1] != " ▢ " and view.sala[i][j] == " ▢ " and view.sala[i][j + 1] != " ▢ ":
                        if f"{view.letras[i]}{j + 1}" in novareserva:
                            pass
                        else:
                            novareserva.append(f"{view.letras[i]}{j + 1}")
                # SE ESTIVER NAS PONTAS DO MEIO
                elif j == 2:
                    if view.sala[i][j] == " ▢ " and view.sala[i][j + 1] != " ▢ ":
                        if f"{view.letras[i]}{j + 1}" in novareserva:
                            pass
                        else:
                            novareserva.append(f"{view.letras[i]}{j + 1}")
                elif j == 11:
                    if view.sala[i][j] == " ▢ " and view.sala[i][j - 1] != " ▢ ":
                        if f"{view.letras[i]}{j + 1}" in novareserva:
                            pass
                        else:
                            novareserva.append(f"{view.letras[i]}{j + 1}")
                if len(novareserva) == quantidade:
                    return novareserva
        for i in range(0, 11):
            if view.sala[i][0] == " ▢ " and view.sala[i][1] != " ▢ ":
                if f"{view.letras[i]}{1}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{view.letras[i]}{1}")
            elif view.sala[i][0] != " ▢ " and view.sala[i][1] == " ▢ ":
                if f"{view.letras[i]}{2}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{view.letras[i]}{2}")
            if len(novareserva) == quantidade:
                return novareserva
        for i in range(0, 11):
            if view.sala[i][12] == " ▢ " and view.sala[i][13] != " ▢ ":
                if f"{view.letras[i]}{13}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{view.letras[i]}{13}")
            elif view.sala[i][12] != " ▢ " and view.sala[i][13] == " ▢ ":
                if f"{view.letras[i]}{14}" in novareserva:
                    pass
                else:
                    novareserva.append(f"{view.letras[i]}{14}")
            if len(novareserva) == quantidade:
                return novareserva
        for i in range(0, 11):
            for j in range(0, 13):
                if view.sala[i][j] == " ▢ ":
                    if f"{view.letras[i]}{j + 1}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{view.letras[i]}{j + 1}")
                    if len(novareserva) == quantidade:
                        return novareserva
>>>>>>> 7fc5202 (Final)

def data_espetaculo_de_reserva(reserva):
    return cur.execute(
        f"SELECT data_espetaculo FROM User_espetaculo_lugar WHERE reserva='{reserva}'").fetchone()[0]

<<<<<<< HEAD

def apagar_reserva(reserva):
    cur.execute(
        f" DELETE FROM User_espetaculo_lugar WHERE reserva = '{reserva}'")
    cur.execute(
        f" DELETE FROM Reservas WHERE id = '{reserva}'")



def alterar_reserva():
    global has_txn_open
=======
def alterar_reserva():
>>>>>>> 7fc5202 (Final)
    espetaculo = listar_espetaculos_user()
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo)
        cur.execute(f"SELECT data_espetaculo FROM User_espetaculo_lugar WHERE reserva ='{reserva}'")
        data_espetaculo = cur.fetchone()[0]
<<<<<<< HEAD
        cur.execute("begin")
        has_txn_open = True
        apagar_reserva(reserva)
        reservar_bilhetes(espetaculo, data_espetaculo)
        con.commit()
        has_txn_open = False


=======
        cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE reserva ='{reserva}'")
        cur.execute(f"DELETE FROM Reservas WHERE id ='{reserva}'")
        con.commit()
        reservar_bilhetes(espetaculo, data_espetaculo)
        
>>>>>>> 7fc5202 (Final)
def cancelar_reserva():
    espetaculo = listar_espetaculos_user()
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo)
<<<<<<< HEAD
        apagar_reserva(reserva)
        con.commit()
        view.menuUser()


=======
        mod.apagar_reserva(reserva)
        con.commit()
        view.askforenter()
        view.menuUser()

>>>>>>> 7fc5202 (Final)
def listar_espetaculos_user():
    i = 0
    espetaculos = []
    for espetaculo in cur.execute(
<<<<<<< HEAD
            f"SELECT DISTINCT espetaculo FROM User_espetaculo_lugar uel INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id WHERE user='{currentuser}'"):
        if i == 0:
            print("\n------Lista de Espetáculos------")
=======
            f"SELECT DISTINCT espetaculo FROM User_espetaculo_lugar uel INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id WHERE user='{view.currentuser}'"):
        if i == 0:
            view.print_cabecalho_lista_espetaculos()
>>>>>>> 7fc5202 (Final)
        i += 1
        espetaculos.append(espetaculo[0])
        print(f"{i}: {espetaculo[0]} ")
    if len(espetaculos) == 0:
<<<<<<< HEAD
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


=======
        view.print_sem_espetaculos_reservados()
        return None
    print("---------------------------------")
    option = view.pedir_escolha_espetaculo()
    selected = espetaculos[int(option) - 1]
    return selected

def listar_reservas_utilizador(espetaculo):
    i = 0
    reservas = []
    view.print_cabecalho_lista_reservas()
    mapa_reservas = mapa_datas_lugares(espetaculo)
    for reserva in mapa_reservas.keys():
        i += 1
        view.print_lista_reservas(i, mapa_reservas, reserva)
        reservas.append(reserva)
    view.print_line()
    option = view.pedir_escolha_reserva()
    return reservas[int(option) - 1]

>>>>>>> 7fc5202 (Final)
def mapa_datas_lugares(espetaculo):
    map = {}
    for item in cur.execute(
            f"SELECT de.data, uel.lugar, uel.reserva "
            f"FROM User_espetaculo_lugar uel "
            f"INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id "
            f"INNER JOIN Lugares l ON uel.lugar = l.id "
<<<<<<< HEAD
            f"WHERE uel.user='{currentuser}' AND espetaculo='{espetaculo}' "
=======
            f"WHERE uel.user='{view.currentuser}' AND espetaculo='{espetaculo}' "
>>>>>>> 7fc5202 (Final)
            f"ORDER BY l.fila, l.coluna"):
        if map.get(item[2]) is None:
            map[item[2]] = [item[0], item[1]]
        else:
            temp = map[item[2]]
            temp[1] = temp[1] + " " + item[1]
            map[item[2]] = temp
    return map

<<<<<<< HEAD

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
=======
def bilheteira_por_dia():
    ano = view.pedir_ano()
    mes = view.pedir_mes()
    dia = view.pedir_dia()
>>>>>>> 7fc5202 (Final)
    datas = []
    for item in cur.execute(
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}' AND strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{mes.zfill(2)}' AND strftime('%d', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{dia.zfill(2)}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)
<<<<<<< HEAD
    print(f"Total no dia {dia}/{mes}/{ano}: {total}€")
    view.menuBilheteira()


def bilheteira_por_mes():
    ano = pedir_ano()
    mes = pedir_mes()
=======
    view.print_total_bilheteira_dia(dia, mes, ano, total)
    view.askforenter()
    view.menuBilheteira()

def bilheteira_por_mes():
    ano = view.pedir_ano()
    mes = view.pedir_mes()
>>>>>>> 7fc5202 (Final)
    datas = []
    for item in cur.execute(
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}' AND strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{mes.zfill(2)}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)
<<<<<<< HEAD
    print(f"Total no mês {mes}/{ano}: {total}€")
    view.menuBilheteira()


def bilheteira_por_ano():
    ano = pedir_ano()
=======
    view.print_total_bilheteira_mes(mes, ano, total)
    view.askforenter()    
    view.menuBilheteira()

def bilheteira_por_ano():
    ano = view.pedir_ano()
>>>>>>> 7fc5202 (Final)
    datas = []
    total = 0
    for item in cur.execute(
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)
<<<<<<< HEAD
    print(f"Total no ano {ano}: {total}€")
    view.menuBilheteira()


=======
    view.print_total_bilheteira_ano(ano, total)
    view.askforenter()
    view.menuBilheteira()

>>>>>>> 7fc5202 (Final)
def bilheteira_por_espetaculo():
    espetaculo = listar_espetaculos()
    datas = []
    total = 0
    for item in cur.execute(f"SELECT id FROM Datas_espetaculo WHERE espetaculo='{espetaculo}'"):
        datas.append(item[0])
<<<<<<< HEAD

    total = get_total_bilheteira(datas)
    print(f"Total do espetaculo '{espetaculo}': {total}€")
    view.menuBilheteira()


=======
    total = get_total_bilheteira(datas)
    view.print_total_bilheteira_espetaculo(espetaculo, total)
    view.askforenter()
    view.menuBilheteira()

>>>>>>> 7fc5202 (Final)
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
<<<<<<< HEAD
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
=======
    view.print_total_bilheteira_sessao(data_espetaculo, espetaculo, total)
    view.askforenter()
    view.menuBilheteira()
    
def remover_espetaculo():
    espetaculo = listar_espetaculos()
    cur.execute(f"SELECT id FROM Datas_espetaculo WHERE espetaculo = '{espetaculo}'")
    datas = cur.fetchall()
    for data in datas:
        cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE data_espetaculo='{data[0]}'")
    for data in datas:
        cur.execute(f"DELETE FROM Datas_espetaculo WHERE id='{data[0]}'")
    cur.execute(f"DELETE FROM Espetaculos WHERE nome='{espetaculo}'")
    con.commit()
    view.print_sucesso_remocao(espetaculo)
    view.askforenter()
    view.menuAdmin()
    
def remover_sessao():
    espetaculo = listar_espetaculos()
    id_data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    cur.execute(f"SELECT data FROM Datas_espetaculo WHERE id='{id_data_espetaculo}'")
    data_espetaculo = cur.fetchone()[0]
    cur.execute(f"SELECT lugar FROM User_espetaculo_lugar WHERE data_espetaculo='{id_data_espetaculo}'")
    reservas = cur.fetchall()
    decisao = view.confirmar_remocao_sessao(len(reservas)).upper()
    if decisao == "SIM":
        cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE data_espetaculo ='{id_data_espetaculo}'")
        cur.execute(f"DELETE FROM Datas_espetaculo WHERE id='{id_data_espetaculo}'")
        con.commit()
        view.print_sucesso_remocao_sessao(data_espetaculo, espetaculo)
        view.askforenter()
        view.menuAdmin()
    else:
        view.menuAdmin()


    

def handle_inp(message):
    user_input = input(message)
    if user_input.upper() == "EXIT":
        if checkAdminLogin(view.currentuser):
            view.menuAdmin()
        else:
            view.menuUser()
    return user_input
>>>>>>> 7fc5202 (Final)
