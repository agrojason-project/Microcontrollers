import socket

Host = None
Port = 12345

Host = input("Enter host: ")
Address = (Host, Port)
while True:
    message = input("Enter message: ")
    print("Connected to server With IP: " + Host + " and Port: " + str(Port))
    data = None
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(Address)
    while True:
        client.sendall(message.encode())
        client.settimeout(10)
        try:
            data = client.recv(1024)
            if data:
                client.settimeout(None)
                print("Received: " + data.decode())
                data = None
                client.close()
                break
        except socket.timeout:
            client.settimeout(None)
