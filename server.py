import socket, select
import Fur
import pelt

HOST = ''
PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(4)

mastersock = sock
waitlist = [mastersock]

class socketFile(object):
	def __init__ (self, socket):
		self.socket = socket
	
	def read(self):
		return self.socket.recv(1024)
	
	def write(self, msg):
		return self.socket.send(msg)
	
	def flush(self): pass

while True:
	ready, _, _ = select.select(waitlist, [], [])
	for s in ready:
		if s == mastersock:
			newsock, peeraddr = s.accept()
			waitlist.append(newsock)
			
			sf = socketFile(newsock)
			pelt.localio.inputfd = pelt.localio.outputfd = sf
			
			Fur.init()