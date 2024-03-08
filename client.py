from socket import *
import os
import time
from tkinter import Tk,filedialog
import ssl


CERTFILE='server_cert.pem'

server_name= ""
server_port=17000
buffer=4096
clientSocket=socket(AF_INET,SOCK_STREAM)
SSLclientSocket = ssl.wrap_socket(clientSocket, cert_reqs=ssl.CERT_REQUIRED, ca_certs=CERTFILE)


root=Tk()
root.withdraw()

def file_window():
    file_path=filedialog.askopenfilename()
    return file_path


SSLclientSocket.connect((server_name,server_port))
print("connected to server\n")
print("Enter 1 for uploading prescription")
print("Enter 2 for downloading prescription")
c=int(input("Enter your choice: "))
l=str(c)
SSLclientSocket.send(l.encode())
if(c==1):
    file_path=input("Enter patient name :")
    file_name=file_path.split("/")[-1]
    SSLclientSocket.send(file_name.encode())

    time.sleep(5)
    f=open(file_name,"r")
    while True:
            file_content=f.read(buffer)

            if not file_content:
                break
            SSLclientSocket.send(file_content.encode())
    print("Sent file\n")
    f.close()

elif c==2:
     s=input("Enter patient name: ")
     SSLclientSocket.send(s.encode())

     with open(s,"w") as f2:
          while True:
               file_content=SSLclientSocket.recv(4096).decode()

               if not file_content:
                    break

               f2.write(file_content)
     print("prescription recieved\n")

else:
     print("Enter valid choice !\n")

SSLclientSocket.close()
