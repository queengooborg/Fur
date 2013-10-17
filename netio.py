def activate():
	"""Synchronize the netio.py and the game's global variables."""
	pass

def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0, s=0):
	"""Send a message to the remote client."""
	pass

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
		pass
	
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