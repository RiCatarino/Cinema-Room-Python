import sqlite3
import os
from Models import model as mod
from Controllers import controller as cont

con = sqlite3.connect('projeto.db', isolation_level=None)
cur = con.cursor()

currentuser= ""

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
    menu_inicial()


def menu_inicial():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\033[95m\033[1m-------BEM-VINDO AO COOLISEU-----\033[0m")
    print("\033[92m\033[1m1. Iniciar Sessão\n2. Registar Utilizador\033[95m")
    print_line()
    option = input("\n\033[0m\033[1mOpção ( Número ): \033[0m")
    if int(option) == 1:
        cont.login()
    elif int(option) == 2:
        cont.signup("User")
        menu_inicial()


def menuAdmin():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n\033[95m\033[1m---------- Olá administrador {currentuser} ----------\033[0m")
    print(
        "\n\033[92m\033[1m1. Inserir Espetáculo\n2. Remover Espetáculo \n3. Remover sessão \n4. Inserir nova data do espetáculo\n5. Ver sala por sessão \n6. Bilheteira  \n7. Alterar password de um cliente\n8. Alterar password\n9. Registar novo administrador\n10. Sair\033[0m")
    option = int(input("\n\033[1mOpção: \033[0m"))
    if option == 1:
        cont.inserir_espetaculo()
    elif option ==2:
        cont.remover_espetaculo()
    elif option == 3:
        cont.remover_sessao()
    elif option == 4:
        cont.inserir_nova_data(None)
    elif option == 5:
        cont.ver_sala()
        askforenter()
        cont.ver_sala()
    elif option == 6:
        menuBilheteira()
    elif option == 7:
        cont.alterar_password_by_utilizador(False, None)
    elif option == 8:
        cont.alterar_password()
    elif option == 9:
        cont.signup("admin")
        menuAdmin()
    elif option == 10:
        menu_inicial()


def menuBilheteira():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[95m\033[1m\n-------- Menu Bilheteira --------\033[0m")
    print_line()
    print(
        "\n\033[92m\033[1m1. Valor por dia \n2. Valor por mês\n3. Valor por ano \n4. Valor por espetáculo \n5. Valor por sessão\n\033[0m")
    print_line()
    while True:
        option = input("\n\033[1mOpção:\033[0m")
        try:
            option = int(option)
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
            else:
                print("\033[91m\033[1mTem de inserir uma opção válida.\033[0m")
        except:
            if str(option).upper() == "EXIT":
                menuAdmin()
            else:
                print("\033[91m\033[1mTem de inserir uma opção válida.\033[0m")
def menuUser():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n\033[95m\033[1m---------- Olá {currentuser}, Bem-vindo ao COOLISEU ----------\033[0m")
    while True:
        print("\n\033[92m\033[1m1. Reservar bilhetes\n2. Alterar Reserva\n3. Cancelar Reserva\n4. Alterar password\n5. Sair\033[0m")
        print_line()
        option = input("\n\033[1mOpção: \033[0m")
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
            
## SALA
def mostrar_sala():
    os.system('cls' if os.name == 'nt' else 'clear')
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
    
##INPUT REQUESTS

def askforenter():
    return input("\n\033[34m\033[1mPara continuar prima 'Enter'...\033[0m")


#USERS E PASSWORDS
def pedir_username():
    return cont.handle_inp("\n\033[95mUsername:\033[0m ")


def pedir_password():
    return input("\033[95mPassword:\033[0m ")

def pedir_nova_password():
    return input("\033[1mNova password: \033[0m")

def pedir_repeat_nova_password():
    return input("\033[1mRepita a nova password: \033[0m")

#DATAS E ESPETACULOS

def pedir_ano():
    while True:
        ano = cont.handle_inp("\033[92m\033[1m\nPor favor, insira o ano: \033[0m")
        try:
            ano = int(ano)
            if ano == 2022 or ano == 2023:
                return ano
        except:
            print("\033[91m Por favor insira o ano em formato numérico.\033[0m")

def pedir_mes():
    while True:
        mes = cont.handle_inp("\033[92m\033[1m\nPor favor, insira o mês(0-12): \033[0m")
        try:
            mes = int(mes)
            if mes > 0 and mes < 13:
                return str(mes)
        except:
            print("\033[91m Por favor insira um mês válido.\033[0m")

def pedir_dia():
    while True:
        dia = cont.handle_inp("\033[92m\033[1m\nPor favor, insira o dia(0-31): \033[0m")
        try:
            dia = int(dia)
            if dia > 0 and dia < 32:
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
    return cont.handle_inp(f"\n\033[91mO total da sua reserva é \033[94m{cont.get_total_reserva(novareserva)}€\033[91m, pretende continuar (Sim/Não) ? \033[0m")

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
    print(f"\033[92m\033[1m{user[0]}\033[1m")

def print_password_sucesso():
    print("\n\033[34m\033[1m------Password Alterada com sucesso.------\033[0m\n")

def print_password_diferentes():
    print("\n\033[91m\033[1m------As password não coincidem.------\033[0m\n")
    
def print_user_nao_existe():
    print("\n\033[91m\033[1mEsse Utilizador não existe.\033[0m")

def print_registo_admin_sucesso():
    print("\n\033[94m\033[1mNovo administrador registado com sucesso!\033[0m")


## DATAS E ESPETACULOS
def print_data_duplicada():
    print("\033[91m\033[1mEste espetáculo já tem uma sessão nessa data.\033[0m")

def print_cabecalho_lista_espetaculos():
    print("\n\033[95m\033[1m------Lista de Espetáculos------\033[0m")
    
def print_lista_espetaculos(i, espetaculo):
    print(f"\033[92m\033[1m{i}: {espetaculo[0]} \033[0m")

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
    print("\n------Não tem espetáculos reservados------")
    
def print_cabecalho_lista_reservas():
    print("\n------Lista de Reservas------")

def print_lista_reservas(i, mapa_reservas, reserva):
    print(f"{i}: Data- {mapa_reservas.get(reserva)[0]} Bilhetes- {mapa_reservas.get(reserva)[1]}")

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
