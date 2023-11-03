#main thread hangs up on input so checking if rThread is alive doesn't accomplish anything since the thread
#will pass the check on startup and never advance until you input something
#os._exit() succesfully shuts down client immediately

from socket import *
import sys
import os
import threading
import time

def main():
    srvrName = sys.argv[1]
    srvrPort = int(sys.argv[2])
    print('Connecting to %s on port %s...' % (srvrName, srvrPort))
    pwd = sys.argv[3] + '\n'
    name = sys.argv[4] + '\n'
    clntSck = socket(AF_INET, SOCK_STREAM)
    clntSck.connect((srvrName,srvrPort))
    clntSck.send(pwd.encode('utf-8'))
    clntSck.send(name.encode('utf-8'))
    response = clntSck.recv(1024)
    if response.decode('utf-8') != 'Welcome!\n':
        sys.exit(1)
    else:
        print(response.decode('utf-8').strip())
    rThread = threading.Thread(target=receive,args=[clntSck])
    rThread.start()

    while True:
        if not rThread.is_alive():
            sys.exit(1)
        msgInput = input()
        if msgInput == ':Exit':
            clntSck.close()
            sys.exit(0)
        elif msgInput == ':)':
            msgInput = '[feeling happy]'
        elif msgInput == ':(':
            msgInput = '[feeling sad]'
        elif msgInput == ':mytime':
            currTime = time.asctime(time.localtime())
            t = currTime[11:16]
            d = currTime[:3]
            m = currTime[4:7]
            dt = currTime[8:10]
            y = currTime[20:24]
            msgInput = 'It\'s %s on %s, %s %s, %s.' % (t, d, dt, m, y)
        try:
            clntSck.send((msgInput + '\n').encode('utf-8'))
        #Server closed the connection
        except ConnectionResetError:
            sys.exit(1)

def receive(clntSck):
    while True:
        try:
            msgReceipt = clntSck.recv(1024)
            if msgReceipt:
                print(msgReceipt.decode('utf-8').strip())
            else:
        #        print("closing client in main/receive thread")
                clntSck.close()
                sys.exit(1)
        #Client exited in main thread
        except ConnectionAbortedError:
            sys.exit(0)
        #Server closed the connection
        except ConnectionResetError:
            print("receiving thread caught resetError")
            sys.exit(1)

if __name__ == '__main__':
    main()