import socket
import sys
import time

if len(sys.argv) < 3:
    server_ip = input("Type server IPv4 adress: ")
    port = int(input("Port: "))
else:
    server_ip = sys.argv[1]
    port = int(sys.argv[2])

file = open("ouput.txt", "w")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Conncting to {server_ip}:{port}...")
    s.connect((server_ip, port))
    data = s.recv(1024)
    
    while data:
        print(data.decode(), end="")
        option = input()
        s.send(option.encode())
        time.sleep(0.02)
        data = s.recv(1024)
        file.write(data.decode()+"\n")