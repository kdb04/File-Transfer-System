from socket import*
import threading
import ssl
CERTFILE = 'server_cert.pem'
KEYFILE = 'server_key.pem'


server_port=17000
serverSocket=socket(AF_INET,SOCK_STREAM) #welcoming socket
serverSocket.bind(("",server_port)) #"" means it will listen to any connection attempts



def activate_server():
    serverSocket.listen()
    print("Server is active\n")
    while True:
        channelSocket,addr = serverSocket.accept()
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

        ssl_channelSocket = ssl_context.wrap_socket(channelSocket, server_side=True)

        thread = threading.Thread(target=handle_client,args=(ssl_channelSocket,))
        thread.start(``)
        print(f"Active connections   {threading.active_count() - 1}")



def handle_client(channelSocket):
    choice = channelSocket.recv(1).decode()
    c = int(choice)

    if c == 1:
        file_name = channelSocket.recv(100).decode()
        print(file_name)

        #with open("table.txt", "a") as f_main:
            #f_main.write(file_name)


        with open(file_name, "w") as f:
            while True:
                file_content = channelSocket.recv(409).decode()
                if not file_content:
                    break
                f.write(file_content)
        print("file received\n")

    elif c == 2:
        file_name = channelSocket.recv(107).decode()
        try:
            with open(file_name, "r") as f2:
                while True:
                    file_content = f2.read(4096)
                    if not file_content:
                        break
                    channelSocket.send(file_content.encode())
                print("File sent\n")

        except FileNotFoundError:
                print("No prescription exists for the patient")
    channelSocket.close()



activate_server()

serverSocket.close()
