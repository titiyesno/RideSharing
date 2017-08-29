import socket
import sys


server_addr = ('127.0.0.1',5000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)

sys.stdout.write(client.recv(1024))
sys.stdout.write('>>')

try:
	while True:
		#print i
		msg = sys.stdin.readline()

except KeyboardInterrupt:
	client.close()

	sys.exit(0)