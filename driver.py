import socket
import select
import sys
import requests
import json
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = '127.0.0.1'
Port = 5000
server.connect((IP_address, Port))
flag_driver = 1

global klien
global t

def send_mylocation():
    t = threading.Timer(5.0, send_mylocation)
    t.start()
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    msg = "APPROACH " + klien + " " + str(lat) + " " + str(lon)
    server.send(msg)

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print message
        else:
            message = sys.stdin.readline()
            if message.split()[0] == "PRESENCE":
                message = message + " " + str(flag_driver)
                name = message.split()[1]
                server.send(message)
            elif message.split()[0] == "ACCEPT":
                message = message + " " + name
                klien = message.split()[1]
                server.send(message)
                send_mylocation()
            elif message.split()[0] == "START":
                t.cancel()
                message = message + " from " + name + " to " + klien
                server.send(message)
            
            # sys.stdout.write(">>")
            # sys.stdout.write(message)
            sys.stdout.flush()
server.close()