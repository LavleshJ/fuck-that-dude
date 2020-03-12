import socket
import sys

target_host = sys.argv[1]
target_port = int(sys.argv[2])


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host,target_port))


while True :
    
    data = input("[*] REQUEST TO SERVER :")
    if(len(data) == 0) :
        break

    client.send(data.encode())

    response = client.recv(4096)

    print("[*] REPLY FROM SERVER :",response.decode())
    print()
