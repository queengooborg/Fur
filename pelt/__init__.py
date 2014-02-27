#PELT Engine
#Created September 12, 2013 at 17:17

peltvers = 154

dependencies = {
	'iOS': [
		{
			'name': 'Pythonista',
			'link': 'the App Store'
		}
	],
	'Computer': [
		{
			'name': 'Colorama',
			'link': 'https://pypi.python.org/pypi/colorama/'
		},
		{
			'name': 'EasyGUI',
			'link': 'http://easygui.sourceforge.net/'
		},
		{
			'name': 'PyGame',
			'link': 'http://www.pygame.org/'
		},
		{
			'name': 'PyRt-Midi',
			'link': 'https://github.com/tedr56/PyRtMidi',
		}
	],
	'Mac': [
		{
			'name': 'Terminal Notifier',
			'link': 'sudo gem install terminal-notifier'
		}
	],
	'Windows': [
		{
			'name': 'PyWin32',
			'link': 'http://sourceforge.net/projects/pywin32/files/pywin32/'
		}
	],
	'Linux': []
}

import time, os, pickle, sys, random, locale, re, argparse
from platform import system as pcinfo
import traceback as tb
from color import *
from credit import credit

from localio import output, newline, getInput
import config, level
from i18n import m, setlang
from errors import *
from item import *

try:
	import console, notification
	from scene import *
	config.pc = 'iphone'
	config.ios = True
except ImportError:
	import colorama, easygui, pygame
	from menu import dumbmenu as dm
	colorama.init()
	#pygame.init()
	
	size = width, height = 720, 680 #Initialize the size
	screen = pygame.display.set_mode(size)
	#size = width, height = screen.get_size() #Get the screen size, for reasons that may come back
	pygame.font.init()
	myfont = pygame.font.Font(None, 32)
	
	screen.fill(BLACK)
	
	config.pc = pcinfo()
	config.ios = False

def sync(vers, officialvers, langversneed, debugmode, title, auth, modules=[], args=[]):
	global version, officialversion, langversneeded, debug, gametitle, author, peltvers, size, width, height, screen, myfont

	version = config.version = vers
	officialversion = config.officialversion = officialvers
	langversneeded = langversneed
	debug = debugmode
	gametitle = config.gametitle = title
	author = config.author = auth
	config.args = args
	
	#from localio import output, newline, getInput, color
	
	#Print the title, author, and version
	color('reset')
	output('author', addon=author)
	output('version', addon=(officialversion, peltvers), s=2)
	newline()
	output('title', addon=gametitle, s=3)

#Save and load functions
def saveload(save, overwarning=False, overaddon=False):
	waiting = True
	while waiting:
		saves = range(10)
		saveslist = list(saves)
		#path = os.path
		#os.listdir(path)
		for s in saves:
			s+=1
			try:
				if pc == 'computer': temp = 'saves/save'
				else: temp='save'
				with open(temp+str(s), 'rb') as handle:
					file = list(pickle.load(handle))
					output('save2', addon=[str(s), file[2]], noscroll=True)
					saveslist[s-1] = output('save2', addon=[str(s), file[2]], r=1)
			except:
				if save: output('save1', addon=str(s), noscroll=True)
				saveslist[s-1] = output('save1', addon=str(s), r=1)
		output('')
		if save: choice = getInput.choice(output('save3', r=1),saveslist)
		else: choice = getInput.choice(output('save4', r=1),saveslist)
		if choice == 'c': return False
		choice = str_to_int(choice[4:])
		if choice > 0 and choice <= len(saves):
			if pc == 'computer': response = 'saves/save'+str(choice)+".save"
			else: response = 'save'+str(choice)+".save"
			try:
				with open(response, 'rb') as handle:
					if handle:
						overwait = True
						handle = pickle.load(handle)
						if save:
							while overwait:
								addon = [file[0], file[1], file[2]]
								overwrite = getInput.choice(output('savewarning', addon=addon, r=1),[output('yes', r=1),output('no', r=1)])
								if overwrite == 1: return response
								elif overwrite == 2: overwait = False
								else: output('inputerror')
						else: return response
			except: return response
		else:
			output('saveerror')
			output('')

#converts a string to an integer and returns -1 (or default) if string is not a number
def str_to_int(text, default=-1):
	try: response = int(text)
	except ValueError: return default
	return response

