import socket
import select
import sys
import requests
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
Port = 5000
server.connect((IP_address, Port))

flag_passenger = 0

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
            	message = message + " " + str(flag_passenger)
            	name = message.split()[1]
            elif message.split()[0] == "REQUEST":
            	send_url = 'http://freegeoip.net/json'
            	r = requests.get(send_url)
            	j = json.loads(r.text)
            	lat = j['latitude']
            	lon = j['longitude']
            	message = message + " " + name + " " + str(lat) + " " + str(lon)

            server.send(message)
            # sys.stdout.write(">>")
            # sys.stdout.write(message)
            sys.stdout.flush()

server.close()
