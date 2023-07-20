from socket import *
import sys
import threading

users = {}

def main():
    srvrPort = int(sys.argv[1])
    print('Server started on port %d. Accepting connections...' % srvrPort)
    pwd = sys.argv[2]
    welcomeSck = socket(AF_INET, SOCK_STREAM)
    welcomeSck.bind(('',srvrPort))
    welcomeSck.listen(1)
    while True:
        connectionSckt, addr = welcomeSck.accept()
        msg = connectionSckt.recv(1024).decode('utf-8')
        partition = msg.partition('\n')
        atmptP = partition[0]
        name = partition[2].strip()
        if atmptP != pwd:
            connectionSckt.send(("Incorrect password").encode('utf-8'))
            connectionSckt.close()
        elif name in users:
            connectionSckt.send(("Name already in use").encode('utf-8'))
            connectionSckt.close()
        #elif " " in name:
        #    connectionSckt.send(("Invalid name").encode('utf-8'))
        #    connectionSckt.close()
        else:
            connectionSckt.send(("Welcome!\n").encode('utf-8'))
            print(name + " joined the chatroom")
            broadcast(name + " joined the chatroom\n")
            users[name] = connectionSckt
            connectThread = threading.Thread(target=clientHandler,args=[connectionSckt, name])
            connectThread.start()

def clientHandler(sck, name):
    while True:
        try: 
            msg = (sck.recv(1024)).decode('utf-8').strip()
        except ConnectionResetError:
            users.pop(name)
            print(name + " left the chatroom")
            broadcast(name + " left the chatroom\n")
            break
        if not msg:
            users.pop(name)
            print(name + " left the chatroom")
            broadcast(name + " left the chatroom\n")
            break
        dmCh = msg.partition(" ")
        if dmCh[0] == ":dm":
            rest = dmCh[2].partition(" ")
            destName = rest[0]
            msg = rest[2]
            destSck = users[destName]
            dm = name + " -> " + destName + ": " + msg
            print(dm)
            destSck.send((dm + "\n").encode('utf-8'))
            sck.send((dm + "\n").encode('utf-8'))
        else:
            print(name + ": " + msg)
            broadcast(name + ": " + msg + "\n")

def broadcast(msg):
    #print(msg)
    for sck in users.values():
        sck.send(msg.encode('utf-8'))

if __name__ == '__main__':
    main()