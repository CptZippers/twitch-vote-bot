#!/usr/bin/python
# bot.py

from time import sleep
import socket
import re

HOST = "irc.twitch.tv"              
PORT = 6667                         
NICK = ""            
PASS = "oauth:" 
CHAN = "#channel"                   

CHAT_MSG=re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
s.send("CAP REQ :twitch.tv/tags\r\n".format(CHAN).encode("utf-8"))
while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        if len(response.split(" ",1)) > 1: #need to check because not all senders have tags apparently
            tags, msg = response.split(" ", 1)
            username = re.search(r"\w+", msg).group(0) # return the entire match
            message = CHAT_MSG.sub("", msg)
            print(username + ": " + message)
            first = message.split()[0]
            if first == "!vote":
                f = open("votes.txt","r")
                lines = f.readlines()
                f.close()
                f = open("votes.txt","w")
                for line in lines:
                    if username not in line:
                        f.write(line)
                    else:
                        print("Already voted")
                f.close()
                target = open('votes.txt', 'a')
                if len(message.split())>=2:
                    submission = message.split(' ', 1)[1]
                else:
                    submission = "none"
                if "subscriber=1" in tags:
                    target.write("SUB " + username + " " + submission + "\n")
                else:
                    target.write(username + " " + submission + "\n")
                target.close()
        if username == "twitchnotify" and "subscribed" in message:
            print("New Sub") #This section was used for the silly string machine! I removed it all though as it was exclusive to raspberry pi
    sleep(0.1)