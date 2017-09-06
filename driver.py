import socket
import select
import sys
import requests
import json
import threading
import datetime
from math import sin, cos, sqrt, atan2, radians

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = '127.0.0.1'
Port = 5000
server.connect((IP_address, Port))
flag_driver = 1

global klien

def send_mylocation():
    global t
    t = threading.Timer(5.0, send_mylocation)
    t.start()
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    msg = "APPROACH " + klien + " " + str(lat) + " " + str(lon)
    server.send(msg)

def get_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6373.0 * c
    return distance

def get_time(start, end):
    time = end - start
    return time

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
                message = message + " from " + name + ", to " + klien
                server.send(message)
                send_url = 'http://freegeoip.net/json'
                r = requests.get(send_url)
                j = json.loads(r.text)
                lat1 = j['latitude']
                lon1 = j['longitude']
                startime = datetime.datetime.now().replace(microsecond=0)
            elif message.split()[0] == "END":
                endtime = datetime.datetime.now().replace(microsecond=0)
                send_url = 'http://freegeoip.net/json'
                r = requests.get(send_url)
                j = json.loads(r.text)
                lat2 = j['latitude']
                lon2 = j['longitude']
                distance = get_distance(lat1, lon1, lat2, lon2)
                time = get_time(startime, endtime)
                message = message + " from " + name + ", to " + klien + ", distance: " + str(distance) + " km " + ", time " + str(time)
                server.send(message)
            
            sys.stdout.flush()
server.close()