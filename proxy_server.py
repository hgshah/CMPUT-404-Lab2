# reference taken from lab code presented in the class - TA Hassnain 
#!/usr/bin/env python3
from multiprocessing.dummy import Process
from operator import truediv
import socket
import time
import sys
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    host = 'www.google.com'
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
        print("proxy server started")
        proxy.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        proxy.bind((HOST, PORT))
        proxy.listen(1)
   
        while True:
            print("listening")
            conn, addr = proxy.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #recieve data, wait a bit, then send it back
                print('Connection being establishe to google')
                remote_ip = get_remote_ip(host)
                s.connect((remote_ip, port))
                multi_process = Process(target = multiple_handling, args=(s, addr, conn))
                multi_process.daemon = True
                multi_process.start()
                print("Started Process:", multi_process)
                
            conn.close()

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def multiple_handling(s, addr, conn):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data  {send_full_data} to google")
    s.sendall(send_full_data)
    s.shutdown(socket.SHUT_WR)
    data = s.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)
    


if __name__ == "__main__":
    main()
