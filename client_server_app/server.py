import socket
import os
import platform 

# show directory contents
def send_dir_contents():
    con.send(b"Enter path: ")
    dir_path = con.recv(1024).decode()
    if dir_path[-1] == "\n":
        dir_path = dir_path[0:-1]
    try: 
        for item in os.listdir(dir_path):
           con.send(f"{item}\n".encode())
    except Exception as msg:
        con.send(f"Error: {str(msg)}".encode())

# sending system info to client
def send_system_info():
    con.send(b"-"*100)
    con.send(f"\nOS: {sys_info[1].system} -version {sys_info[1].version}".encode())
    con.send(f"\nProcessor: {sys_info[2]}".encode())
    con.send(f"\nMachine name: {sys_info[1].node}\n".encode()+
    f"Logged in with username: {sys_info[0]}\n".encode())
    con.send(b"-"*100)

# gathering system information
def get_system_info():
    user_id = os.getlogin()
    sys_info = platform.uname()
    proc_info = []
    proc_info.append(os.environ["PROCESSOR_ARCHITECTURE"])
    proc_info.append(os.environ["PROCESSOR_IDENTIFIER"])
    proc_info.append(os.environ["PROCESSOR_ARCHITECTURE"])
    return user_id, sys_info, proc_info

# interactiv user manu      
def menu():
    while menu_cond:
        con.send(b"\nSelect an option:\n1. Show contents of a directory"+
        b"\n2. Get system info\n3. Exit\n>")
        try:    
            data = int(con.recv(1024))
            if data == 3: break
            user_menu[data]()
        except ValueError as err:
            con.send(str(err).encode())


user_menu = {
    1: send_dir_contents,
    2: send_system_info,
}
ipv4 = input("Enter the ipv4 address: ")
port = int(input("Port: "))
menu_cond = True
sys_info = get_system_info()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Socket initializing...")
    s.bind((ipv4, port))
    s.listen(1)
    print(f"Host {ipv4} listening at port {port}....")
    con, addr = s.accept()
    print(f"[ OK ] Client {addr} connected")
    try: 
#        con.sendall(b"[ OK ] Connection establised\n")
        menu()
        con.sendall(b"Connection ended.\nPress enter to continue.")
    except socket.error as err:
        print("Socket error: "+str(err))
    finally:
        con.close()
        





