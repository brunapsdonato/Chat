import socket
import threading
import os

HOST = input("Host: ")
PORT = int(input("Porta: "))

#invocando socket com parâmetros IPV4 e TCP
servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.bind((HOST,PORT))
servidor.listen()
print(f'O servidor está ativo e receptivo {HOST}:{PORT}\nAguardando conexão de usuários')

clientes = []
usernames = []

def globalMessage(message):
    for cliente in clientes:
        cliente.send(message)

def handleMessages(cliente):
    while True:
        try:
            recebeMensagemDeCliente = cliente.recv(2048).decode('UTF-8')
            globalMessage(f'{usernames[clientes.index(cliente)]} :{recebeMensagemDeCliente}'.encode('UTF-8'))
        except:
            clientLeaved = clientes.index(cliente)
            cliente.close()
            clientes.remove(clientes[clientLeaved])
            clientLeavedUsername = usernames[clientLeaved]
            print(f'{clientLeavedUsername} deixou o chat')
            globalMessage(f'{clientLeavedUsername} saiu do chat!'.encode('UTF-8'))
            usernames.remove(clientLeavedUsername)


def iniciarConexao():
    while True:
        try:
            cliente, address = servidor.accept()
            print(f'Nova conexão: {str(address)}')
            clientes.append(cliente)
            cliente.send('getUser'.encode('UTF-8'))
            username = cliente.recv(2048).decode('UTF-8')
            usernames.append(username)
            globalMessage(f'{username} acabou de entrar no chat!'.encode('UTF-8'))
            user_thread = threading.Thread(target=handleMessages,args=(cliente,))
            user_thread.start()
        except:
            pass

iniciarConexao()