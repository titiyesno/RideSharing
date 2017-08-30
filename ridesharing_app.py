import socket
import select
import threading
import sys
import time

allow_delete = False
local_ip = socket.gethostbyname(socket.gethostname())

class rideserver(threading.Thread):
	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 5000
		self.mode = 'I'
		self.backlog = 5
		self.size = 1024
		self.threads = []
		threading.Thread.__init__(self)

	def open_socket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		self.server.bind((self.host, self.port))
		self.server.listen(5)

	def run(self):
		self.open_socket()
		input = [self.server, sys.stdin]
		running = 1
		while running:
			inputready, outputready, exceptready = select.select(input, [], [])

			for s in inputready:
				if s == self.server:
					print s
					c = rideserverfunc(self.server.accept())
					c.start()
					self.threads.append(c)
				elif s == sys.stdin:
					junk = sys.stdin.readline()
					running = 0

		self.server.close()
		for c in self.threads:
			c.join()

class rideserverfunc(threading.Thread):
	def __init__(self, (client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.rest = False
		self.pasv_mode = False
		self.size = 1024
		self.running = True

	def run(self):
		self.client.send('220 Welcome!\r\n')
		while self.running:
			cmd = self.client.recv(self.size)
			if not cmd:
				break
			else:
				print 'recv: ',cmd
				try:
					func=getattr(self, cmd[:4].strip().upper())
					func(cmd)
				except Exception,e:
					print e
					self.client.send('500 Sorry.\r\n')

	def PRES(self,cmd):
		if cmd.strip().split()[1] == "Anonymous":
			self.client.send("Please identify yourself\r\n")
		else:
			global flag_role
			global user
			global driver
			driver = []
			flag_role = cmd.strip().split()[2]
			user = cmd.strip().split()[1]
			#print cmd
			if flag_role == "0":
				self.client.send("Hai "+user+"\nYou're identified as a passenger\r\n")
			else:
				driver.append(user)
				self.client.send("Hai "+user+"\nYou're identified as a driver\r\n")

	def RQST(self,cmd):
		if not driver:
			self.client.send("Sorry. There is no driver available for you\r\n")
		else:
			self.client.send("Please wait\r\n")

if __name__=='__main__':
	ride = rideserver()
	ride.daemon = True
	ride.start()
	raw_input('Enter to end...\n')
