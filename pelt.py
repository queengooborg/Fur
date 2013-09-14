import time, os, pickle, sys, random, locale, re

try:
	import console, notification
	from scene import *
	pc = 'iphone'
	ios = True
except ImportError:
	import colorama, easygui #, menu, pygame
	colorama.init()
	#pygame.init()
	pc = 'computer'
	ios = False

def sync(vers, debugmode, title):
	global version, debug, gametitle
	version = vers
	debug = debugmode
	gametitle = title

#define the attributes of an item
class Item(object):

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

class BattleModifier(Item):
	def use(self, onPlayer):
		pass
		
class Potion(BattleModifier):
	def __init__(self, name, force, description):
		BattleModifier.__init__(self, name, description)
		self.force = force
	
	def use(self, onPlayer): onPlayer.life += self.force

class Tagger(BattleModifier):
	pass
	
class Thing(BattleModifier):
	def use(self, onPlayer): onPlayer.tags.append('blind')
	
	
class Spell(object):
	def __init__(self, name, description):
		self.name = name
		self.description = description
		
	def cast(self, source, target):
		pass

class BattleSpell(Spell, BattleModifier):
	pass


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
		else: choice = easygui.enterbox(msg=msg, title='PELT Engine - '+gametitle+' v'+str(version))
		return choice
	
	def choice(self, msg, choices, window=False):
		strings = [str(c) for c in choices]
		if ios and __name__ in '__main__':
			temp = strings[-1]
			if temp == output('quit', r=1) or temp == output('back', r=1) or temp == output('cancel', r=1): strings.remove(temp)
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
		if temp == output('quit', r=1) or temp == output('back', r=1) or temp == output('cancel', r=1): return 0
		return choices[number-1]

	def alert(self, msg):
			if ios and __name__ in '__main__':
				try: console.alert('',msg)
				except KeyboardInterrupt: pass
			else:
				easygui.msgbox(title='PELT Engine - '+gametitle+' v'+str(version), msg=msg)

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
				with open('options.pyp', 'wb') as handle: pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
				wait2=False
			elif choice == 0 or choice == 4: quit('', nosave=True)
			else: output("Invalid option/Opcion incorrecto/L'option invalide", dict=True)
		if lang == "English":
			with open('english.lang', 'rb') as handle: msgs = pickle.load(handle)
		else: output("Language File Version Incompatible/Version del Archivo del Idioma Incompatible/Version de L'archive du Language Incompatible", dict=True)

def setlang(lang):
	global msgs
	with open('english.lang', 'rb') as handle: msgs = pickle.load(handle)

#Function that prints the messages
def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0, s=0):
	global scroll, styles, annoy, msgs
	#modifier = caps, title, lower, normal (when modifier isn't present)
	try:
		if dict: msg = msgs[msg]
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
	time.sleep(s)

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

#define what a room is
class Room(object):
	def __init__(self, name, size, place, items, doors):
		self.name = name
		self.size = size
		self.place = place
		self.doors = doors
		self.items = items
	
	def __str__(self):
		return self.name
	
	@classmethod
	def fromText(cls, text):
		'''Room is:
			Called "Main Room" sized 17x10 placed A20x27
			Door to "Balcony" on Top 1 from Left
			Door to "Hallway" on Top 2 from Right locked with "Rusty Key"
			Door to "Play Room" on Bottom 4 from Right locked with "Silver Key"
			Trapdoor to "Chest Room" 1 from Left 2 from Bottom locked with "Fire Circle" (Hidden)
		Finish Room'''
		
		if type(text) == str: lines = text.split('\n')
		elif type(text) == list: lines = text
		else: lines = []
		meta = lines[0]
		
		xlines = ['Door to "Balcony" on Top 1 from Left',
		'Door to "Hallway" on Top 2 from Right locked with "Rusty Key"',
		'Door to "Play Room" on Bottom 4 from Right locked with "Silver Key"',
		'Trapdoor to "Chest Room" 1 from Left 2 from Bottom locked with "Fire Circle" (Hidden)']
		
		metasplit = re.search('Called "([^"]+)" sized (\d+)x(\d+) placed ([A-Z])(\d+)x(\d+)', meta)
		name = metasplit.group(1)
		size = metasplit.group(2,3)
		place = metasplit.group(4,5,6)
		size = (int(size[0]), int(size[1]))
		place = (place[0], int(place[1]), int(place[2]))
		lines = lines[1:]
		
		items = []
		doors = []
		
		for element in lines:
			if element[0:4] == "Door":
				match = re.search('Door to "([^"]+)" on ([a-zA-Z]+) (\d+) from ([a-zA-Z])', element)
				room = match.group(1)
				
				doors.append(element)
			
			elif element[0:8] == "Trapdoor":
				doors.append(element)
			
			elif element[0:5] == "Chest":
				items.append(element)
			
			print element
		
		return cls(name, size, place, items, doors)
	
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

#define the player and characters
class Character(object):
	def __init__(self, name, level, life, attk=25, dfns=25, attacks=[]):
		self.name = name
		self.level = level
		self.life = life
		self.attk = attk
		self.dfns = dfns
		self.tag = []
		self.type = 'Normal'
		self.attacks = [Attack(output('attack1', r=1), output('attack1desc', r=1), 20, 0, output('type1', r=1))]
		self.attacks += attacks
	
	def __str__(self):
		return self.name
	
	def take(self, item_name):
			item = self.location.getItem(item_name)
			self.inventory.append(item)
		
	def take_damage(self, dmg): self.life -= dmg
	
	def add_attack(self, attack):
		if type(attack) == Attack: pass
		else: output('attackerror')
	
	def rem_attack(): pass

class Ally(Character):
	def __init__(self, location, name, last, species, gender, level, life=100, attk=25, dfns=25):
		Character.__init__(self, name, level, life, attk, dfns)
		self.inventory = []
		self.location = location
		self.last = last
		self.species = species
		self.gender = gender
	
	def get_var(var):
		if var == 'all': return output('playerdesc', r=1, addon=[self.name, self.last, self.gender, self.species, self.inventory, self.location, self.level, self.attacks])
		else:
			try: return self.__getattribute__(var)
			except AttributeError: return None

class Enemy(Character):
	pass

class Attack(object):
	def __init__(self, name, desc, pwr, bonus, type):
		self.name = name
		self.desc = desc
		self.pwr = pwr
		self.bonus = bonus
		self.type = type
	
	def __repr__(self): return self.name
	
	def use(self, attacker, attacked):
		temp = 1.5 if self.type == attacked.type else 1
		#attack.bonus = 4, 2, 1, 5, 2.5, or 0
		damage = self.pwr
		attacked.take_damage(damage)
		print str(attacked)+' took '+str(damage)+' damage'

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

try:
	with open('options.pyp', 'rb') as handle:
		handle = pickle.load(handle)
		lang = handle[0]
		scrollspeed = handle[1]
		if scrollspeed == 'Fast': scroll = 0.01
		elif scrollspeed == 'Medium': scroll = 0.03
		elif scrollspeed == 'Slow': scroll = 0.05
		annoy = handle[2]
		devplayer = handle[3]
	if lang == "English": setlang('en')
except:
	scrollspeed='Medium'
	scroll=0.03
	lang=None
	annoy=False
	devplayer=True
	language()

styles = ''