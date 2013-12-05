#PELT Local I/O
#Created October 19, 2013 at 23:37

from i18n import m
import config
import time, os, pickle, sys, random, locale, re
import easygui
#import menu

try:
	import console, notification
	from scene import *
	config.pc = 'iphone'
	config.ios = True
except ImportError:
	import colorama, easygui #, menu, pygame
	colorama.init()
	#pygame.init()
	config.pc = 'computer'
	config.ios = False

styles = ''

#Function that prints the messages
def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0, s=0):
	#s = 0 # TEMPORARY LINE
	# modifier = caps, title, lower, normal (when modifier isn't present)
	try:
		if dict: msg = m(msg)
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
		for c in msg:
			sys.stdout.write(c)
			if not noscroll:
				sys.stdout.flush()
				time.sleep(config.scroll)
		if newline: sys.stdout.write('\n')
		if noscroll: sys.stdout.flush()
		sys.stdout.flush()
		time.sleep(s)
	elif r == 1: return msg

def newline():
	sys.stdout.write('\n')
	sys.stdout.flush()

class Input():
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
		except: choice = easygui.enterbox(msg=msg, title='PELT Engine - '+gametitle+' v'+str(version))
		return choice
	
	def choice(self, msg, choices, window=False):
		strings = [str(c) for c in choices]
		if ios:
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
				choice = easygui.buttonbox(msg=msg, title='PELT Engine - '+gametitle+' v'+str(version), choices=strings)
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

	def alert(self, msg):
		try:
			try: console.alert('',msg)
			except KeyboardInterrupt: pass
		except:
			easygui.msgbox(title='PELT Engine - '+gametitle+' v'+str(version), msg=msg)
	
	def multtext(self, msg, fields, optfields = None):
		orgmsg = str(msg)
		disfields = []
		for field in fields: disfields.append(field)
		if optfields:
			for optfield in optfields: disfields.append(optfield+" (Optional)")
		try:
			response = []
			for field in fields:
				waiting = True
				while waiting:
					choice = console.input_alert(msg+"  Enter the "+str(field), '', '', 'Ok')
					if choice != "": waiting = False
				response.append(choice)
			for field in optfields:
				fields.append(field)
				choice = console.input_alert(msg+"  Enter the "+str(field), '', '', 'Ok')
				response.append(choice)
		except:
			waiting = True
			while waiting:
				waiting = True
				temp = False
				while waiting:
					response = easygui.multenterbox(msg, 'PELT Engine - '+gametitle+' v'+str(version), disfields)
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
		if response: dictresp = dict(zip(disfields, response))
		else: return None
		return dictresp

getInput = Input()

def color(color):
	global styles
	styles = ''
	if color == 'red':
		try: console.set_color(1.0, 0.0, 0.0)
		except: styles += colorama.Fore.RED
	elif color == 'green':
		try: console.set_color(0.2, 0.8, 0.2)
		except: styles += colorama.Fore.GREEN
	elif color == 'blue':
		try: console.set_color(0.0, 0.0, 1.0)
		except: styles += colorama.Fore.CYAN
	elif color == 'reset':
		try:
			console.set_color(0.2, 0.2, 0.2)
			console.set_font()
		except: styles += colorama.Fore.RESET
	elif color == 'random':
		try: console.set_color(random.random(),random.random(),random.random())
		except:
			list = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN, colorama.Fore.WHITE]
			styles += random.choice(list)
	elif color == 'bold':
		try: console.set_font('Helvetica', 32.0)
		except: pass
	else: output('colorerror')