import socket
import select
from thread import *
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = '127.0.0.1'
Port = 5000
server.bind((IP_address, Port)) 
server.listen(100)
print "Waiting..."
list_of_clients=[]
passengers = {}
drivers = {}

def clientthread(conn, addr):
    conn.send("Welcome to ridesharing!")
    i=0
    while True:
            try:     
                message = conn.recv(2048)    
                if message:
                    # print "<" + addr[0] + "> " + message
                    # message_to_send = "<" + addr[0] + "> " + message
                    if i == 0:
                        if message.split()[0] != "PRESENCE":
                            conn.send("Please identify yourself")
                        elif message.split()[0] == "PRESENCE":
                            whoami(message,conn)
                    else:
                        if message.split()[0] == "PRESENCE":
                            whoami(message,conn)
                        elif message.split()[0] == "REQUEST":
                            conn.send("Processing request.. please wait")
                            send_request(message,conn)
                        elif message.split()[0] == "ACCEPT":
                            conn.send("Request accepted")
                            accept_request(message)
                        elif message.split()[0] == "APPROACH":
                            approach(message)
                        elif message.split()[0] == "START":
                            print "<" + addr[0] + "> " + message
                        elif message.split()[0] == "END":
                            print "<" + addr[0] + "> " + message
                        else:
                            conn.send("Command not found")
                else:
                    remove(conn)
            except:
                continue
            i+=1

def whoami(message,conn):
    if message.split()[2] == "0":
        passengers[message.split()[1]] = conn
        conn.send("You're identified as a passenger")
    else:
        drivers[message.split()[1]] = conn
        conn.send("You're identified as a driver")

def send_request(message,conn):
    if not drivers:
        conn.send("No drivers available")
        remove(conn)
    else:
        for drv in drivers:
            if drivers[drv] != conn:
                try:
                    drivers[drv].send(message.split()[1] + " need a ride. Lat: " + message.split()[2] + " Lon: " + message.split()[3])
                except:
                    drivers[drv].close()
                    remove(drivers[drv])

def accept_request(message):
    passengers[message.split()[1]].send("Driver " + message.split()[2] + " accept your request. Please wait")

def approach(message):
    passengers[message.split()[1]].send("Approaching... Lat: " + message.split()[2] + " Lon: " + message.split()[3])

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    
    list_of_clients.append(conn)
    print addr[0] + " connected"
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()