import socket
import threading

class Server:
    def __init__(self):
        self.startServer()

    def startServer(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('======> Server Chat by Afif <=======')
        
        host = socket.gethostbyname(socket.gethostname())
        port = int(input('Masukkan port yang ingin digunakan :  '))

        self.clients = []

        self.s.bind((host,port))
        self.s.listen(50)
    
        print('Jalan pada host : '+str(host))
        print('Jalan pada Port : '+str(port))

        self.username_lookup = {}

        while True:
            c, addr = self.s.accept()

            username = c.recv(1024).decode()
            
            print('Baru tersambung. Nama User : '+str(username))
            self.broadcast('Pengguna Baru . Nama User : '+username)

            self.username_lookup[c] = username

            self.clients.append(c)
             
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self,msg):
        for connection in self.clients:
            connection.send(msg.encode())

    def handle_client(self,c,addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                
                print(str(self.username_lookup[c])+' Meninggalkan Ruang Chat.')
                self.broadcast(str(self.username_lookup[c])+' Telah meninggalkan Ruang Chat.')

                break

            if msg.decode() != '':
                print('Pesan Baru : '+str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)

server = Server()