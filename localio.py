import pelt
import time, os, pickle, sys, random, locale, re
import easygui

def activate():
	global scroll, ios, pc, gametitle, version
	scroll = pelt.scroll
	ios = pelt.ios
	pc = pelt.pc
	gametitle = pelt.gametitle
	version = pelt.version
	if ios:
		import console, notification
		from scene import *
	else:
		import colorama, easygui #, menu, pygame
		colorama.init()
		#pygame.init()

#Function that prints the messages
def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0, s=0):
	global scroll
	s = 0 # TEMPORARY LINE
	# modifier = caps, title, lower, normal (when modifier isn't present)
	try:
		if dict: msg = pelt.m(msg)
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
				time.sleep(scroll)
		if newline: sys.stdout.write('\n')
		if noscroll: sys.stdout.flush()
		sys.stdout.flush()
	elif r == 1: return msg
	time.sleep(s)

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
			if temp == pelt.m('quit') or temp == pelt.m('back') or temp == pelt.m('cancel'): strings.remove(temp)
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
				number = choice
		temp = str(choice)
		if temp == pelt.m('quit') or temp == pelt.m('back') or temp == pelt.m('cancel'): return 0
		return choices[number-1]

	def alert(self, msg):
		try:
			try: console.alert('',msg)
			except KeyboardInterrupt: pass
		except:
			easygui.msgbox(title='PELT Engine - '+gametitle+' v'+str(version), msg=msg)

getInput = Input()