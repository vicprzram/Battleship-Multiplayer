import os
import sys
import time
import socket
import datetime
import threading
import random
from tabulate import tabulate

def errors(msg):
    os.system("cls")
    print(f"[!] {msg}")
    time.sleep(5)

def messageSender(client, msg):
    
    client.send(bytes(f"{msg}".encode('utf-8')))
    time.sleep(0.2)

class credentials():

    def welcome():
        begin = False
        while(begin != True):
            os.system("cls")
            print("-- Welcome to battleship 2022 --\n")
            print("This game is created by: Víctor Pérez\n")
            print("Please introduce the server credentials to create/connect a server\n")
            host = input("Server IP: ")
            port = input("Server port: ")

            hostArray = list(host)

            bad = False

            for i in hostArray:
                if(i.isalpha()):
                    bad = True
                    break

            if(port.isdigit() and bad == False):
                begin = True
            else:
                errors("Value error: The port value has to be a number and the IP has to be a valid IP, please try again")

        return (host, port)

class startMenu():
    def menu():
        begin = False
        while(begin != True):
            os.system("cls")
            print("-- Welcome to battleship 2022 --\n")
            print("This game is created by: Víctor Pérez\n")
            print("Choose an option:\n\n1 - Start/Connect to a server\n2 - Exit\n")
            userInput = input("Your option: ")

            if userInput.isdigit() and (userInput == "1" or userInput == "2"):
                begin = True
                userInput = int(userInput)
                return userInput
            else:
                errors("Value error: The inserted value is incorrect, please try again")