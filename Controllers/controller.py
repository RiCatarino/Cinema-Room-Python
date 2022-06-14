import sqlite3
from xmlrpc.client import DateTime

from django.views import View
from Models import model as mod
from Views import view

con = sqlite3.connect('projeto.db')
cur = con.cursor()

pending = False

def check_user_exists(username):
    cur.execute(f"SELECT * FROM Users WHERE username='{username}'") #Query para percorrer por todos os registos o utilizador com aquele username
    if cur.fetchone() != None: #Se a query devolver algum valor, quer dizer que existe e devolve true
        return True
    else:
        return False

def checkUserLogin(username, password):
    cur.execute(f"SELECT * FROM Users WHERE username='{username}' AND password='{password}'") #Query para percorrer por todos os registos as credenciais inseridas
    if cur.fetchone() != None:#Se a query devolver algum valor, quer dizer que existe e devolve true
        return True
    else:
        return False

def checkAdminLogin(username):
    cur.execute(f"SELECT role FROM Users WHERE username='{username}'") #Query para verificar se o "role" do utilizador
    if cur.fetchone()[0] == "admin": #Se devolver um registo com "admin", devolve true
        return True
    else:
        return False # Quer dizer que é utilizador normal

def verificar_data_duplicada(name, date):
    cur.execute(f"SELECT * FROM Datas_espetaculo WHERE data='{DateTime(date)}' AND espetaculo='{name}'") #Query para verificar se já existe a data para o respetivo espetaculo
    result = cur.fetchone()
    return result    

def get_espetaculos():
    for espetaculo in cur.execute("SELECT id, nome FROM Espetaculos"): #Query para printar todos os espetaculos
        view.print_lista_espetaculos_com_id(espetaculo)

def check_letra(input): #Verificar se o input tem alguma das letras dentro da lista "letras"
    if input[0][0] not in view.letras: # Se a primeira letra não estiver dentro da lista de letras devolve falso
        return False
    if len(input) > 3: #Se o tamanho do input for maior que 3 ou seja "ABCD" devolve falso
        return False
    if int(input[1:3]) < 1 or int(input[1:3]) > 14: #SE O número do lugar for menor que 1 ou maior que 14 devolve falso, pois só pode ir de 1 a 14 conforme a sala
        return False
    return True

def convert_letters_in_numbers(lista, letras): #CONVERTE AS LETRAS EM NÚMEROS
    for i in range(0, len(lista)): #CICLO para percorrer a lista de reservas
        for k in range(0, len(letras)): # CICLO para percorrer a lista de letras
            if lista[i][:1] == letras[k]: # Ao percorrer a lista de letras, quando encontra a letra associada ao valor do indice da lista, por exemplo (K1)
                lista[i] = lista[i].replace(str(letras[k]), str(letras.index(letras[k])) + " ") #Converte o "K", neste caso em "0", pois substitui a letra na string pelo indíce onde está o "K", dentro da lista de letras.
    list_to_print = []  #Lista a enviar para a sala
    view.sala = view.sala_backup #devolve a sala ao seu estado original(sem reservas)
    for item in range(0, len(lista)): #por cada item dentro da lista de reservas
        list_to_print.append(str(lista[item]).split(" ")) #Adiciona o item e separa com espaço "0 1", "0 2", em vez de "01" ou "02".
    for item in range(0, len(list_to_print)):# Ciclo para percorrer a lista a enviar para a sala
        if list_to_print[item] != ['']: #Se for diferente de ''(bug ao converter)
            view.sala[int(list_to_print[item][0])][int(list_to_print[item][1]) - 1] = "\033[91m x \033[0m" #Muda o lugar vazio para "x", conforme o respetivo indíce. (0, 1) (0, 2) 

def check_if_is_full(): #Verifica se existem lugares disponiveis
    for i in range(0, 11):
        for j in range(0, 13):
            if view.sala[i][j] == " ▢ ": #se encontrar algum lugar vazio, devolve falso, ou seja, não está cheio
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


def get_total_reserva(novareserva): #Calcular o total da reserva
    total = 0
    for item in novareserva:
        if item == "F6" or item == "F7" or item == "F8" or item == "F8" or item == "A6" or item == "A7" or item == "A8" or item == "A9": #SE FOREM VIPS
            total += 12
        else:
            total += 4
    return total


def login():
    username = view.pedir_username() #Pede username
    password = view.pedir_password() #Pede a password
    if checkUserLogin(username, password): #Se as credenciais estiverem corretas
        view.currentuser = username #atribui o utilizador atual ao username inserido
        if checkAdminLogin(username): #Verifica se é admin, se for encaminha para o menuadmin
            view.menuAdmin()
        else:
            view.menuUser() # se não, encaminha para o menuuser
    else:
        view.print_password_errada()
        login() #volta a chamar a função caso o username ou a password estiverem incorretos


def signup(role):
    username = view.pedir_username() #Pede username
    password = view.pedir_password() #Pede a password
    repeatpassword = view.pedir_repeat_nova_password() #Pede para confirmar a password
    while password != repeatpassword: #Enquanto as passwords forem diferentes, solicita a confirmação da password
        view.print_password_diferentes()
        repeatpassword = view.pedir_repeat_nova_password()
    mod.inserir_utilizador(username, password, role) #Chama a função no model para inserir o utilizador, role e password na base de dados
    con.commit()
    view.print_registo_admin_sucesso()

def inserir_espetaculo():
    name = view.pedir_nome_espetaculo() #Pede o nome do espetaculo ao user
    mod.inserir_espetaculo(name) #chama a função no model para inserir o espetaculo na tabela "Espetaculos"
    con.commit()
    option = view.questao_novo_espetaculo() #Pergunta se pretende inserir datas para este novo espetaculo
    if option == "Sim":
        inserir_nova_data(name) #Chama a função para inserir datas
    else:
        view.menuAdmin()

def listar_espetaculos():
    i = 0
    view.print_cabecalho_lista_espetaculos()
    espetaculos = []
    for espetaculo in cur.execute("SELECT nome FROM Espetaculos"): #Query para solicitar o nome de todos os espetaculos
        i += 1
        espetaculos.append(espetaculo[0]) #Insere na lista de espetaculos o valor devolvido
        view.print_lista_espetaculos(i, espetaculo) #dá print ao espetaculo devolvido, juntamente com o indíce atual do ciclo
    view.print_line()
    while True:
        try:
            option = view.pedir_escolha_espetaculo() #Pede a escolha do espetaculo ao user
            selected = espetaculos[int(option) - 1] #converte em int
            return selected
        except:
            view.print_erro_input()

def listar_datas_espetaculo(nome): #Lista os espetaculos
    view.print_cabecalho_lista_datas(nome)
    view.print_line()
    for date in cur.execute(f"SELECT data FROM Datas_espetaculo WHERE espetaculo='{nome}'"):
        view.print_lista_datas(date)
    view.print_line()

def listar_datas_espetaculo_para_reserva(nome):
    datas = []
    for data in cur.execute(f"SELECT id, data FROM Datas_espetaculo WHERE espetaculo='{nome}'"): #Query para devolver as datas do respetivo espetaculo
        datas.append({"id": data[0], "data": data[1]}) #adiciona o valor devolvido à lista de datas
    if datas: #se houver datas para o espetaculo
        view.print_cabecalho_lista_datas(nome)
        view.print_line()
        for i in range(0, len(datas)): #dá print a cada valor dentro da lista de datas
            view.print_lista_datas_para_reserva(i, datas)
        view.print_line()
        while True:
            try:
                option = view.pedir_escolha_data_espetaculo()
                return datas[int(option) - 1]['id']
            except:
                view.print_erro_input()
    else: #se não houver datas
        view.print_sem_datas()
        reservar_bilhetes(None, None) #volta ao menu de reservas de bilhetes

def inserir_nova_data(nome_espetaculo):
    if nome_espetaculo is None: #se não tiver passado um valor para a função (pode passar no caso de acabarmos de inserir um espetaculo)
        nome_espetaculo = listar_espetaculos() #Pede para escolher o espetaculo
        listar_datas_espetaculo(nome_espetaculo) #Lista as datas para o mesmo
    ano = view.pedir_ano()
    mes = view.pedir_mes() #PEDE A DATA
    dia = view.pedir_dia()
    novadata = f"{str(dia).zfill(2)}/{str(mes).zfill(2)}/{str(ano).zfill(2)}" #Converte os inputs em data legivel dd/mm/yyyy
    if verificar_data_duplicada(nome_espetaculo, novadata): #Verifica se a data já existe, se sim dá print e chama a função outra vez
        view.print_data_duplicada()
        inserir_nova_data(nome_espetaculo)
    else:
        mod.inserir_nova_data(nome_espetaculo, novadata) #Chama a função no mod para inserir a nova data na base de dados
        con.commit()
        view.print_sessoa_adicionada_sucesso()
        view.askforenter()
        view.menuAdmin()

def listar_utilizadores(): #Lista os utilizadores
    view.print_cabecalho_lista_users()
    for user in cur.execute("SELECT username FROM Users WHERE role='User'"): #Query para selecionar todos os utilizador com o role "user"
        view.print_users(user)
        view.print_line()

def alterar_password_by_utilizador(username):
    listar_utilizadores()
    while True:
        username = view.pedir_username() #Pede o nome do user
        if check_user_exists(username): #Se existir
            password = view.pedir_nova_password() #Pede a nova password 
            repeatpassword = view.pedir_repeat_nova_password() #Pede a confirmação
            while password != repeatpassword: #Enquanto a confirmação da password for diferente, continua a pedir
                view.print_password_diferentes()
                repeatpassword = view.pedir_repeat_nova_password()
            mod.change_password(username, password) #Chama a função no mod para fazer as alterações na BD
            con.commit()
            view.print_password_sucesso()
            view.askforenter()
            view.menuAdmin()
        else:
            view.print_user_nao_existe()

def alterar_password():
    password = view.pedir_nova_password() #Pede a password
    repeatpassword = view.pedir_repeat_nova_password() #Pede a confirmação
    while password != repeatpassword: #Enquanto a confirmação da password for diferente, continua a pedir
        view.print_password_diferentes()    
        repeatpassword = view.pedir_repeat_nova_password() #Pede a confirmação    
    mod.change_password(view.currentuser, password)
    con.commit()
    view.print_password_sucesso()
    view.askforenter()
    view.main()

def lugares_sala(): #Devolve todos os ids da tabela lugares
    cur.execute(
        f"SELECT id FROM Lugares")
    return [item[0] for item in cur.fetchall()]

def lugares_sala_reservados(data_espetaculo): #Devolve todos os lugares reservados naquela data(id), cada data tem um id agregado ao filme
    cur.execute(
        f"SELECT lugar FROM User_espetaculo_lugar WHERE data_espetaculo='{data_espetaculo}'")
    return [item[0] for item in cur.fetchall()]

def escolha_quantidade(lugares_possiveis): #Solicita a quantidade de bilhetes, se for menor que 0, inválido ou maior que o número de lugares disponíveis, dá os respetivos prints
    while True:
        quantidade = view.pedir_quantidade_bilhetes()
        if quantidade.isnumeric(): #Se for um número
            if int(quantidade) > 0:
                if int(quantidade) <= lugares_possiveis:
                    return int(quantidade)
                else:
                    view.print_sem_lugares_disponiveis()
            else:
                view.print_maior_que_zero()
        else:
            view.print_numero_invalido()

def inserir_novas_reservas(novareserva, data_espetaculo):#Insere as novas reservas na base de dados
    ultima_reserva = cur.execute(f"INSERT INTO Reservas DEFAULT VALUES ").lastrowid
    lugares = ""
    for lugar in novareserva:
        cur.execute(
            f"INSERT INTO User_espetaculo_lugar(user, data_espetaculo, lugar, reserva) VALUES('{view.currentuser}', '{data_espetaculo}', '{lugar}', '{ultima_reserva}')")
        lugares += lugar + " "
    view.print_lugares_reservados(lugares)
    view.print_reserva_sucesso()
    view.askforenter()

def ver_sala():#Pede o espetaculo, a data, solicita os lugares reservados naquela data (id), converte as letras em números e preenche a variável sala, depois dá o print da mesma
    espetaculo = listar_espetaculos()
    data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo)
    lugares_reservados = lugares_sala_reservados(data_espetaculo)
    convert_letters_in_numbers(lugares_reservados, view.letras)
    view.mostrar_sala()
    

def reservar_bilhetes(espetaculo, data_espetaculo):
    novareserva = [] #Variável para as novas reservas
    if espetaculo is None: # Se não for passado nenhum espetáculo
        espetaculo = listar_espetaculos() #Pede o espetaculo
        data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo) #Pede a data do respetivo espetaculo
    lugares = lugares_sala() #Pede à base de dados todos os lugares
    lugares_reservados = lugares_sala_reservados(data_espetaculo) #Pede à BD todos os lugares reservados naquela data (id)
    lugares_disponiveis = [x for x in lugares if x not in lugares_reservados] #Cria uma lista (lugares_disponiveis), com todos os lugares que não são "x"
    if lugares_disponiveis:#Se houverem lugares disponiveis(a variável lugares_disponiveis não está vazia)
        convert_letters_in_numbers(lugares_reservados, view.letras) #Converte as letras em números para preencher a sala
        view.mostrar_sala()
        quantidade = escolha_quantidade(len(lugares_disponiveis)) #solicita a quantidade
        manual_or_auto = view.pedir_manual_auto() #pergunta se a escolha é manual ou auto
        while True:
            if manual_or_auto == "Manual": #se for manual
                novareserva = escolha_manual(quantidade, lugares, lugares_disponiveis)
                break
            elif manual_or_auto == "Auto": # se for auto
                novareserva = escolha_auto(quantidade)
                break
            else:
                view.print_erro_input()
        while True:
            decisao = view.pedir_confirmacao_total_reserva(novareserva) #Pede a confirmação
            if decisao.upper() == "NÃO": #Se for não
                view.menuUser()
            elif decisao.upper() == "SIM":
                inserir_novas_reservas(novareserva, data_espetaculo)
                con.commit()
                view.menuUser()
            else:
                view.print_erro_input()
    else:
        view.print_sala_esgotada()
        reservar_bilhetes(None, None)

def escolha_manual(quantidade, lugares, lugares_disponiveis):
    novareserva = []
    for i in range(0, quantidade): #CICLO Para a quantidade de bilhetes
        lugar = view.pedir_lugar() #Pede o lugar
        if lugar not in lugares: #Se o lugar não estiver na lista de lugares
            view.print_lugar_inexistente()
        else:
            if lugar not in lugares_disponiveis or lugar in novareserva: #Se estiver já estiver reservado
                view.print_lugar_ja_escolhido()
            else:
                novareserva.append(lugar) #adiciona o lugar à nova reserva
    return novareserva

def escolha_auto(quantidade):
    novareserva = []
    if quantidade == 2: # SE FOREM 2 RESERVAS, PROCURA NOS LUGARES DA ESQUERDA E DA DIREITA, PARA FICAREM JUNTOS
        for i in range(0, 11): #PROCURA NA FILA DA ESQUERDA
            if view.sala[i][0] == " ▢ " and view.sala[i][1] == " ▢ ": #SE ESTIVEREM OS DOIS LUGARES VAZIOS, INSERE OS DOIS NA LISTA DA NOVA RESERVA
                novareserva.append(f"{view.letras[i]}{1}")
                novareserva.append(f"{view.letras[i]}{2}")
                return novareserva
        for i in range(0, 11):
                if view.sala[i][12] == " ▢ " and view.sala[i][13] == " ▢ ": #SE ESTIVEREM OS DOIS LUGARES VAZIOS, INSERE OS DOIS NA LISTA DA NOVA RESERVA
                    novareserva.append(f"{view.letras[i]}{13}")
                    novareserva.append(f"{view.letras[i]}{14}")
                    return novareserva
    
    else: #SE NÃO FOREM SÓ 2
        for i in range(0, 11): #PROCURA NO MEIO
            if quantidade - len(novareserva) > 1: #SE FOR MAIS QUE 1 BILHETE A FALTAR 
                all = 0 #Variável para perceber se consegue por todos juntos no meio
                for k in range(2, 12):
                    if view.sala[i][k] == " ▢ ": #Se o lugar estiver vazio 
                        all += 1 #adiciona um ao all
                    else:
                        all -= 1 #retira 1 
                if all >= quantidade or all == 10: #SE ALL for maior ou igual à quantidade ou for 10(máximo no meio)
                    for k in range(2, 12): #Ciclo para adicionar os lugares todos a linha atual
                        if (view.sala[i][k] == " ▢ ") and f"sala[i]{k + 1}" not in novareserva:  #Se já não estiverem na lista da novareserva
                            novareserva.append(f"{view.letras[i]}{k + 1}") #adiciona à lista
                            if quantidade == len(novareserva): #se a quantidade solicitada por igual ao número de bilhetes na lista de reservas, devolve a lista de reservas
                                return novareserva
                            
        #SE NÃO OS CONSEGUIR JUNTAR TODOS, TENTA POR DE 2 EM 2 NO MEIO
        for i in range(0, 11):
            for j in range(2, 12):
                if quantidade - len(novareserva) > 1:
                    if (view.sala[i][j] == " ▢ " and view.sala[i][j + 1] == " ▢ ") or (
                            view.sala[i][j] == "VIP" and view.sala[i][j + 1] == "VIP"):
                        if f"{view.letras[i]}{j + 1}" in novareserva:#SE JÁ ESTIVER NA LISTA DE RESERVAS
                            pass
                        else:
                            novareserva.append(f"{view.letras[i]}{j + 1}")
                            novareserva.append(f"{view.letras[i]}{j + 2}")
                                
        #PROCURA DE 2 EM 2 PELA ESQUERDA
        for i in range(0, 11):
            if quantidade - len(novareserva) > 1:
                if view.sala[i][0] == " ▢ " and view.sala[i][1] == " ▢ ":
                    if f"{view.letras[i]}{1}" in novareserva or f"{view.letras[i]}{2}" in novareserva: #SE JÁ NÃO ESTIVER NA LISTA DE RESERVAS
                        pass
                    else:
                        novareserva.append(f"{view.letras[i]}{1}")
                        novareserva.append(f"{view.letras[i]}{2}")
            else:
                break
        #PROCURA DE 2 EM 2 PELA DIREITA
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
        ##SE SÓ SOBRAR 1
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
        #PROCURA NA ESQUERDA E DIREITA POR UM LUGAR VAZIO AO LADO DE OUTRO OCUPADO
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
        #CASO NÃO ENCONTRAR, PROCURA PELO PRIMEIRO LUGAR VAZIO QUE ENCONTRAR
        for i in range(0, 11):
            for j in range(0, 13):
                if view.sala[i][j] == " ▢ ":
                    if f"{view.letras[i]}{j + 1}" in novareserva:
                        pass
                    else:
                        novareserva.append(f"{view.letras[i]}{j + 1}")
                    if len(novareserva) == quantidade:
                        return novareserva

def data_espetaculo_de_reserva(reserva): # DEVOLVE A DATA DO ESPETACULO NA RESPETIVA RESERVA
    return cur.execute(
        f"SELECT data_espetaculo FROM User_espetaculo_lugar WHERE reserva='{reserva}'").fetchone()[0]

def alterar_reserva():
    espetaculo = listar_espetaculos_user() # PEDE O ESPETACULO
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo) #PEDE A RESERVA
        data_espetaculo = data_espetaculo_de_reserva(reserva) #PROCURA A DATA DO ESPETACULO(ID) PELA RESERVA
        cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE reserva ='{reserva}'") #ELIMINA A RESERVA
        cur.execute(f"DELETE FROM Reservas WHERE id ='{reserva}'") #ELIMINA A RESERVA DA TABELA "RESERVAS"
        reservar_bilhetes(espetaculo, data_espetaculo) #CHAMA A FUNÇÃO PARA RESERVAR OS BILHETES
        
def cancelar_reserva():
    espetaculo = listar_espetaculos_user() #PEDE O ESPETACULO
    if espetaculo is not None:
        reserva = listar_reservas_utilizador(espetaculo) #PEDE A RESERVA
        mod.apagar_reserva(reserva) #CHAMA A FUNÇÃO NO MOD PARA APAGAR A RESERVA
        con.commit()
        view.print_reserva_cancelada()
        view.askforenter()
        view.menuUser()

def listar_espetaculos_user(): #FUNÇÃO PARA LISTAR OS ESPETACULOS ONDE O USER TEM RESERVAS
    i = 0
    espetaculos = []
    for espetaculo in cur.execute( #PROCURA PELOS ESPETACULOS ONDE O USER TEM RESERVA
            f"SELECT DISTINCT espetaculo FROM User_espetaculo_lugar uel INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id WHERE user='{view.currentuser}'"):
        if i == 0:
            view.print_cabecalho_lista_espetaculos() #DÁ PRINT DO ESPETACULO
        i += 1
        espetaculos.append(espetaculo[0]) #ADICIONA O ESPTACULOS À LISTA DE ESPETACULOS
        view.print_lista_espetaculos(i, espetaculo)
    if len(espetaculos) == 0: #SE NÃO DEVOLVER NADA, INFORMA QUE O USER NÃO TEM RESERVAS
        view.print_sem_espetaculos_reservados()
        return None
    print("---------------------------------")
    while True:
        try:
            option = view.pedir_escolha_espetaculo()
            selected = espetaculos[int(option) - 1]
            return selected
        except:
            view.print_input()

def listar_reservas_utilizador(espetaculo): #lista as reservas do utilizador
    i = 0
    reservas = []
    view.print_cabecalho_lista_reservas()
    mapa_reservas = mapa_datas_lugares(espetaculo)
    for reserva in mapa_reservas.keys(): #O IULIAN É QUE FEZ ESTA, TEMOS DE TENTAR PERCEBER
        i += 1
        view.print_lista_reservas(i, mapa_reservas, reserva)
        reservas.append(reserva)
    view.print_line()
    while True:
        try:
            option = view.pedir_escolha_reserva()
            return reservas[int(option) - 1]
        except:
            view.print_erro_input()

def mapa_datas_lugares(espetaculo): # IULIAN
    map = {}
    for item in cur.execute(
            f"SELECT de.data, uel.lugar, uel.reserva "
            f"FROM User_espetaculo_lugar uel "
            f"INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id "
            f"INNER JOIN Lugares l ON uel.lugar = l.id "
            f"WHERE uel.user='{view.currentuser}' AND espetaculo='{espetaculo}' "
            f"ORDER BY l.fila, l.coluna"):
        if map.get(item[2]) is None:
            map[item[2]] = [item[0], item[1]]
        else:
            temp = map[item[2]]
            temp[1] = temp[1] + " " + item[1]
            map[item[2]] = temp
    return map

def bilheteira_por_dia():
    ano = view.pedir_ano()
    mes = view.pedir_mes()
    dia = view.pedir_dia()
    datas = [] #LISTA PARA AS DATAS
    for item in cur.execute( #seleciona as reservas na respetiva data
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}' AND strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{mes.zfill(2)}' AND strftime('%d', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{dia.zfill(2)}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas) #Calcula os valores associados
    view.print_total_bilheteira_dia(dia, mes, ano, total)
    view.askforenter()
    view.menuBilheteira()

def bilheteira_por_mes():
    ano = view.pedir_ano()
    mes = view.pedir_mes()
    datas = [] #LISTA PARA AS DATAS
    for item in cur.execute(#seleciona as reservas na respetiva data
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}' AND strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{mes.zfill(2)}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)#Calcula os valores associados
    view.print_total_bilheteira_mes(mes, ano, total)
    view.askforenter()    
    view.menuBilheteira()

def bilheteira_por_ano():
    ano = view.pedir_ano()
    datas = [] #LISTA PARA AS DATAS
    total = 0
    for item in cur.execute(#seleciona as reservas na respetiva data
            f"SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  ='{ano}'"):
        datas.append(item[0])
    total = get_total_bilheteira(datas)#Calcula os valores associados
    view.print_total_bilheteira_ano(ano, total)
    view.askforenter()
    view.menuBilheteira()

def bilheteira_por_espetaculo():
    espetaculo = listar_espetaculos() #PEDE O ESPETACULO
    datas = [] #LISTA PARA AS DATAS
    total = 0
    for item in cur.execute(f"SELECT id FROM Datas_espetaculo WHERE espetaculo='{espetaculo}'"): #SELECIONA AS DATAS DO RESPETIVO ESPETACULO
        datas.append(item[0])
    total = get_total_bilheteira(datas)#Calcula os valores associados
    view.print_total_bilheteira_espetaculo(espetaculo, total)
    view.askforenter()
    view.menuBilheteira()

def bilheteira_por_sessao():
    espetaculo = listar_espetaculos() #PEDE O ESPETACULO
    data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo) #PEDE A DATA
    lugares_reservados = lugares_sala_reservados(data_espetaculo) #PROCURA OS LUGARES RESERVADOS
    total = 0
    for item in lugares_reservados: #CALCULA OS VALORES
        if item == "F6" or item == "F7" or item == "F8" or item == "F8" or item == "A6" or item == "A7" or item == "A8" or item == "A9":
            total += 12
        else:
            total += 4
    view.print_total_bilheteira_sessao(data_espetaculo, espetaculo, total)
    view.askforenter()
    view.menuBilheteira()
    
def remover_espetaculo():
    espetaculo = listar_espetaculos() #PEDE O ESPETACULO
    cur.execute(f"SELECT id FROM Datas_espetaculo WHERE espetaculo = '{espetaculo}'") #PROCURA AS DATAS DO ESPETACULO
    datas = cur.fetchall()
    for data in datas:
        cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE data_espetaculo='{data[0]}'") #ELIMNA AS RESERVAS DO ESPETACULO
    for data in datas:
        cur.execute(f"DELETE FROM Datas_espetaculo WHERE id='{data[0]}'") #ELIMINA AS DATAS DO ESPETACULO
    cur.execute(f"DELETE FROM Espetaculos WHERE nome='{espetaculo}'") #ELIMINA O ESPETACULO
    view.print_sucesso_remocao(espetaculo)
    view.askforenter()
    view.menuAdmin()
    
def remover_sessao(): #Remover sessão(data)
    espetaculo = listar_espetaculos() #Pede o espetaculo ao admin
    id_data_espetaculo = listar_datas_espetaculo_para_reserva(espetaculo) #solicita o id da data do espetaculo
    cur.execute(f"SELECT data FROM Datas_espetaculo WHERE id='{id_data_espetaculo}'") #procura pela data com esse id
    data_espetaculo = cur.fetchone()[0]
    cur.execute(f"SELECT lugar FROM User_espetaculo_lugar WHERE data_espetaculo='{id_data_espetaculo}'") #Procura pelas reservas nessa data
    reservas = cur.fetchall() #atribui o resultado à variável reservas
    decisao = view.confirmar_remocao_sessao(len(reservas)).upper() #Pede confirmação ao user com o nº de reservas
    if decisao == "SIM":
        cur.execute(f"DELETE FROM User_espetaculo_lugar WHERE data_espetaculo ='{id_data_espetaculo}'") #ELIMINA AS RESERVAS NESSA DATA
        cur.execute(f"DELETE FROM Datas_espetaculo WHERE id='{id_data_espetaculo}'") #ELIMINA A DATA
        view.print_sucesso_remocao_sessao(data_espetaculo, espetaculo)
        view.askforenter()
        view.menuAdmin()
    else:
        view.menuAdmin()

def handle_inp(message):
    user_input = input(message)
    if user_input.upper() == "EXIT": #SE O USER ESCREVER EXIT, VOLTA PARA O MENU
        con.rollback()
        if checkAdminLogin(view.currentuser):
            view.menuAdmin()
        else:
            view.menuUser()
    return user_input