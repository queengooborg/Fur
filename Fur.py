#Fur
#Text-based RPG by Dark Tailed
#Created May 10, 2013 at 15:14 
#Last edited August 10, 2013 at 20:36
version=307
langversneeded=0.1
#Dependencies:
	#For iPad:
	#	Pythonista
	#For PC:
	#	Colorama: https://pypi.python.org/pypi/colorama/
	#	EasyGUI: http://easygui.sourceforge.net/
	#	PyGame: http://www.pygame.org/

#Import modules
try:
	import console, notification
	from scene import *
	pc = 'iphone'
	ios = True
except ImportError:
	import pygame
	from modules import *
	colorama.init()
	pygame.init()
	pc = 'computer'
	ios = False

import time, os, pickle, sys, random, locale

#initialize variables
scrollspeed='Medium'
scroll=0.03
lang=None
annoy=False
devplayer=True
dolang = False

try:
	with open('options', 'rb') as handle:
		handle = pickle.load(handle)
		lang = handle[0]
		scrollspeed = handle[1]
		if scrollspeed == 'Fast': scroll = 0.01
		elif scrollspeed == 'Medium': scroll = 0.03
		elif scrollspeed == 'Slow': scroll = 0.05
		annoy = handle[2]
		devplayer = handle[3]
	if lang == "English":
		#with open('english.lang', 'rb') as handle2: msgs = pickle.load(handle2)
		pass
except: 

loc=None
gender=None
player_name=None
player_last=None
player_species=None
frnd_gender=None
frnd_gndrpn=None
frnd_nane=None

species = ["Wolf","Cat","Dragon","Bear","Fox","Mouse","Bird","Otter"]
styles = ''

try: console.clear()
except: pass
	#os.console('cls')
	#os.console('clear')

getInput = getinput()

sandwich = Food('sandwich', 'A ham and cheese on rye bread.', False)
p1MainRoom = Room('Main Room', items = [sandwich],doors = [Door('northwest', 'Balcony'), Door('northeast', 'Hallway'), Door('southeast', 'Play Room'), Door('southwest', 'Chest Room', key="Bronze")])
p1Balcony = Room('Balcony', items = [], doors=[Door('south', 'Main Room')])
p1Hallway = Room('Hallway', items = [], doors=[Door('south', 'Main Room'), Door('west','Garden', key="A")])

if not lang: language()
if pc == 'iphone':
	choice = getInput.choice(output(149, r=1), ['iPhone','iPad'])
	if choice == 1: pc = 'iPhone'
	elif choice == 2: pc = 'iPad'
	else: quit(output(150, r=1), nosave=True)

mainmenu()

if len(sys.argv) > 1:
	arg = sys.argv[1:]
	if "nostory" in arg:
		loc = 'p1MainRoom'
		gameplay()
	elif "betatester" in arg: devplayer = True
	elif "annoy" in arg: annoy = True

start()
part1()
