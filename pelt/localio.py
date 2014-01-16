#PELT Local I/O
#Created October 19, 2013 at 23:37

from i18n import m
import config, pelt
import time, os, pickle, sys, random, locale, re
#import menu

try:
	import console, notification
	from scene import *
	config.pc = 'iphone'
	config.ios = True
except ImportError as error:
	import colorama, easygui #, menu, pygame
	colorama.init()
	#pygame.init()
	config.pc = 'computer'
	config.ios = False

try: styles = colorama.Fore.WHITE #Set color to default...
except: styles = '' #...and set to a blank string if on iOS

#Function that prints the messages
def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", ignorecolor=False, noreset=False, r=0, s=0):
	#s = 0 # TEMPORARY LINE
	if not noreset: color('reset')
	# modifier = caps, title, lower, normal (when modifier isn't present)
	try:
		if dict: msg = m(msg, color=True)
	except KeyError:
		if msg == '': pass
		else: msg = "WARNING: "+msg+" is not a valid keyword."
	if addon: 
		try: msg = msg % addon
		except TypeError: msg = 'Hey, this message is broken.  Tried to print "%s" and add "%s".' %(msg, addon)
	if modifier == 'caps': msg = msg.upper()
	elif modifier == 'title': msg = msg.title()
	elif modifier == 'lower': msg = msg.lower()
	if r == 0:
		style = False
		colour = ''
		for c in msg:
			if not ignorecolor:
				if c == "[": style = True
				elif c == "]":
					style = False
					color(colour)
					colour = ''
				elif style: colour += c
			
				else:#if not style and c != "]":
					sys.stdout.write(c)
					if not noscroll:
						sys.stdout.flush()
						time.sleep(config.scroll)
			
			else:
				sys.stdout.write(c)
				if not noscroll:
					sys.stdout.flush()
					time.sleep(config.scroll)
		
		if newline: sys.stdout.write('\n')
		if not noreset: color('reset')
		sys.stdout.flush()
		time.sleep(s)
	elif r == 1: return msg

def newline():
	sys.stdout.write('\n')
	sys.stdout.flush()

class guiInput():
	def __init__(self):
		self.network = False
		self.firstmsg = True
	
	def network(self):
		try:
			if self.network:
				console.hide_activity()
				self.network = False
			else:
				console.show_activity()
				self.network = True
		except: pass

	def text(self, msg):
		try: choice = console.input_alert(msg, '', '', 'Ok')
		except:
			choice = easygui.enterbox(msg=msg, title='PELT Engine - '+pelt.gametitle+' v'+str(pelt.version))
		return choice
	
	def choice(self, msg, choices, window=False):
		strings = [str(c) for c in choices]
		if config.ios:
			temp = strings[-1]
			if temp == m('quit') or temp == m('back') or temp == m('cancel'): strings.remove(temp)
			try:
				if len(strings) == 1: choice = console.alert(msg, '', strings[0])
				elif len(strings) == 2: choice = console.alert(msg, '', strings[0], strings[1])
				elif len(strings) == 3: choice = console.alert(msg, '', strings[0], strings[1], strings[2])
				else:
					waiting = True
					page = 1
					while waiting:
						try:
							b = 2
							choice = console.alert(msg, '', strings[0+(page-1)*2], strings[1+(page-1)*2], "Next Page")
						except IndexError: 
							b = 1
							try: 
								choice = console.alert(msg, '', strings[0+(page-1)*2], output('next', r=1))
							except IndexError:
								page = 0
								choice = 1+b
							except KeyboardInterrupt: return 0
						except KeyboardInterrupt: return 0
						if choice == 1+b:
							if page <= len(strings) // 2: page += 1
							else: page = 1
						else:
							number = choice+(page-1)*2
							waiting = False
				number = choice
			except KeyboardInterrupt: return 0
		else:
			if not window:
				choice = easygui.buttonbox(msg=msg, title='PELT Engine - '+pelt.gametitle+' v'+str(pelt.version), choices=strings)
				i = 1
				for c in strings:
					if choice == c: number = i
					else: i += 1
			else:
				choice = menu.main(strings)
				time.sleep(0.1)
				return choice
		temp = str(choice)
		if temp == m('quit') or temp == m('back') or temp == m('cancel'): return 0
		return choices[number-1]

	def alert(self, data):
		nocolordata = ''
		color=False
		for c in data:
			if c == '[':
				color=True
			elif c == ']':
				color=False
			elif not color:
				nocolordata += c
		msg = nocolordata
		if config.ios:
			try: console.alert('',msg)
			except KeyboardInterrupt: pass
		else: easygui.msgbox(title='PELT Engine - '+pelt.gametitle+' v'+str(pelt.version), msg=msg)
	
	def multtext(self, msg, fields, optfields = None):
		orgmsg = str(msg)
		disfields = []
		for field in fields: disfields.append(field)
		if optfields: disfields += ['%s (Optional)' %f for f in optfields]
		if config.ios:
			response = {}
			for field in fields:
				waiting = True
				while waiting:
					choice = self.text(msg+"  Enter the "+str(field))
					if choice != "": waiting = False
				response[field] = choice
			for field in optfields:
				fields.append(field)
				choice = self.text(msg+"  Enter the "+str(field))
				response[field] = choice
		else:
			waiting = True
			while waiting:
				waiting = True
				temp = False
				while waiting:
					response = easygui.multenterbox(msg, 'PELT Engine - '+pelt.gametitle+' v'+str(pelt.version), disfields)
					x = 0
					if response:
						for resp in response:
							if x <= len(fields):
								if resp == "":
									msg = "One or more required fields are not filled out.  "+orgmsg
									temp = True
									break
							else: break
							x += 1
						if not temp: waiting = False
						else: temp = False
					else: waiting = False
		if not response: return None
		return response
		
	def notification():
		if ios: pass
		else:
			if pc == "Darwin": pass
			

class TerminalInput():
	def __init__(self):
		self.network = False
		self.firstmsg = True
	
	def network(self):
		try:
			if self.network:
				console.hide_activity()
				self.network = False
			else:
				console.show_activity()
				self.network = True
		except: pass

	def text(self, msg): return raw_input(msg+"  ")
	
	def choice(self, msg, choices, window=False):
		choicerange = range(len(choices))
		for i in choicerange:
			output("[yellow]%d: [reset]%s" %(i+1, choices[i]), dict=False)
		while True:
			choic = pelt.str_to_int(raw_input("%s  " %msg), default=0)
			if choic-1 not in choicerange: continue
			if choices[choic-1] == m('quit') or choices[choic-1] == m('back') or choices[choic-1] == m('cancel'): return 0
			return choices[choic-1]

	def alert(self, msg): output(msg, dict=False)
	
	def multtext(self, msg, fields, optfields = None):
		orgmsg = str(msg)
		disfields = []
		for field in fields: disfields.append(field)
		if optfields: disfields += ['%s (Optional)' %f for f in optfields]
		response = {}
		for field in fields:
			waiting = True
			while waiting:
				choice = self.text(msg+"  Enter the "+str(field))
				if choice != "": waiting = False
			response[field] = choice
		for field in optfields:
			fields.append(field)
			choice = self.text(msg+"  Enter the "+str(field))
			response[field] = choice
		if not response: return None
		return response

if config.gui: getInput = guiInput()
else: getInput = TerminalInput()

def color(color):
	global styles
	try: #If styles is greater than 20, reset...
		if len(styles) > 20: styles = colorama.Fore.WHITE
		styles = colorama.Fore.WHITE
	except: pass #...or pass if on iOS
	if color == 'red':
		try: console.set_color(1.0, 0.0, 0.0)
		except: styles += colorama.Fore.RED
	elif color == 'green':
		try: console.set_color(0.2, 0.8, 0.2)
		except: styles += colorama.Fore.GREEN
	elif color == 'blue':
		try: console.set_color(0.0, 0.0, 1.0)
		except: styles += colorama.Fore.CYAN
	elif color == 'yellow':
		try: console.set_color(0.6, 0.6, 0.1)
		except: styles += colorama.Fore.YELLOW
	elif color == 'darkblue':
		try: console.set_color(0.6, 0.6, 1.0)
		except: styles += colorama.Fore.BLUE
	elif color == 'magneta':
		try: console.set_color(1.0, 0.2, 1.0)
		except: styles += colorama.Fore.MAGENTA
	elif color == 'reset':
		try:
			console.set_color(0.2, 0.2, 0.2)
			console.set_font()
		except: styles += colorama.Fore.WHITE
	elif color == 'random':
		try: console.set_color(random.random(),random.random(),random.random())
		except:
			list = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN, colorama.Fore.WHITE]
			styles += random.choice(list)
	elif color == 'bold':
		try: console.set_font('Helvetica', 32.0)
		except: pass
	else: output('colorerror')
	if styles:
		sys.stdout.write(styles)
		sys.stdout.flush()
