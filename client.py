from email import message
from modules import *

class gameClient():

    #? Atributes
    lives = 0
    server = ""
    username = ""
    playerBoard = [[]]
    actionPlayerBoard = [[]]
    DIMENSIONS = 10

#?#################################### Board printer and points printer ###############################################

    def printBoard(self, board):
        Alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(self.DIMENSIONS):
            if(i == 0):
                print(f"    {i}   ", end="")
            else:
                print(f"{i}   ", end="")

        print()

        for i in range(self.DIMENSIONS):
            print(f"{Alphabet[i]}   ", end="")
            for a in range(self.DIMENSIONS):
                print(f"{board[i][a]}   ", end="")
            print()

    def printPoints(self, points, usernames):
        os.system("cls")
        table = [['Player points', 'Points'], [usernames[0], points[0]], [usernames[1], points[1]]]
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', stralign='center', floatfmt='.0f'))


#?#################################### Connection to the server and reciver of server messages ###############################################

    def connectServer(self, credentials):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((credentials[0], int(credentials[1])))
        self.server = serverSocket

        self.reciveMessages()

    def reciveMessages(self):
        while True:
            message = self.server.recv(1024).decode('utf-8')
            print(message)

            if(message == "@start"):
                messageSender(self.server, "@start")
            elif(message == "@username"):
                username = input("Username: ")
                self.username = username
                messageSender(self.server, username)
            elif(message == "@repeatUsername"):
                errors("ERROR: The chosen username is already taken, please choose another one")
            elif(message == "@ships"):
                ships = self.server.recv(1024).decode('utf-8')
                print(ships)
                self.fillBoards(ships)
                self.lives = int(ships)
            elif(message == "@menu"):
                username = self.server.recv(1024).decode('utf-8')
                print(f"self.username: {self.username}, username: {username}")
                self.menu(username)

            elif(message == "@myBoard"):
                username = self.server.recv(1024).decode('utf-8')
                if(self.username == username):
                    os.system("cls")
                    print(f"-- This is {username}'s board --\n")
                    self.printBoard(self.playerBoard)
                    input("\nIntroduce any key in order to continue: ")
                    messageSender(self.server, "end")
                else:
                    os.system("cls")
                    print(f"The user: {username} has selected \"My board\", you can't see his board")

            elif(message == "@sendAction"):
                username = self.server.recv(1024).decode('utf-8')
                print(username)
                print(self.username)
                if(username == self.username):
                    messageSender(self.server, self.actionPlayerBoard)

            elif(message == "@sendBoard"):
                username = self.server.recv(1024).decode('utf-8')
                print(username)
                print(self.username)
                if(username == self.username):
                    messageSender(self.server, self.lives)
                    time.sleep(0.2)
                    messageSender(self.server, self.playerBoard)

            elif(message == "@myAction"):
                enemyActionBoard = self.server.recv(1024).decode('utf-8')
                enemyActionBoard = eval(enemyActionBoard)
                username = self.server.recv(1024).decode('utf-8')
                os.system("cls")
                print(f"-- This is {username}'s action board --\n")
                self.printBoard(enemyActionBoard)
                if(username == self.username):
                    input("\nIntroduce any key in order to continue: ")
                    messageSender(self.server, "end")

            elif(message == "@getPoints"):
                username = self.server.recv(1024).decode('utf-8')
                if(username == self.username):
                    messageSender(self.server, self.lives)

            elif(message == "@points"):
                pointsUser1 = self.server.recv(1024).decode('utf-8')
                pointsUser2 = self.server.recv(1024).decode('utf-8')
                username = self.server.recv(1024).decode('utf-8')
                user1 = self.server.recv(1024).decode('utf-8')
                user2 = self.server.recv(1024).decode('utf-8')
                
                self.printPoints(points=(pointsUser1, pointsUser2), usernames=(user1, user2))
                
                if(username == self.username):
                    input("\nIntroduce any key in order to continue: ")
                    messageSender(self.server, "end")

            elif(message == "@attack"):
                username = self.server.recv(1024).decode('utf-8')
                board = self.server.recv(1024).decode('utf-8')
                if(username == self.username):
                    self.attack(board)

            elif(message == "@printAttack"):
                username = self.server.recv(1024).decode('utf-8')
                badUsername = self.server.recv(1024).decode('utf-8')
                action = self.server.recv(1024).decode('utf-8')
                cords = self.server.recv(1024).decode('utf-8')

                os.system("cls")
                if(action == "Water"):
                    print(f"Water!! The user: {username} shot in the coordinates: {cords}")
                    if(self.username == badUsername):
                        messageSender(self.server, self.lives)  
                    else:
                        time.sleep(4)
                        messageSender(self.server, "end")
                else:
                    print(f"Touch!! The user: {username} shot in the coordinates: {cords}")
                    if(self.username == badUsername):
                        self.lives -= 1
                        messageSender(self.server, self.lives)
                        time.sleep(4)
                    else:
                        time.sleep(4)
                        messageSender(self.server, "end")
                

            elif(message == "@end"):
                msg = self.server.recv(1024).decode('utf-8')
                os.system("cls")
                print(msg)
                time.sleep(3)
                raise KeyboardInterrupt

            elif(message == "@exit"):
                raise KeyboardInterrupt

#?#################################### Filling all the boards ###############################################

    def fillBoards(self, ships):
        self.playerBoard = [[0 for x in range(self.DIMENSIONS)] for y in range(self.DIMENSIONS)]
        self.actionPlayerBoard = [[0 for x in range(self.DIMENSIONS)] for y in range(self.DIMENSIONS)]
        for i in range(self.DIMENSIONS):
            for y in range(self.DIMENSIONS):
                self.playerBoard[i][y] = '-'
                self.actionPlayerBoard[i][y] = '-'

        for i in range(int(ships)):
            latitude = random.randint(1, self.DIMENSIONS-1)
            longitude = random.randint(1, self.DIMENSIONS-1)

            if(self.playerBoard[latitude][longitude] == '-'):
                self.playerBoard[latitude][longitude] = '*'

#?#################################### Main menu and send of the text number introduces by the user ###############################################

    def menu(self, username):
        begin = False
        while(begin != True):
            os.system("cls")
            print(f"It's the turn of the user: \"{username}\"")
            print("1 - My board\n2 - My action board\n3 - Enemy action board\n4 - Points\n5 - Attack\n6 - Exit")
            if(username == self.username):
                userSelection = input("Your option: ")
                if(userSelection.isdigit()):
                    if(int(userSelection) >= 1 and int(userSelection) <= 6):
                        self.selectionText(int(userSelection))
                        break

                errors("Value error: The inserted value is not correct, please try again")

            else:
                begin = True

    def selectionText(self, userInput):
        if(userInput == 1):
            messageSender(self.server, "@myBoard")
        elif(userInput == 2):
            messageSender(self.server, "@myAction")
        elif(userInput == 3):
            messageSender(self.server, "@enemyAction")
        elif(userInput == 4):
            messageSender(self.server, "@points")
        elif(userInput == 5):
            messageSender(self.server, "@attack")
        elif(userInput == 6):
            messageSender(self.server, "@exit")
            messageSender(self.server, self.username)
            raise KeyboardInterrupt

#?#################################### Attacking enemy ###############################################

    def attack(self, enemyBoard):
        enemyBoard = eval(enemyBoard)

        words = []
        Alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        begin = False
        while(begin != True):
            os.system("cls")
            print("-- This is your action board --\n")
            self.printBoard(self.actionPlayerBoard)
            attackPosition = input("\nType the coordenates of your shoot --> ")

            if(len(attackPosition) == 2):
                for i in attackPosition:
                    words.append(i)
            

                if(words[0].upper() in Alphabet and words[1].isdigit()):
                    found = False
                    for i in range(len(Alphabet)):
                        if(Alphabet[i] == words[0].upper()):
                            found = True
                            firstDimension = i
                            secondDimension = int(words[1])

                            if(self.actionPlayerBoard[firstDimension][secondDimension] == '-'):
                                if(enemyBoard[firstDimension][secondDimension] == '-'):
                                    messageSender(self.server, "Water")
                                    messageSender(self.server, f"{Alphabet[i]}{secondDimension}")
                                    self.actionPlayerBoard[firstDimension][secondDimension] = "O"
                                    begin = True
                                    break
                                else:
                                    messageSender(self.server, "Touch")
                                    messageSender(self.server, f"{Alphabet[i]}{secondDimension}")
                                    self.actionPlayerBoard[firstDimension][secondDimension] = "*"
                                    begin = True
                                    break
                            else:
                                print("You already shoot in that cordinates, please try again...")
                                time.sleep(3)
                                words.clear()
                                break
                    
                    if(found == False):
                        errors("Value error: The inserted value is not correct, please try again 3")
                        words.clear()


                else:
                    errors("Value error: The inserted value is not correct, please try again 2")
                    words.clear()

            else:
                errors("Value error: The inserted value is not correct, please try again 1")
             

if __name__ == '__main__':
    try:
        begin = False
        while(begin != True):
            userInput = startMenu.menu()
            if(userInput == 1):
                serverCredentials = credentials.welcome()

                try:
                    clientObject = gameClient()
                    clientObject.connectServer(serverCredentials)

                except socket.gaierror:
                    errors("Value error: The inserted value is incorrect, please try again")

            else:
                begin = True
                os.system("cls")
                print("Exiting...")

    except KeyboardInterrupt:
        os.system("cls")
        print("Exiting...")

    except ConnectionResetError or ConnectionRefusedError:
        errors("Connection refused: The server is offline")