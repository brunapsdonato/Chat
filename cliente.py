#!/usr/bin/env python3
from ast import While
import socket
import threading
import os

# Dicionário criado para algumas das possiveis mensagens que o cliente possa digitar para confirmação de saida do chat.

dicionario = {
's': 'sim', 'yes': 'sim', 'ok': 'sim', 'confirmo': 'sim', 'S': 'sim', 'SIM': 'sim', 'sair': 'sim', 'sim': 'sim'
}

print('\nSeja bem vindo ao nosso aplicativo de mensagens!\nPara se conectar precisamos que digite as informações a seguir:\n')

try:
    HOST = input("HOST: ") # IP do servidor
    PORT = int(input("Porta: "))#Porta que o servidor escuta
    
    cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Se deseja se conectar ao CHAT junto a outros clientes, terá que criar um Nome de Usuário')
    username = input('Digite seu nome de usuário: ').lower()
    # Connect conecta a soquetes que estão no estado conectado 
    cliente.connect((HOST,PORT))
    print(f'Conectado com sucesso em {HOST}:{PORT}')
except:
    print(f'Erro: reveja o que digitou {HOST}:{PORT}')

# Método para cliente receber mensagens
def receberMensagem():
    while True:
        try:
            message = cliente.recv(2048).decode('UTF-8') # Tamanho do bloco de mensagem
            if message=='getUser':
                cliente.send(username.encode('UTF-8'))
            else:
                print(message)
        except:
            print('ERRO: Verifique se sua conexão ou servidor pode estar offline')
            cliente.close()
            os._exit(0)

# Método para cliente enviar mensagens
def sendMessage():
    while True:
        mensagemSend = input('Digite sua mensagem ou digite QUIT para sair: ')
        if mensagemSend.lower() == 'quit':
            check = input('Você realmente deseja sair? ')
            if check in dicionario and dicionario[check] == 'sim':
                cliente.close()
                os._exit(0)
        cliente.send(mensagemSend.encode('UTF-8'))

thread1 = threading.Thread(target=receberMensagem,args=()) 
thread2 = threading.Thread(target=sendMessage,args=())

thread1.start()
thread2.start()
