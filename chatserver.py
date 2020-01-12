#!/usr/bin/python3
import socket
import sys
from _thread import *
import select 
import re

if len(sys.argv)!=2:
    print("Input format = ./chatserver ip:port ")
    sys.exit()

my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


my_info = (sys.argv[1])
a=my_info.split(':')
my_ip_addr=str(a[0])
my_port=int(a[1])

my_server.bind((my_ip_addr,my_port))

my_server.listen(100)
print('Server is connected')
print('Waiting for connection')


clients=[]
clients.append(my_server)

def clientthreading(conn,addr):
    while True:
        
        try:
            nick=conn.recv(2048).decode('utf-8')
            nick1=nick.strip('NICK ')
            regex = re.compile('[@!#$%^&*()?/|}{~:]')
            
            if(regex.search(nick1) == None) and len(nick1)<=12 and 'NICK ' in nick :
                conn.sendall('OK'.encode('utf-8'))
                break
            elif len(nick1) or regex.search(nick1) != None:
                conn.sendall('ERR message is not valid'.encode('utf-8'))
            else:
                conn.close()
                print(addr[0]+" disconnected")
                clients.remove(conn)
                del clients[conn]
                break
        except :
                break

        

    while True:
        try:
            if conn in clients:
                message = conn.recv(2048).decode('utf-8')
                another_message=message.strip('MSG ')
                
            
                if not message:
                    conn.close()
                    print(addr[0]+" has disconnected")
                    clients.remove(conn)
                    break 

                elif 'MSG ' not in message:
                    conn.sendall('ERROR malformed message'.encode('utf-8'))
                else:

                
                    if len(another_message)<=255 :
                    
                        count=0
                        for i in another_message[:-1]:
                            if ord(i)<31:
                            
                                count = count +1
                            
                            else:
                                pass
                            
                        if count != 0:
                            conn.sendall('ERROR , dont use control characters'.encode('utf-8'))
                        else:
                            message_to_send = 'MSG '+nick1+' ' + another_message[:-1]
                
                            broadcasting(message_to_send,conn,nick1)
                    elif len(another_message) > 255 :
                        conn.sendall('ERROR ,message length is more than 256 characters'.encode('utf-8'))
                   
                

        except KeyboardInterrupt:
            conn.close()
            break

def broadcasting(message,connection,nick1):
    for sockets in clients:
        if sockets!= my_server:
            try:
                sockets.sendall(message.encode('utf-8'))
            except KeyboardInterrupt:
                    clients.remove(sockets)
                    break 



while True:
    conn,addr=my_server.accept()
    conn.sendall('Hello 1'.encode('utf-8'))
    clients.append(conn)
    print(addr[0]+" connected")
    
    start_new_thread(clientthreading,(conn,addr))

conn.close()
my_server.close()     


