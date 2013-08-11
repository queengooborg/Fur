#Fur
#Text-based RPG by Dark Tailed
#Created May 10, 2013 at 15:14 
#Last edited August 10, 2013 at 23:51
version=308
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
	from pelt import *
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
styles = ''

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
except: language()

loc=None
gender=None
player_name=None
player_last=None
player_species=None
frnd_gender=None
frnd_gndrpn=None
frnd_nane=None

species = ["Wolf","Cat","Dragon","Bear","Fox","Mouse","Bird","Otter"]
for i in range(len(species)):
	temp = species[i].lower()
	species[i] = output(temp, r=1)

try: console.clear()
except: pass
	#os.console('cls')
	#os.console('clear')

sandwich = Food('sandwich', 'A ham and cheese on rye bread.', False)
p1MainRoom = Room('Main Room', items = [sandwich],doors = [Door('northwest', 'Balcony'), Door('northeast', 'Hallway'), Door('southeast', 'Play Room'), Door('southwest', 'Chest Room', key="Bronze")])
p1Balcony = Room('Balcony', items = [], doors=[Door('south', 'Main Room')])
p1Hallway = Room('Hallway', items = [], doors=[Door('south', 'Main Room'), Door('west','Garden', key="A")])

def quit(msg, nosave=False):
	global ios, devplayer
	if nosave: pass
	else: save()
	color('red')
	if ios and not devplayer: notification.schedule(output('mailto2', r=1), 15, 'Beep', output('mailto1', r=1))
	if msg: sys.exit(msg)
	else: sys.exit(0)

def save():
	global loc,gender,player_name,player_last,player_species,frnd_gender,frnd_gndrpn,frnd_nane,scrollspeed,scroll,devplayer
	#with open(reply+'-'+player_name, 'wb') as handle:
	reply = saveload(True)
	if reply:
		with open(reply, 'wb') as handle: pickle.dump([loc,gender,player_name,player_last,player_species,frnd_gender,frnd_gndrpn,frnd_nane,scrollspeed,scroll,devplayer], handle)

def load():
	global loc,gender,player_name,player_last,player_species,frnd_gender,frnd_gndrpn,frnd_nane,scrollspeed,scroll,devplayer
	try:
		reply = saveload(False)
		if reply:
			with open(reply, 'rb') as handle:
				file = pickle.load(handle)
				player_name = file[0]
				player_last = file[1]
				loc = file[2]
				gender = file[3]
				player_species = file[4]
				frnd_gender = file[5]
				frnd_gndrpn = file[6]
				frnd_nane = file[7]
				scrollspeed = file[8]
				scroll = file[9]
				devplayer = file[10]
			return True
		else: return False
	except IOError:
		output('saveerror')
		return False

#When starting the game, program must ask if the player is a boy or girl.
def start():
	global gender, frnd_gender, player_name, player_last, player_species, frnd_gndrpn, species
	waiting=True
	while waiting:
		temp = getInput.choice(output('setup1', r=1), [output('boy', r=1), output('girl', r=1)])
		if temp == 1:
			gender=output('boy', r=1, modifier="lower")
			frnd_gender=output('girl', r=1, modifier="lower")
			frnd_gndrpn=output('she', r=1)
		elif temp == 2:
			gender=output('girl', r=1, modifier="lower")
			frnd_gender=output('boy', r=1, modifier="lower")
			frnd_gndrpn=output('he', r=1)
		else: quit(output('quitmsg', r=1), nosave=True)
		waiting=False
	waiting = True
	while waiting:
		temp = getInput.text(output('setup2', r=1))
		temp = temp.title().split()
		try:
			player_last = temp[1]
			player_name = temp[0]
			waiting = False
		except:
			if temp:
				temp = temp[0]
				while waiting:
					temp2 = getInput.text(output('setup3', r=1, addon=temp))
					temp2 = temp2.title()
					if temp2:
						player_name = temp
						player_last = temp2
						waiting = False
					else: output('inputerror')
			else: output('inputerror')
	output('setup4', addon=[player_name, player_last])
	i = 0
	time.sleep(2)
	while i != 3:
		i += 1
		output(str(i))
		time.sleep(1)
	output('setup5')
	time.sleep(2)
	output('setup6')
	choice = getInput.choice(output('setup7', r=1), species)-1
	if choice == -1: quit(output('quitmsg', r=1), nosave=True)
	player_species = species[choice]
	output('setup8', addon=[player_species,player_species])
	time.sleep(4)

#part 1 init
def part1():
	global loc,gender,player_name,player_last,frnd_gender,frnd_nane,frnd_last,devplayer
	playing = True
	output(66)
	time.sleep(2)
	output(67)
	time.sleep(2)
	output(68)
	time.sleep(3)
	output(69, addon=player_species)
	time.sleep(2)
	output(70)
	time.sleep(2)
	output(71, addon=[frnd_gender, frnd_gender])
	time.sleep(4)
	output(72)
	time.sleep(3)
	if frnd_gndrpn == output(29, r=1): temp = output(29, r=1, modifier='title')
	else: temp = output(26, r=1, modifier='title')
	if frnd_gender == output(25, r=1): temp2 = output(147, r=1)
	else: temp2 = output(148, r=1)
	output(73, addon=[frnd_gender, temp, temp2, temp2])
	time.sleep(0.5)
	output(74)
	time.sleep(0.5)
	output(75)
	time.sleep(2)
	output(76, newline=False)
	time.sleep(1)
	waiting = True
	while waiting:
		frnd_name=getInput.text(output(77, r=1, addon=[frnd_gndrpn, frnd_gender]))
		frnd_name = frnd_name.title()
		i = False
		if frnd_name: waiting = False
		else: output(57)
	output(78, addon=frnd_name)
	time.sleep(2)
	output(79)
	time.sleep(1)
	output(80, addon=player_name)
	time.sleep(2)
	if player_species == output(36, r=1): temp = output(30, r=1)
	else: temp = output(31, r=1)
	output(81, addon=[frnd_name, player_name, player_species,temp])
	time.sleep(2)
	output(82)
	time.sleep(1)
	if player_species == output(36, r=1): temp = output(84, r=1)
	elif player_species == output(34, r=1): temp = output(85, r=1)
	else:
		temp = output(86, r=1, addon=frnd_gender)
		if player_species == output(38, r=1): temp += output(87, r=1)
		elif player_species == output(32, r=1): temp += output(88, r=1)
		elif player_species == output(33, r=1): temp += output(89, r=1)
		elif player_species == output(35, r=1): temp += output(90, r=1)
		elif player_species == output(37, r=1): temp += output(91, r=1)
		elif player_species == output(39, r=1): temp += output(92, r=1)
	output(83, addon=temp)
	time.sleep(0.5)
	output(93)
	time.sleep(3)
	output(94, addon=frnd_name)
	time.sleep(1)
	output(95, addon=player_species)
	time.sleep(2)
	output(96)
	time.sleep(2)
	output(97)
	time.sleep(1)
	output(98, addon=[frnd_name, player_species, frnd_gndrpn])
	time.sleep(3)
	output(99)
	time.sleep(2)
	output(100, addon=frnd_name)
	time.sleep(1)
	output(101)
	time.sleep(5)
	output('')
	color('blue')
	output(102)
	color('reset')
	output('')
	time.sleep(2)
	loc = 'p1MainRoom'
	gameplay()

def gameplay():
	global loc, p1MainRoom, p1RoomTwo, devplayer, player, gender, frnd_gender, player_name, player_last, player_species, frnd_gndrpn, species, frnd_nane
	player = Character(loc, player_name, player_last, species, gender, 1)
	friend = Character(loc, frnd_nane, player_last, 'Fox', frnd_gender, 1)
	playing=True
	if not devplayer: quit(output(103, r=1))
	output(104)
	if loc == 'p1MainRoom':
		location = p1MainRoom
		location.describe()
	playing=True
	while playing:
		output("")
		cmnd = getCommand(getInput.text(output(105, r=1)))
		if not cmnd:
			output(106)
			continue
		if cmnd['verb'] == output(107, r=1): quit(output(109))
		elif cmnd['verb'] == output(110, r=1):
			save()
			continue
		elif cmnd['verb'] == output(112, r=1):
			load()
			continue
		elif cmnd['verb'] == output(113, r=1):
			output(108)
			output(111)
			output(114)
			output(116)
			output(118)
			output(120)
			output(123)
			continue
		noun = cmnd.get('noun')
		if not noun: continue
		else:
			item = location.findItem(noun)
			if cmnd['verb'] == output(115, r=1) and hasattr(item, 'examine'): item.examine()
			elif cmnd['verb'] == output(117, r=1) and hasattr(item, 'eat'): item.eat()
			elif cmnd['verb'] == output(119, r=1) and hasattr(item, 'drink'): item.drink()
			elif cmnd['verb'] == output(121, r=1) and hasattr(player, 'take'): player.take(item)
			elif not item:
				if cmnd['verb'] == output(122, r=1):
					roomname = location.go(noun)
					if not roomname: output(124)
					elif roomname == "locked": output(125)
					elif roomname == "invalid": output(126)
					else:
						location = rooms[roomname]
						location.describe()
				else: output(127, addon=noun)
			else: output(128)

def init():
	if pc == 'iphone':
		choice = getInput.choice(output('iosask', r=1), ['iPhone','iPad'])
		if choice == 1: pc = 'iPhone'
		elif choice == 2: pc = 'iPad'
		else: quit(output('iosquit', r=1), nosave=True)

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

init()