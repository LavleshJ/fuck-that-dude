#!/usr/bin/env python3

import socket
import threading
import sys
import getopt
import os




def usage() :
    print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]" )
    print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")

def main() :
    if len(sys.argv) != 5 :
        usage()
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    server_loop(local_host,local_port,remote_host,remote_port)
    
def server_loop(local_host,local_port,remote_host,remote_port) :
     
    middle = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    middle.bind((local_host,local_port))
    middle.listen(5)
        
    while True :
        client ,addr = middle.accept()
        
        print("[*] RECEVIED CONNECTION FROM", addr[0], addr[1])
        
        client_handle = threading.Thread(target=proxy_handler,args=(client,remote_host,remote_port))
        client_handle.start()
    
        
    
    
def proxy_handler(client,remote_host,remote_port) :
    
    remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    remote.connect((remote_host,remote_port))
    
    try :
        while True :
            
            output = recv_from(client)
            hexdump(output)
            remote.send((request_handler(output)).encode())
            
            output = recv_from(remote)
            hexdump(output)
            client.send((response_handler(output)).encode())
    
    except :
        
        print("[*] Exception handled :")
        client.close()
    
    
def recv_from(reciever) :
    
    recv_len=1
    buffer_data = ""
    while recv_len >1 :
        data = (reciever.recv(4026)).decode()
        buffer_data += data
        recv_len = len(buffer_data)
        if recv_len == 0 :
            break
    return buffer_data
        
def request_handler(client_request) :
    return client_request
    
    
def reponse_handler(server_response) :
    return server_response

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X %-*s %s" % (i, length*(digits + 1), hexa,text) )
    print(b"\n".join(result))    

    
    

main()

