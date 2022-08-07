
# Battleship-Multiplayer

This pythons scripts are a game application. This game is the known Battleship game
but, with a tiny random mechanic. The repo has in total 3 main files:

- server.py --> Server deployment script
- client.py --> Client connection
- modules.py --> Functions and libraries for the functionality of the scripts

This application is developed only for Windows operative system

# Explanation

In order to play the game it has to be deployed a game server (server.py) and
insert a valid device IP and port. In case you want to play in your network
insert your local IP. If you want to play only in your device insert the Loopback IP
(127.0.0.1)

It is recomended to insert port 9090 to not harm the normal functionality of the device

Is very important run the scripts in the workspace they are

The user's board in the game it's a 10x10 this means it has 100 boxes. The ships are created and placed
randomly. 

In order to execute processes in the game there has to be 2 player playing at the same time
# Requirements

This application only use one python library called Tabulate

#### Install Requirements

```
  pip install -r requirements.txt
```
```


____   ____.__        __                 __________                             
\   \ /   /|__| _____/  |_  ___________  \______   \ ___________   ____ ________
 \   Y   / |  |/ ___\   __\/  _ \_  __ \  |     ___// __ \_  __ \_/ __ \\___   /
  \     /  |  \  \___|  | (  <_> )  | \/  |    |   \  ___/|  | \/\  ___/ /    / 
   \___/   |__|\___  >__|  \____/|__|     |____|    \___  >__|    \___  >_____ \
                   \/                                   \/            \/      \/


```
This project is licensed under the terms of the Apache License 2.0