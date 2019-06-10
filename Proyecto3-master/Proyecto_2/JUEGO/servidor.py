import socket
import threading

s = s.socket(socket.AF_INET, s.SOCK_STREM)

sock.bind(('0.0.0.0', 8000))

sock.listen(2)

connections = []

def handler(c,a):
    global connections
    while True:
        data = c.recv(1024)
        for connection in connections:
            connection.send(bytes(data))
        if not data:
            connections.remove(c)
            c.close()
            break

while True:
    c,a = sock.accept()
    cThread = threading.Thread(target = handler)
    cThread.daemon = True
    cThread.start
    connections.append(c)
    print(connections)
    
    
