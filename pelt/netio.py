# -*- coding: utf-8 -*-

#PELT Network I/O
#Created October 17, 2013 at 11:04

from pelt import m

socket = None

def activate(**kwargs):
	"""Synchronize the netio.py and the game's global variables."""
	global socket
	socket = kwargs.get("socket")
	

def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0, s=0):
	"""Send a message to the remote client."""
	global socket
	socket.send(m(msg))

def newline():
	"""Tell the remote client to print a newline."""
	pass

class Input():
	"""Ask the remote client for input."""
	
	def __init__(self):
		"""Initialize class object variables."""
		pass
	
	def network(self):
		"""Tell the remote client that it is accessing network resources not from game server."""
		pass
	
	def text(self, msg): 
		"""Ask the remote client for text feedback."""
		global socket
		output(msg)
		return socket.recv()
	
	def choice(self, msg, choices, window=False):
		"""Send the remote client a multiple choice question and wait for response."""
		pass
	
	def alert(self, msg):
		"""Tell the remote client to pop-up an alert box."""
		pass

"""
activate
output
newline
GetInput:
	__init__
	network
	text
	choice
	alert
"""