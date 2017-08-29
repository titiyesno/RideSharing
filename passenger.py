import socket
import sys


server_addr = ('127.0.0.1',5000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_addr)

sys.stdout.write(client.recv(1024))


i=0
flag_passenger=0

try:
	while True:
		sys.stdout.write('>>')
		msg = sys.stdin.readline()

		if i==0:
			if "PRES" not in msg:
				client.send("PRES Anonymous")
				pesan = client.recv(1024)
				sys.stdout.write(pesan)
			else:
				msg = msg + " " + str(flag_passenger)
				client.send(msg)
				pesan = client.recv(1024)
				sys.stdout.write(pesan)

		else:
			if "PRES" in msg:
				msg = msg + " " + str(flag_passenger)
				
			client.send(msg)
			pesan = client.recv(1024)
			sys.stdout.write(pesan)

		i+=1


except KeyboardInterrupt:
	client.close()

	sys.exit(0)

