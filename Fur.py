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
	import pygame, colorama, easygui, menu
	colorama.init()
	pygame.init()
	pc = 'computer'
	ios = False

#from pelt import *
import time, os, pickle, sys, random, locale, re

#initialize variables
scrollspeed='Medium'
scroll=0.03
lang=None
annoy=False
devplayer=True
styles = ''
rooms={}

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
		with open('english.lang', 'rb') as handle2: msgs = pickle.load(handle2)
		pass
except: language()






#PELT engine
class Door(object):
	def __init__(self, direction, room, key=None):
		self.direction = direction
		self.room = room
		if key:
			self.locked = True
			self.key = key
		else: self.locked = False

	def __str__(self):
		return output('doordesc', r=1, addon=[self.direction,self.room])

#define the attributes of an item
class Item(object):
	name = None
	description = None

	def __init__(self, name, description=None):
		self.name = name
		self.description = description

	def examine(self):
		if self.description: output(self.description, dict=False)
		else: output('itemnormal', addon=self.name)

#define drink item
class Drink(Item):
	def __init__(self, name, description, poison):
		Item.__init__(self, name, description)
		self.poison = poison

	def drink(self):
		if self.poison:
			output('drinkpoisoned', addon=self.name)
			quit('drinkpoisonedmsg', addon=self.name)
		else: output('foodeaten', addon=self.name)

#define food item
class Food(Item):
	def __init__(self, name, description, poison):
		Item.__init__(self, name, description)
		self.poison = poison

	def eat(self):
		if self.poison:
			output('foodpoisoned', addon=self.name)
			quit('foodpoisonedmsg', addon=self.name)
		else: output('foodeaten', addon=self.name)

def getCommand(sentence):
	''' Read a command from the user and parse it.
	This parser understands some simple sentences:
		* just a verb: 'quit'
		* verb followed by a noun: 'eat sandwich'
		* verb noun 'with' noun: 'kill monster with sword'

	Return a dictionary of the parsed words, or None if the
	command couldn't be parsed.
	'''
	cmnd = {}
	words = sentence.lower().split()

	if len(words) == 0: return None

	cmnd['verb'] = words[0].lower()

	if len(words) > 1: cmnd['noun'] = words[1].lower()

	if len(words) > 2:
		if words[2] == output('with', r=1) or words[2] == output('using', r=1):
			if len(words) > 3: cmnd['using'] = words[3]
			else:
				output('usingerror', addon=[verb, noun])
				return None
		else: cmnd['extra'] = words[2:]
	return cmnd

class getinput():
	def __init__(self):
		self.network = False
		self.firstmsg = True
	
	def network(self):
		if ios:
			if self.network:
				console.hide_activity()
				self.network = False
			else:
				console.show_activity()
				self.network = True
		else: pass

	def text(self, msg):
		if ios and __name__ in '__main__': choice = console.input_alert(msg, '', '', 'Ok')
		else: choice = easygui.enterbox(msg=msg, title=output('title2', r=1, addon=str(version)))
		return choice
	
	def choice(self, msg, choices, window=False):
		if ios and __name__ in '__main__':
			temp = choices[-1]
			if temp == output('quit', r=1) or temp == output('back', r=1) or temp == output('cancel', r=1): choices.remove(temp)
			try:
				if len(choices) == 1: choice = console.alert(msg, '', choices[0])
				elif len(choices) == 2: choice = console.alert(msg, '', choices[0], choices[1])
				elif len(choices) == 3: choice = console.alert(msg, '', choices[0], choices[1], choices[2])
				else:
					waiting = True
					page = 1
					while waiting:
						try:
							b = 2
							choice = console.alert(msg, '', choices[0+(page-1)*2], choices[1+(page-1)*2], "Next Page")
						except IndexError: 
							b = 1
							try: 
								choice = console.alert(msg, '', choices[0+(page-1)*2], output('next', r=1))
							except IndexError:
								page = 0
								choice = 1+b
							except KeyboardInterrupt: return 0
						except KeyboardInterrupt: return 0
						if choice == 1+b:
							if page <= len(choices) // 2: page += 1
							else: page = 1
						else:
							return choice+(page-1)*2
				return choice
			except KeyboardInterrupt: return 0
		else:
			if not window:
				choice = easygui.buttonbox(msg=msg, title="Fur - Version "+str(version), choices=choices)
				i = 1
				for c in choices:
					if choice == c: return i
					else: i += 1
			else:
				choice = menu.main(choices)
				time.sleep(0.1)
				return choice

	def alert(self, msg):
			if ios and __name__ in '__main__':
				try: console.alert('',msg)
				except KeyboardInterrupt: pass
			else:
				easygui.msgbox(title="Fur - Version "+str(version), msg=msg)

getInput = getinput()

def language():
	global lang, msgs
	wait=True
	wait2=True
	while wait:
		while wait2:
			choice = getInput.choice('Language/Idioma', ['English','Espanol (Archivo del Idioma no Esta Presente)','Francais (Fichier de Langue pas present', 'Quit'])
			if choice == 1:
				lang = "English"
				with open('options', 'wb') as handle: pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
				wait2=False
			elif choice == 0 or choice == 4: quit('', nosave=True)
			else: output("Invalid option/Opcion incorrecto/L'option invalide", dict=True)
		if lang == "English":
			with open('english.lang', 'rb') as handle: msgs = pickle.load(handle)
		else: output("Language File Version Incompatible/Version del Archivo del Idioma Incompatible/Version de L'archive du Language Incompatible", dict=True)

#Function that prints the messages
def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0):
	global scroll, styles, annoy, msgs
	#modifier = caps, title, lower, normal (when modifier isn't present)
	try:
		if dict: msg = msgs[msg]
	except KeyError:
		if msg == '': pass
		else: msg = "WARNING: "+msg+" is not a valid keyword."
	if addon:
		if type(addon) == type([]):
			i = 1
			for add in addon:
				addfromdict = addonfromdict[i-1]
				if addfromdict:
					add = msgs[add]
				re.sub('ADDON'+str(1),add,msg)
				i += 1
		else:
			if addon: re.sub('ADDON',addon,msg)
	if modifier == 'caps': msg = msg.upper()
	elif modifier == 'title': msg = msg.title()
	elif modifier == 'lower': msg = msg.lower()
	if r == 0:
		for c in msg:
			if annoy: color('random')
			sys.stdout.write(styles+c)
			if not noscroll:
				sys.stdout.flush()
				time.sleep(scroll)
		if newline: sys.stdout.write('\n')
		if noscroll: sys.stdout.flush()
		color('reset')
		sys.stdout.write(styles)
		sys.stdout.flush()
	elif r == 1: return msg

#define what a room is
class Room(object):
	def __init__(self, name, items, doors):
		self.name = name
		rooms[name] = self
		self.doors = doors
		self.items = items

	def findItem(self, name):
		for i in self.items:
			if i.name == name: return i
		return None

	def describe(self):
		output(self.name)
		for i in self.items:
			output('itemhere', addon=i.name)
			time.sleep(0.1)
		for d in self.doors:
			output('doorhere', addon=d.direction)
			time.sleep(0.1)

	def go(self, direction):
		for d in self.doors:
			if d.direction == direction:
				if not d.locked: return d.room
				else: return "locked"
		return None

#Save and load functions
def saveload(save, overwarning, overaddon):
	waiting = True
	while waiting:
		saves = range(10)
		saveslist = list[saves]
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
		choice = str_to_int(choice)
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
								addon = [file[0], file[1]]
								for o in overaddon: addon.append(o)
								overwrite = getInput.choice(output(overwarning, addon=addon, r=1),[output('yes', r=1),output('no', r=1)])
								if overwrite == 1: return response
								elif overwrite == 2: overwait = False
								else: output('inputerror')
						else: return response
			except: return response
		else:
			output('saveerror')
			output('')

#converts a string to an integer and returns -1 if string is not a number
def str_to_int(text):
	try: response=int(text)
	except ValueError: return -1
	return response

#define an attack
class Attack(object):
	def __init__(self, name, desc, pwr, bonus, type):
		self.name = name
		self.desc = desc
		self.pwr = pwr
		self.bonus = bonus
		self.type = type
	
	def use(attacker, attacked):
		temp = 1.5 if self.type == attacked.type else 1
		#attack.bonus = 4, 2, 1, 5, 2.5, or 0
		damage = (((((((2*attacker.level/5+2)*attacker.attk*self.pwr)/50)+2)*temp)*self.bonus/10)*random.randint(217, 255))/255
		attacked.take_damage(damage)

#define the player and characters
class Character(object):
	def __init__(self, location, name, last, species, gender, level, life=100):
		self.inventory = []
		self.location = location
		self.name = name
		self.last = last
		self.species = species
		self.gender = gender
		self.level = level
		self.life = life
		self.attk = 25
		self.dfns = 25
		self.attacks = [Attack(output('attack1', r=1), output('attack1desc', r=1), 20, 0, output('type1', r=1))]

		def take(self, item_name):
			item = self.location.getItem(item_name)
			self.inventory.append(item)
		
		def take_damage(dmg): self.life -= dmg
		
		def get_var(var):
			if var == 'all': return output('playerdesc', r=1, addon=[self.name, self.last, self.gender, self.species, self.inventory, self.location, self.level, self.attacks])
			else:
				try: return self.__getattribute__(var)
				except AttributeError: return None
		
		def use_attack(): pass
		
		def add_attack(attack):
			if type(attack) == Attack: pass
			else: output('attackerror')
		
		def rem_attack(): pass

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



#PELT engine

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

def mainmenu():
	global version, scrollspeed, scroll, loc, devplayer, annoy, pc, ios, msgs
	#Print the title, author, and version
	color('reset')
	output('author')
	output('version', addon='r'+str(version))
	time.sleep(2)
	temp = scroll
	scroll = 0.2
	output('')
	output('title')
	scroll = temp
	time.sleep(3)
	if ios: temp = output('cancel', r=1)
	else: temp = output('ok', r=1)
	getInput.alert(output('broken1', r=1, addon=temp))
	#print available choices and wait for the user to pick a valid choice
	not_chosen=True
	wait_opt=True
	while not_chosen:
		output('')
		choice = getInput.choice(output('title', r=1),[output('start', r=1),output('load', r=1, addon='broken2', addonfromdict=True),output('options', r=1),output('quit', r=1)], window=True)
		output('')
		if choice==1: not_chosen=False
		elif choice==2:
			getInput.alert(output('broken3', r=1))
			continue
			i = load()
			if i and devplayer: gameplay()
			elif not i: continue
			elif not devplayer: quit(output('broken4', r=1), nosave=True)
		elif choice==3:
			wait_opt = True
			while wait_opt:
				choice_opt = getInput.choice(output('title', r=1),[output('scroll', r=1, addon=scrollspeed),output('annoy', r=1, addon='broken2', addonfromdict=False),output('beta', r=1),output('lang', r=1),output('back', r=1)])
				if choice_opt == 1:
					if scrollspeed==output('slow', r=1):
						scrollspeed=output('med', r=1)
						scroll=0.03
					elif scrollspeed==output('med', r=1):
						scrollspeed=output('fast', r=1)
						scroll=0.01
					else:
						scrollspeed=output('fast', r=1)
						scroll=0.05
				elif choice_opt==2:
					getInput.alert(output('broken3', r=1))
					continue
					if not annoy:
						getInput.alert(output('annoyon', r=1))
						annoy = True
					else:
						getInput.alert(output('annoyoff', r=1))
						annoy = False
				elif choice_opt==3:
					if not devplayer:
						getInput.alert(output('betaon', r=1))
						devplayer = True
					else:
						getInput.alert(output('betaoff', r=1))
						devplayer = False
				elif choice_opt == 4: language()
				elif choice_opt == 0 or choice_opt == 5:
					with open('options', 'wb') as handle:
						pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
					wait_opt=False
				else: output('invalidinput')
		elif choice==0 or choice==4: quit(output('quitmsg', r=1), nosave=True)
		else: output('invalidinput')

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
	global ios, pc
	if ios:
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