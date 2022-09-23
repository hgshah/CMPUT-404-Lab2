# reference taken from lab code presented in the class by TA Hassnain 
#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    try:
       s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')

    #QUESTION 3
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #bind socket to address
    s.bind((HOST, PORT))
    #set to listening mode
    s.listen(2)
    
    #continuously listen for connections
    while True:
        print("listening")
        conn, addr = s.accept()
        print("Connected by", addr)
        multi_process = Process(target = handler, args=(s, addr, conn))
        multi_process.daemon = True
        multi_process.start()
        print("Started Process:", multi_process)
        
        #recieve data, wait a bit, then send it back

def handler(s, addr, conn):
        full_data = conn.recv(BUFFER_SIZE)
        time.sleep(0.5)
        conn.sendall(full_data)
        conn.close()

if __name__ == "__main__":
    main()
