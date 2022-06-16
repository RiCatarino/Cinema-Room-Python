from ast import Break
import sqlite3 #Biblioteca sqlite
import os
from Models import model as mod
from Controllers import controller as cont


con = sqlite3.connect('projeto.db', isolation_level=None) #Conexão à BD
cur = con.cursor()

currentuser= "" #Variável para saber qual é o utilizador que está ativo

letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"] # Lista de letras para inserir no printa da sala, e receber os inputs dos utilizadores relativamente aos bilhetes
letras.reverse() #Inverte a lista, pois é o formato da sala
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
    menu_inicial()

def menu_inicial():
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa o terminal consoante o SO
    global currentuser
    currentuser = ""
    print("\n\033[95m\033[1m-------BEM-VINDO AO COOLISEU-----\033[0m")
    print("\033[92m\033[1m1. Iniciar Sessão\n2. Registar Utilizador\n3. Sair\033[95m")
    print_line()
    while True:
        try: # Tenta converter o input em int, se encontrar uma excepção(linha 48), dá print com o erro.
            option = int(input("\n\033[0m\033[1mOpção ( Número ): \033[0m")) #Pede input ao utilizador e tenta converter em int
            if option== 1:
                cont.login()
            elif option == 2:
                cont.signup("User")
                menu_inicial()
            elif option == 3:
                os._exit(0)
            else:
                print_erro_input()# Se não for o 1 ou 2
        except:
            print_erro_input() # Se o input não for um número

def menuAdmin():
    os.system('cls' if os.name == 'nt' else 'clear')# Limpa o terminal consoante o SO
    print(f"\n\033[95m\033[1m---------- Olá administrador {currentuser} ----------\033[0m") #Print com o nome do utilizador
    print("\n\033[92m\033[1m1. Espetáculos \n2. Gestão de Utilizadores\n3. Bilheteira  \n4. Sair\033[0m")
    while True:
        try: # Tenta converter o input em int, se encontrar uma excepção(linha 82), dá print com o erro.
            option = int(input("\n\033[1mOpção: \033[0m"))#Pede input ao utilizador e tenta converter em int
            if option == 1:
                menu_espetaculos()
            elif option ==2:
                menu_gestao_utilizadores()
            elif option == 3:
                menuBilheteira()
            elif option == 4:
                menu_inicial()
            else:
                print_erro_input() # Se não for um dos números do menu
        except:
            print_erro_input() # Se o input não for um número
    
    
def menu_espetaculos():
    os.system('cls' if os.name == 'nt' else 'clear')# Limpa o terminal consoante o SO
    print(f"\n\033[95m\033[1m---------- Menu de Espetáculos ----------\033[0m") #Print com o nome do utilizador
    print("\n\033[92m\033[1m1. Lista de espetáculos\n2. Listar sessões de um espetáculo\n3. Inserir Espetáculo\n4. Remover Espetáculo \n5. Remover sessão \n6. Inserir nova data do espetáculo\n7. Ver sala por sessão \n8. Voltar\033[0m")
    while True:
        try: # Tenta converter o input em int, se encontrar uma excepção(linha 82), dá print com o erro.
            option = int(input("\n\033[1mOpção: \033[0m"))#Pede input ao utilizador e tenta converter em int
            if option ==1:
                cont.listar_espetaculos(True)
                askforenter()
                menu_espetaculos()
            elif option ==2:
                cont.listar_sessoes_espetaculo()
                askforenter()
                menu_espetaculos()
            elif option == 3:
                cont.inserir_espetaculo()
            elif option ==4:
                cont.remover_espetaculo()
            elif option == 5:
                cont.remover_sessao()
                askforenter()
                menu_espetaculos()
            elif option == 6:
                cont.inserir_nova_data(None)
            elif option == 7:
                cont.ver_sala()
                askforenter()
                menu_espetaculos()
            elif option == 8:
                menuAdmin()
            else:
                print_erro_input() # Se não for um dos números do menu
        except:
            print_erro_input() # Se o input não for um número

def menu_gestao_utilizadores():
    os.system('cls' if os.name == 'nt' else 'clear')# Limpa o terminal consoante o SO
    print(f"\n\033[95m\033[1m---------- Menu de Gestão de Utilizadores ----------\033[0m") #Print com o nome do utilizador
    print("\n\033[92m\033[1m1. Listar Utilizadores \n2. Alterar password de um Utilizador\n3. Alterar password\n4. Registar novo Administrador\n5. Bloquear Utilizador\n6. Desbloquear Utilizador\n7. Voltar\033[0m")
    while True:
        try: # Tenta converter o input em int, se encontrar uma excepção(linha 82), dá print com o erro.
            option = int(input("\n\033[1mOpção: \033[0m"))#Pede input ao utilizador e tenta converter em int
            if option ==1:
                cont.listar_todos_os_utilizadores()
                askforenter()
                menu_gestao_utilizadores()
            if option == 2:
                cont.alterar_password_by_utilizador(None)
            elif option ==3:
                cont.alterar_password()
            elif option == 4:
                cont.signup("admin")
                askforenter()
                menu_gestao_utilizadores()
            elif option == 5:
                cont.bloquear_utilizador()
            elif option == 6:
                cont.desbloquear_utilizador()
            elif option == 7:
                menuAdmin()
            else:
                print_erro_input() # Se não for um dos números do menu
        except:
            print_erro_input() # Se o input não for um número


def menuBilheteira():
    os.system('cls' if os.name == 'nt' else 'clear')# Limpa o terminal consoante o SO
    print("\033[95m\033[1m\n-------- Menu Bilheteira --------\033[0m")
    print_line()
    print(
        "\n\033[92m\033[1m1. Valor por dia \n2. Valor por mês\n3. Valor por ano \n4. Valor por espetáculo \n5. Valor por sessão\n6. Sair\033[0m")
    print_line()
    while True:
        try: # Tenta converter o input em int, se encontrar uma excepção(linha 108), dá print com o erro.
            option = int(cont.handle_inp("\n\033[1mOpção: \033[0m"))#Pede input ao utilizador e tenta converter em int, caso insira exit, será encaminhado para o menu admin
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
            elif option == 6:
                menuAdmin()    
            else:
                print_erro_input()# Se não for um dos números do menu
        except:
            print_erro_input()# Se o input não for um número
    
                

def menuUser():
    os.system('cls' if os.name == 'nt' else 'clear')# Limpa o terminal consoante o SO
    print(f"\n\033[95m\033[1m---------- Olá {currentuser}, Bem-vindo ao COOLISEU ----------\033[0m")
    while True:
        print("\n\033[92m\033[1m1. Reservar bilhetes\n2. Alterar Reserva\n3. Cancelar Reserva\n4. Alterar password\n5. Sair\033[0m")
        print_line()
        while True:
            try:
                option = int(input("\n\033[1mOpção: \033[0m"))
                if option == 1:
                    cont.reservar_bilhetes(None, None)
                elif option == 2:
                    cont.alterar_reserva()
                elif option == 3:
                    cont.cancelar_reserva()
                elif option == 4:
                    cont.alterar_password()
                elif option == 5:
                    menu_inicial()
                else:
                    print_erro_input()# Se não for um dos números do menu
            except:
                print_erro_input()# Se o input não for um número

            
## SALA
def mostrar_sala():
    os.system('cls' if os.name == 'nt' else 'clear')# Limpa o terminal consoante o SO
    print("\n\t\t\t\033[95m   ESTADO DA SALA")
    print("\033[94m|---------------------------------------------------------------------|")
    print("|     1   2      3   4   5   6   7   8   9   10  11  12     13  14    |")
    for i in range(0, 11): #Para cada linha inteira preenche o que está no respetivo indíce, seja um lugar vazio ou reservado
            if i == 6 or i == 10: #se for a 6 linha da matriz, salta uma linha (conforme o design da sala que está no enunciado)
                print()
            print("|", letras[i], "\033[0m", sala[i][0], sala[i][1], "  ", sala[i][2], sala[i][3],
                  sala[i][4], sala[i][5], sala[i][6], sala[i][7], sala[i][8], sala[i][9],
                  sala[i][10], sala[i][11], "  ", sala[i][12], sala[i][13], "\033[94m", letras[i], "|") #Print dos indíces com as diferentes cores em cada parte, e também as barras de lado
    print("\n\t   |----------------------------------------------------------|")
    print("\t   |\t\t\t\t\t\t\t      |")
    print("\t   |\t\t\t PALCO \t\t\t\t      |")
    print("\t   |\t\t\t\t\t\t\t      |")
    print("\t   |----------------------------------------------------------|\033[0m")
    
##INPUT REQUESTS

def askforenter():
    return input("\n\033[34m\033[1mPara continuar prima 'Enter'...\033[0m") # Pede ao utilizador qualquer input para continuar o programa

#USERS E PASSWORDS
def pedir_username():
    return cont.handle_inp("\n\033[95mUsername:\033[0m ")

def pedir_password():
    return cont.handle_inp("\033[95mPassword:\033[0m ")

def pedir_nova_password():
    return cont.handle_inp("\033[1mNova password: \033[0m")

def pedir_repeat_nova_password():
    return cont.handle_inp("\033[1mRepita a nova password: \033[0m")

def pedir_confirmacao_bloquear(username):
    return cont.handle_inp(f"\033[91m\033[1mPretende bloquear o utilizador {username}? (Sim/Não):\033[0m ")

def pedir_confirmacao_desbloquear(username):
    return cont.handle_inp(f"\033[91m\033[1mPretende desbloquear o utilizador {username}? (Sim/Não):\033[0m ")

#DATAS E ESPETACULOS

def pedir_ano():
    while True:
        ano = cont.handle_inp("\033[92m\033[1m\nPor favor, insira o ano: \033[0m") #Pede o input ao utilizador do ano
        try: #tenta converter em INT
            ano = int(ano) #converte o input em int
            if ano == 2022 or ano == 2023: #se o input for 2022 ou 2023, devolve o input à respetiva função
                return ano
        except:
            print("\033[91m Por favor insira o ano em formato numérico.\033[0m") #

def pedir_mes():
    while True:
        mes = cont.handle_inp("\033[92m\033[1m\nPor favor, insira o mês(1-12): \033[0m")
        try: #tenta converter o input em int
            mes = int(mes)#converte o input em int
            if mes > 0 and mes < 13:#Se o input for entre 1 e 12 devolve o input em tipo string
                return str(mes)
        except:
            print("\033[91m Por favor insira um mês válido.\033[0m")

def pedir_dia():
    while True:
        dia = cont.handle_inp("\033[92m\033[1m\nPor favor, insira o dia(1-31): \033[0m")
        try:#tenta converter o input em int
            dia = int(dia) #converte o input em int
            if dia > 0 and dia < 32:#Se o input for entre 0 e 31 devolve o input em tipo string
                return str(dia)
        except:
            print("\033[91m Por favor insira um dia válido.\033[0m")

def pedir_nome_espetaculo():
    return cont.handle_inp("\n\033[92m\033[1mNome do novo espetáculo: \033[0m")

def questao_novo_espetaculo():
    return cont.handle_inp("\n\033[92m\033[1mPretende inserir datas para este espetáculo?: (Sim / Não):  \033[0m")

def pedir_escolha_espetaculo():
    return cont.handle_inp("\033[1mEscolha o Espetáculo: \033[0m")

def pedir_escolha_data_espetaculo():
    return cont.handle_inp("\n\033[1mQual data pretende? \033[0m")
    
def confirmar_remocao_sessao(total):
    return cont.handle_inp(f"\n\033[91m\033[1mPretende apagar este sessão com {total} lugares reservados (Sim/Não) ? \033[0m")
    

def pedir_quantidade_bilhetes():
    return cont.handle_inp("\n\033[1mQuantos lugares pretende reservar? \033[0m")

def pedir_manual_auto():
    return cont.handle_inp("\033[1mPretende a escolha manual ou automática? (Manual/Auto):\033[0m")
    
def pedir_confirmacao_total_reserva(novareserva):
    stringreservas = ""
    for item in novareserva:
        stringreservas += item + " "
        
    return cont.handle_inp(f"\n\033[91mO total da sua reserva é \033[94m{cont.get_total_reserva(novareserva)}€\033[91m, para os bilhetes \033[94m{stringreservas}\033[91mpretende continuar (Sim/Não) ? \033[0m")

def pedir_lugar():
    return cont.handle_inp("\033[1mEscolha o lugar: \033[0m").upper()
    
def pedir_escolha_reserva():
    return cont.handle_inp("\033[1mEscolha a Reserva: \033[0m")

#PRINT OUTPUTS

#PRINTS USERS
def print_password_errada():
    print("\033[91m\033[1m\nUtilizador ou Password incorretos.\033[0m")

def print_cabecalho_lista_users():
    print("\n\033[95m\033[1m--------- Utilizadores ---------\033[0m\n")

def print_users(user):
    if user[1] == None: ## SE O UTILIZADOR NÃO ESTIVER BLOQUEADO
        print(f"\033[92m\033[1m{user[0]}\033[1m")
    else:
        print(f"\033[91m\033[1m{user[0]}\033[1m") # SE ESTIVER BLOQUEADO

def print_password_sucesso():
    print("\n\033[34m\033[1m------ Password Alterada com sucesso. ------\033[0m\n")

def print_password_diferentes():
    print("\n\033[91m\033[1m------ As password não coincidem. ------\033[0m\n")
    
def print_user_nao_existe():
    print("\n\033[91m\033[1mEsse Utilizador não existe.\033[0m")
    
def print_user_existe():
    print("\n\033[91m\033[1mJá existe um utilizador com esse username.\033[0m")
    

def print_registo_admin_sucesso():
    print("\n\033[94m\033[1mNovo administrador registado com sucesso!\033[0m")

def print_utilizador_bloqueado():
    print("\033[91m\033[1mEste utilizador está bloqueado, por favor contacte um administrador.\033[0m")

def print_utilizador_naobloqueado():
    print("\033[91m\033[1mEste utilizador não está bloqueado.\033[0m")
    
def print_erro_utilizador_ja_bloqueado():
    print("\033[91m\033[1mEste utilizador já se encontra bloqueado.\033[0m")    

def print_erro_bloquear_a_si_mesmo():
    print("\033[91m\033[1mPedimos desculpa, mas não se pode bloquear a si mesmo.\033[0m")    
    
def print_bloqueio_sucesso():
    print("\n\033[34m\033[1m------ Utilizador bloqueado com sucesso ------\033[0m\n")

def print_desbloqueio_sucesso():
    print("\n\033[34m\033[1m------ Utilizador desbloqueado com sucesso ------\033[0m\n")
    


    
## DATAS E ESPETACULOS
def print_data_duplicada():
    print("\033[91m\033[1mEste espetáculo já tem uma sessão nessa data.\033[0m")

def print_cabecalho_lista_espetaculos():
    print("\n\033[95m\033[1m------ Lista de Espetáculos ------\033[0m")
    
def print_lista_espetaculos(i, espetaculo):
    print(f"\033[92m\033[1m{i}: {espetaculo[0]} \033[0m")

def print_lista_espetaculos_com_id(espetaculo):
    print(f"\nID: {espetaculo[0]} Nome: {espetaculo[1]} ")

def print_erro_espetaculo_existe():
    print("\033[91m\033[1mJá existe um espetáculo com esse nome.\033[0m")


def print_line():
    print("\033[95m\033[1m---------------------------------\033[0m")
    
def print_cabecalho_lista_datas(nome):
    print(f"\n\033[95m\033[1m------ Datas do espetáculo {nome} ----\033[0m")

def print_lista_datas(data):
    print(f"\033[92m\033[1m\t| {data[0]} |\033[0m")
    
def print_lista_datas_para_reserva(i,datas):
    print(f"\t\033[92m\033[1m| {i + 1}: {datas[i]['data']} |\033[0m")
    
def print_sem_datas():
    print("\033[31m\nNão há datas para este evento.\033[0m")

def print_sucesso_remocao(espetaculo):
    print(f"\033[91m\033[1m\nEspetáculo '{espetaculo}' removido com sucesso!")

def print_sessoa_adicionada_sucesso():
    print("\n\033[95m\033[1m---------- Sessão adicionada com sucesso. ----------\033[0m")

def print_erro_input():
        print("\033[91m\033[1mEssa opção não existe.\033[0m") # Se o input não for um número
    
##RESERVAS
def print_sem_lugares_disponiveis():
    print("\033[91mNão existem lugares suficientes disponíveis.\033[0m")
    
def print_maior_que_zero():
    print("\033[91mTem de inserir um número maior que 0.\033[0m")

def print_numero_invalido():
    print("\033[91mTem de inserir um número válido.\033[0m")
    
def print_lugares_reservados(lugares):
    print(f"\n\033[33m\033[1mLugares reservados: {lugares}\033[0m")
    
def print_reserva_sucesso():
    print("\n\033[94m\033[1m----------Lugares reservados com sucesso----------\033[0m")
    
def print_sala_esgotada():
    print("\n\033[91mPedimos desculpa, mas a sala encontra-se esgotada.\033[0m")

def print_lugar_inexistente():
    print("\n\033[91mALERTA: Esse lugar não existe.\n\033[0m")
    
def print_lugar_ja_escolhido():
    print("\n\033[91mALERTA: Esse lugar já está escolhido.\n\033[0m")

def print_sem_espetaculos_reservados():
    print("\n------ Não tem espetáculos reservados ------")
    
def print_cabecalho_lista_reservas():
    print("\n------ Lista de Reservas ------")

def print_lista_reservas(i, mapa_reservas, reserva):
    print(f"{i}: Data- {mapa_reservas.get(reserva)[0]} Bilhetes- {mapa_reservas.get(reserva)[1]}")

def print_reserva_cancelada():
    print(f"\n\033[33m\033[1mReserva cancelada!\033[0m")
## BILHETEIRA

def print_total_bilheteira_dia(dia, mes, ano, total):
    print(f"\033[107m\033[94m\033[1m\nTotal no dia {dia}/{mes}/{ano}: {total}€\033[0m")
    
def print_total_bilheteira_mes(mes, ano, total):
    print(f"\033[107m\033[94m\033[1m\nTotal no mês {mes}/{ano}: {total}€\033[0m")
    
def print_total_bilheteira_ano(ano, total):
    print(f"\033[107m\033[94m\033[1m\nTotal no ano {ano}: {total}€\033[0m")
    
def print_total_bilheteira_espetaculo(espetaculo, total):
    print(f"\033[107m\033[94m\033[1m\nTotal do espetaculo '{espetaculo}': {total}€\033[0m")

def print_total_bilheteira_sessao(data, espetaculo, total):
    print(f"\033[107m\033[94m\033[1m\nTotal da sessão no dia {data}, do espetáculo '{espetaculo}': {total}€\033[0m")

def print_sucesso_remocao_sessao(data, espetaculo):
    print(f"\033[34m\033[1m\nA sessão na data {data} do espetáculo '{espetaculo}' foi removida com sucesso.\033[0m")
