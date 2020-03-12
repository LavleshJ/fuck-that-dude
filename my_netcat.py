#!/usr/bin/env python3

import sys
import socket
import getopt
import threading
import os
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
send=""
port = 0

def usage() :
    print("First learn it .")
    
    
def main() :
    global listen 
    global command 
    global upload 
    global execute 
    global target 
    global upload_destination
    global port 
    global send
    
    if not len(sys.argv[1:]) :
        usage()
    
    try :
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:s:",["help","listen","execute","target","port","command","upload","send"])
    except getopt.GetoptError as err :
        print(str(err))
        
    for option,value in opts :
        if option in ("-h","--help") :
            usage()
        elif option in ("-l","--listen") :
            listen = True
        elif option in ("-c","--commandshell") :
            command = True
        elif option in ("-e","--execute") :
            execute = value
        elif option in ("-t","--target") :
            target = value
        elif option in ("-p","--port") :
            port = int(value)
        elif option in("-s","--send") :
            send = value
        elif option in ("-u","--upload") :
            upload_destination = value
        else :
            #assert False,"Unhandled option"
            print("Unhandled option")
          
    if listen==False and len(target) and port > 0 :
        buffer = sys.stdin.read()
        #print(buffer)
        client_sender(buffer)
    
    if listen :
        server_loop()
        
            

def client_sender(buffer) :
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    
        client.connect((target,port)) 
        if len(buffer) :
            client.send(buffer.encode())
        
        if len(send):
            f = open(send,"r")
            data = f.read()
            print(data)
            client.send(data.encode())
            f.close()
            client.close()
            print("[*] File successfully sent : ")
        
        
            
        while True:        
            #print("yes4")
            recv_len = 1
            response = ""
            
            while recv_len:  
                data = client.recv(4096)
                recv_len = len(data.decode())
                response += data.decode()
                if recv_len < 4096:
                    break  
            
            print(response,end="")
            
            buffer = input()
            buffer += "\n"
                
            
            client.send(buffer.encode())     
    except :
        print("[*] Exception! Exiting.")
        
        client.close()  
        
def server_loop() :
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((target,port))
    server.listen(5)
    
    while True :
        
        client,addr = server.accept()
        
        print("[*] Accept connection from :", addr[0]," ",addr[1])
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()
        
def handle_client(client_socket) :
    global upload
    global execute
    global command
    
    if (len(upload_destination)) :
        
        buffer_reader = ""
        while True :
            data = client_socket.recv(1024)
            data = data.decode()
            
            if not len(data) :
                break
            else :
                buffer_reader += data
           
        try :     
            file_descriptor= open(upload_destination,"w")
            file_descriptor.write(buffer_reader)
            file_descriptor.close()
            
            print("File sucessfully saved to ", upload_destination)
            
        except :
            print("An error occured")
    if len(execute) :
        output = run_command(execute)
        client_socket.send(output)
        
    if command :
        while True : 
            client_socket.send("</IMHERE>".encode())
            
            cmd_buffer = ""
            
            while "\n" not in cmd_buffer:
                data = client_socket.recv(1044)
                cmd_buffer += data.decode()
                
            output = run_command(cmd_buffer)
            
            client_socket.send(output)
            
def run_command(command) :
    
    command = command.rstrip()
    if 'cd' in command :
        if command[3:] ==  '..' :
            path = os.getcwd()
            index = path.rfind('/')
            os.chdir(path[0:index])
        else :
            
            path = os.getcwd()
            os.chdir(path+'/'+command[3:])
        command = 'pwd'
    
    
    try :
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
        
    except:
        output ="Invalid command\n".encode()
        
        
    return output
        
            
        
        
main()