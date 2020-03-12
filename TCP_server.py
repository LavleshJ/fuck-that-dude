import socket
import threading

def handle_client(client_socket) :
    request =client_socket.recv(1024)
    if(len(request) == 0) :
        print("[*] Connection closed !!")
        print("[*] Waiting for new client.....")
        client_socket.close()
        return
    print("[*] Recevied :",request)
    data = input("[*] Response to Client :")
    client_socket.send(data.encode())
    handle_client(client_socket)
        
    


bind_ip = ""
bind_port = 30002

server = socket.socket()
server.bind((bind_ip,bind_port))
server.listen(1)

print("[*] Listening on ",bind_ip,":",bind_port)
print()

while True :
    client,addr = server.accept()
    
    print("[*] Accept connnection from : ",addr[0],":",addr[1])
    '''
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
    '''
    handle_client(client)
