"""
TODO: Salida de los usuarios que no de errores
TODO: Comprobar en cliente que no meta un parametro mal el usuario
TODO: Mejorar LOG
"""

from modules import *

class gameServer():

    #? Atributes
    usernames = []
    clients = []
    LOG = r"Server_Log.txt"

#?##################################### Message senders ##############################################

    def broadcast(self, msg):
        for client in self.clients:
            client.send(bytes(f"{msg}".encode('utf-8')))
            time.sleep(0.2)

#?###################################### Log handler ##############################################

    def log(self, txt, warning):
        date = datetime.datetime.now()

        strDate = f"{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}"

        with open(self.LOG, 'a') as file:
            if(warning):
                file.write(f"[!] {txt}  |  {strDate}\n")
            else:
                file.write(f"-   {txt}  |  {strDate}\n")
            file.close()

#?#################################### Creation of the server and conenction reciever ###############################################

    def createServer(self, credentials):
        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((credentials[0], int(credentials[1])))
            self.log(f"Server deployed in: {credentials[0]}:{credentials[1]}", True)
            serverSocket.listen()


            begin = self.reciveConnections(serverSocket)

            return begin

        except socket.gaierror:
            errors("Value error: the inserted server values are not correct, please try again")
            return False

        except KeyboardInterrupt:
            os.system("cls")
            print("Exiting...")
            time.sleep(1)

    def reciveConnections(self, server):
        while True:
            try:
                client, addr = server.accept()
                if(len(self.clients) <= 1):

                    begin = False
                    while(begin != True):
                        messageSender(client, "@username")
                        username = client.recv(1024).decode('utf-8')

                        if(username not in self.usernames and username != "" and username != " "):

                            self.clients.append(client)
                            self.usernames.append(username)
                            self.log(f"New connection: {addr[0]}:{addr[1]} --> Username: {username}", False)

                            if(len(self.clients) == 1):
                                self.broadcast("-- Waiting for one more player --")
                            else:
                                self.broadcast("-- Starting game --")
                                time.sleep(3)

                                messageThread = threading.Thread(target=self.reciveMessages)
                                messageThread.start()

                            begin = True

                        else:
                            messageSender(client, "@repeatUsername")

                else:
                    self.log(f"Connection refused: The host {addr[0]}:{addr[1]} try to connect. Already 2 users connected", False)
                    client.close()

            except KeyboardInterrupt:
                os.system("cls")
                print("Exiting...")
                begin = True
                return True

            except (ConnectionAbortedError, ConnectionResetError):
                errors("Closing server: An internal error ocurred, closing server")         
                self.log("Server closed: Internal error", False)
                if(len(self.clients) == 1):
                    messageSender(self.clients[0], "@exit")
                elif(len(self.clients) == 2):
                    messageSender(self.clients[0], "@exit")
                    messageSender(self.clients[1], "@exit")
                sys.exit(0)

#?#################################### Thread: Message reciever ###############################################

    def reciveMessages(self):
        try:
            enter = True
            self.breakLoop = False
            while(self.breakLoop != True):
                
                if(enter):
                    print(f"entre en Enter, enter: {enter}")
                    messageSender(self.clients[0], "@start")
                    response = self.clients[0].recv(1024).decode('utf-8')

                    if(response == "@start"):
                        enter = False
                        #? Creating and sending ships to the user
                        ships = random.randint(1, 100)
                        self.broadcast("@ships")
                        self.broadcast(ships)


                else:
                    for position in range(2):
                        print("Position: ", position)
                        print("Entre")
                        while True:
                            self.broadcast("@menu")
                            self.broadcast(self.usernames[position])
                        
                        
                            selectionText = self.clients[position].recv(1024).decode('utf-8')
                        

                        
                            if(selectionText == "@exit"):
                                raise ConnectionAbortedError               

                            elif(selectionText == "@myBoard"):
                                self.broadcast("@myBoard")
                                self.broadcast(self.usernames[position])
                                message = self.clients[position].recv(1024).decode('utf-8') #? In order to wait a response to be synchronise

                            elif(selectionText == "@myAction"):
                                self.broadcast("@sendAction")
                                self.broadcast(self.usernames[position])
                                board = self.clients[position].recv(1024).decode('utf-8')
                                self.broadcast("@myAction")
                                self.broadcast(board)
                                self.broadcast(self.usernames[position])
                                message = self.clients[position].recv(1024).decode('utf-8') #? In order to wait a response to be synchronise

                            elif(selectionText == "@enemyAction"):
                                self.broadcast("@sendAction")
                                if(position == 0):
                                    self.broadcast(self.usernames[1])
                                    enemyActionBoard = self.clients[1].recv(1024).decode('utf-8')
                                    self.broadcast("@myAction")
                                    self.broadcast(enemyActionBoard)
                                    self.broadcast(self.usernames[position])
                                else:
                                    self.broadcast(self.usernames[0])
                                    enemyActionBoard = self.clients[0].recv(1024).decode('utf-8')
                                    self.broadcast("@myAction")
                                    self.broadcast(enemyActionBoard)
                                    self.broadcast(self.usernames[position])

                                message = self.clients[position].recv(1024).decode('utf-8')

                            elif(selectionText == "@points"):
                                self.broadcast("@getPoints")

                                messageSender(self.clients[0], self.usernames[0])
                                pointsUser1 = self.clients[0].recv(1024).decode('utf-8')

                                messageSender(self.clients[1], self.usernames[1])
                                pointsUser2 = self.clients[1].recv(1024).decode('utf-8')

                                self.broadcast("@points")
                                self.broadcast(pointsUser1)
                                self.broadcast(pointsUser2)
                                self.broadcast(self.usernames[position])
                                self.broadcast(self.usernames[0])
                                self.broadcast(self.usernames[1])

                                message = self.clients[position].recv(1024).decode('utf-8')

                            elif(selectionText == "@attack"):
                                self.broadcast("@sendBoard")
                                if(position == 0):
                                    self.broadcast(self.usernames[1])
                                    points = self.clients[1].recv(1024).decode('utf-8')
                                    enemyBoard = self.clients[1].recv(1024).decode('utf-8')
                                    sendUser = self.usernames[1]
                                    badClient = self.clients[1]
                                else:
                                    self.broadcast(self.usernames[0])
                                    points = self.clients[0].recv(1024).decode('utf-8')
                                    enemyBoard = self.clients[0].recv(1024).decode('utf-8')
                                    sendUser = self.usernames[0]
                                    badClient = self.clients[0]

                                self.broadcast("@attack")
                                self.broadcast(self.usernames[position])
                                self.broadcast(enemyBoard)
                                action = self.clients[position].recv(1024).decode('utf-8')
                                cords = self.clients[position].recv(1024).decode('utf-8')

                                self.broadcast("@printAttack")
                                self.broadcast(self.usernames[position])
                                self.broadcast(sendUser)
                                self.broadcast(action)
                                self.broadcast(cords)

                                points = badClient.recv(1024).decode('utf-8')
                                message = self.clients[position].recv(1024).decode('utf-8')

                                if(points == "0"):
                                    self.broadcast("@end")
                                    self.broadcast(f"The user: {sendUser} has just lost the game")
                                    self.breakLoop = True
                                break
                            
                            elif(position == "@exit"):
                                username = self.clients[position].recv(1024).decode('utf-8')
                                errors(f"Closing server: The user {username} exited the application")         
                                self.log(f"Server closed: The user: {username} exited the application", False)
                                if(position == 0):
                                    messageSender(self.clients[1], "@exit")
                                elif(position == 1):
                                    messageSender(self.clients[0], "@exit")
                                sys.exit(0)        

        except (ConnectionAbortedError, ConnectionResetError):
            errors("Closing server: An internal error ocurred, closing server")         
            self.log("Server closed: Internal error", False)
            if(len(self.clients) == 1):
                messageSender(self.clients[0], "@exit")
            elif(len(self.clients) == 2):
                messageSender(self.clients[0], "@exit")
                messageSender(self.clients[1], "@exit")
            sys.exit(0)                                 




if __name__ == '__main__':
    try:
        begin = False
        while(begin != True):
            userInput = startMenu.menu()
            if(userInput == 1):
                serverCredentials = credentials.welcome()

                gameServerObject = gameServer()
                begin = gameServerObject.createServer(serverCredentials)

            else:
                begin = True
                os.system("cls")
                print("Exiting...")

    except KeyboardInterrupt:
        os.system("cls")
        print("Exiting...")

    except ConnectionRefusedError:
        errors("Connection refused: The server is offline")