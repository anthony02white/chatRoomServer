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
    #rThread = threading.Thread(target=receive,args=[clntSck])
    #rThread.start()
    #rThread.join()
    wThread = threading.Thread(target=write,args=[clntSck])
    wThread.start()
    
    while True:
        try:
        #    print('before trying recv')
            msgReceipt = clntSck.recv(1024)
        #    print("recv worked, don't know if msgReceipt null yet")
            if msgReceipt:
        #        print("got msg")
                print(msgReceipt.decode('utf-8').strip())
            else:
        #        print("closing client in main/receive thread")
                os._exit(1)
        #Client exited in main thread
        except ConnectionAbortedError:
            os._exit(0)
        #Server closed the connection
        except ConnectionResetError:
        #    print("receiving thread caught resetError")
            wThread.join()
            os._exit(1)
        #except:
        #    print("some other error")

    '''
    while True:
        #rThread.join() send test case said the string it printed was None
        msgInput = input()
        if msgInput == ':Exit':
            #rThread.join()
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
        #This made client exit work?
        try:
            print("before msg send")
            clntSck.send((msgInput + '\n').encode('utf-8'))
        #Server closed the connection
        except ConnectionResetError:
            print("was trying to write, connectionResetError")
            os._exit(1)
    '''
def write(clntSck):
    while True:
        #rThread.join() send test case said the string it printed was None
        msgInput = input()
        if msgInput == ':Exit':
            #rThread.join()
            clntSck.close()
            os._exit(0)
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
        #This made client exit work?
        try:
        #    print("before msg send")
            clntSck.send((msgInput + '\n').encode('utf-8'))
        #Server closed the connection
        except ConnectionResetError:
        #    print("was trying to write, connectionResetError")
            os._exit(1)

#def receive(clntSck):
    while True:
        try:
            print('before trying recv')
            msgReceipt = clntSck.recv(1024)
            print("recv worked, don't know if msgReceipt null yet")
            if msgReceipt:
                print("got msg")
                print(msgReceipt.decode('utf-8').strip())
            else:
                print("closing client in main/receive thread")
                sys.exit(1)
        #Client exited in main thread
        except ConnectionAbortedError:
            sys.exit(0)
        #Server closed the connection
        except ConnectionResetError:
            print("receiving thread caught resetError")
            os._exit(1)
        except:
            print("some other error")

if __name__ == '__main__':
    main()