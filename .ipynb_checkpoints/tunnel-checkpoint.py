import socket
import threading

def forward_data(src, dst):
    while True:
        try:
            data = src.recv(4096)
            if not data:
                break
            dst.send(data)
        except:
            break

def tunnel_handler():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9000))
    server.listen(5)
    print('Strix tunnel listening on port 9000')
    
    while True:
        conn, addr = server.accept()
        print(f'Connection from {addr}')
        
        try:
            target = socket.socket()
            target.connect(('192.168.0.1', 80))
            print('Connected to router 192.168.0.1:80')
            
            t1 = threading.Thread(target=forward_data, args=(conn, target), daemon=True)
            t2 = threading.Thread(target=forward_data, args=(target, conn), daemon=True)
            t1.start()
            t2.start()
        except Exception as e:
            print(f'Error: {e}')
            conn.close()

if __name__ == '__main__':
    tunnel_handler()
