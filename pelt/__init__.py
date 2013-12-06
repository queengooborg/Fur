# -*- coding: utf-8 -*-

#PELT Engine
#Created September 12, 2013 at 17:17

peltvers = 87

import time, os, pickle, sys, random, locale, re, argparse
from localio import output, newline, getInput, color

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

def sync(vers, officialvers, langversneed, debugmode, title, auth, modules=[], args={}):
	global version, officialversion, langversneeded, debug, gametitle, author, peltvers
	version = vers
	officialversion = officialvers
	langversneeded = langversneed
	debug = debugmode
	gametitle = title
	author = auth
	#from localio import output, newline, getInput, color
	#Print the title, author, and version
	color('reset')
	output('author', addon=author)
	output('version', addon=(officialversion, peltvers), s=2)
	newline()
	output('title', addon=gametitle, s=3)

#define the attributes of an item
class Item(object):
	def __init__(self, name, description=None):
		self.name = name
		self.description = description

	def examine(self):
		if self.description: output(self.description, dict=False)
		else: output('itemnormal', addon=self.name)

#Errors
class ParseError(ValueError):
	pass
	
class NoFacingError(ParseError):
	pass
#/Errors

class Chest(Item):
	placedRE = re.compile("placed (\d+) from ([a-zA-Z]+) (\d+) from ([a-zA-Z]+)")

	def __init__(self, contents=[], key=None):
		self.contents = contents
		self.copen = False
		if not key: self.locked = False
		else:
			self.locked = True
			self.key = key
		Item.__init__(self, "chest")
	
	def __str__(self):
		return 'chest'
	
	@classmethod
	def fromText(cls, text):
		
		placedMatch = cls.placedRE.search(text)
		if placedMatch:
			# assign to variables
			pass
		
		# XXX add a block like the above (and compiled RE's in the class) for each phrase, then delete from below
		phrases = {
			'placed':  "placed (\d+) from ([a-zA-Z]+) (\d+) from ([a-zA-Z]+)",
			'facing': 'facing ([a-zA-Z]+)',
			'with': '\(([^\)]+)\)',
		}
		
		#for name, regex in phrases.items():
		#	if not match:
		#		pass#raise ParseError('Missing %s phrase in "%s"' %(name, text))
		
		"""Chest placed 1 from Left 1 from Top facing Bottom with (Rusty Key, $50)"""
		match = re.search('Chest placed (\d+) from ([a-zA-Z]+) (\d+) from ([a-zA-Z]+) facing ([a-zA-Z]+) with \(([^\)]+)\)', text)
		if match == None:
			noFacingMatch = re.search('Chest placed (\d+) from ([a-zA-Z]+) (\d+) from ([a-zA-Z]+) with \(([^\)]+)\)', text)
			if noFacingMatch == None:
				raise ParseError('Invalid syntax for "%s".  There is nothing else we know.' %text)
			else: raise NoFacingError('Tried to parse "%s", however I don\'t know which way that chest is facing.' %text)
		
		placed = match.group(1, 2, 3, 4, 5)
		itemsraw = match.group(6)
	
		itemsraw = itemsraw.split(', ')
		#for item in itemsraw: items.append(item)
		keymatch = re.search('locked with "([a-zA-Z]+)"', text)
		if keymatch != None: key = keymatch.group(1)
		else: key = None
		
		return cls(itemsraw, key)

	def examine(self):
		if self.open: output('chestdescopen', addon=self.contents.join(', '))
		else: output('chestdescclosed')
	
	def open(self, inventory):
		if self.locked:
			for item in inventory:
				if item.name == self.key:
					self.locked = False
					output('chestunlocked', addon=self.key)
					continue
			if self.locked:
				output('chestlocked')
				return
		if self.copen: output('chestopenerror')
		else:
			self.copen = True
			output('chestopen', addon=self.contents.join(', '))
	
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
	if sentence == None: return None
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

#PARSER
def getblocks(start, end, data, max):
	i = 0
	blocks = []
	blockopen = False
	for line in data:
		if line == start:
			istart = i
			if blockopen: raise SyntaxError('New block started before previous block closed')
			blockopen = True
		if line == end:
			iend = i
			if not blockopen: raise SyntaxError('A block was closed before it began')
			blockopen = False
			blocks.append(data[istart+1:iend])
			if max != 0 and len(blocks) >= max: return blocks
		i += 1
	return blocks

def preprocess(data):
	#To begin, remove comments
	nocommentdata = ''
	comment=False
	for c in data:
		if c == '[':
			comment=True
		elif c == ']':
			comment=False
		elif not comment:
			nocommentdata += c
	
	#Then, collapse all whitespace
	clean1data = re.sub('\n[ \t]+','\n',nocommentdata)
	cleandata = re.sub('\r','',clean1data)

	#Finally, remove all blank lines
	listdata = cleandata.split('\n')
	temp = []
	for line in listdata:
		if line:
			temp.append(line)
	
	return temp

def parselevel(leveldata):
	level = leveldata.read()
	l = Level.fromText(level)
	return l

class DialogueSpeech(object):
	def __init__(self, speaker, text):
		self.speaker = speaker
		self.text = text
	
	def __str__(self):
		return self.speaker+": "+self.text

class Dialogue(object):
	#response = getblocks('Dialogue is:', 'End Dialogue', data, 1)
	'''
		%Player% {Player's Dialogue}
		%Friend1% {Friend1's Dialogue}
		%Action% {The Action, remember you can put %Player% and %Friend1% in the action}
		%Choice% {Question}
			${Choice 1}$ {Action or Dialogue} $
			${Choice 2}$ {Action or Dialogue} $
		%End Choice%
	'''

	def __init__(self, dialogue):
		self.raw = dialogue
		for line in self.raw:
			# XXX get what's between the % symbols
			if thing == 'Choice':
				"""this is complicated"""
			elif thing == 'Action':
				DialogueAction(other)
			else:
				DialogueSpeech(thing, other)

class Level(object):
	def __init__(self, name, size, dialogue=None, rooms=[]):
		self.name = name
		self.size = size
		self.dialogue = dialogue
		self.rooms = rooms
	
	@classmethod
	def fromText(cls, text):
		lines = preprocess(text)
		
		level = lines[0]
		
		#Check and parse level name and size
		#print('Parsing level metadata...')
		levelmeta = re.match('Level is "([^"]+)" sized (\d+)x(\d+)', level)
		if not levelmeta: raise SyntaxError('Level name and size not on first line.  It was found as {%s}.' %level)
		name = levelmeta.group(1)
		strsize = levelmeta.group(2,3)
		size = (int(strsize[0]), int(strsize[1]))
		#print('Level metadata parsed.  Level is named %s, %s tiles high, and %s tiles wide' %(name, size[0], size[1]))
		
		blocks = lines[1:]
		dialogue = getblocks('Dialogue is:', 'Finish Dialogue', blocks, 1)
		d = None #Dialogue.fromLines(dialogue)
		rooms = getblocks('Room is:', 'Finish Room', blocks, 0)
		r = []
		for room in rooms:
			rm = Room.fromText(room)
			r.append(rm)
		
		return cls(name, size, d, r)
	
	def addRoom(self, room):
		self.rooms.append(room)

class Door(object):
	def __init__(self, placed, room, key=None, trapdoor=False):
		self.trapdoor = trapdoor
		if self.trapdoor: self.placed = {'dist1': placed[0], 'onwall': placed[1], 'distance': placed[2], 'fromwall': placed[3]}
		else: self.placed = {'onwall': placed[0], 'distance': placed[1], 'fromwall': placed[2]}
		self.room = room
		if key:
			self.locked = True
			self.key = key
		else: self.locked = False
		for i in [self.placed['onwall'], self.placed['fromwall']]:
			if i == 'Top': h1 = 'north'
			elif i == 'Bottom': h1 = 'south'
			elif i == 'Left': h2 = 'west'
			elif i == 'Right': h2 = 'east'
		self.direction = h1+h2

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
			#Door
			if element[0:4] == "Door":
				"""Door to "Play Room" on Bottom 4 from Right locked with "Silver Key"""
				match = re.search('Door to "([^"]+)" on ([a-zA-Z]+) (\d+) from ([a-zA-Z]+)', element)
				if match != None:
					room = match.group(1)
					placed = match.group(2, 3, 4)
					keymatch = re.search('locked with "([a-zA-Z]+)"', element)
					if keymatch: key = keymatch.group(1)
					else: key = None
					door = Door(placed, room, key)
					
					doors.append(door)
			
			#Trapdoor (same mechanic as door)
			elif element[0:8] == "Trapdoor":
				"""Trapdoor to "Chest Room" 1 from Left 2 from Bottom locked with "Fire Circle" (Hidden)"""
				match = re.search('Trapdoor to "([^"]+)" (\d+) from ([a-zA-Z]+) (\d+) from ([a-zA-Z]+)', element)
				if match != None:
					room = match.group(1)
					placed = match.group(2, 3, 4, 5)
					keymatch = re.search('locked with "([a-zA-Z]+)"', element)
					if keymatch != None: key = keymatch.group(1)
					else: key = None
					door = Door(placed, room, key, trapdoor=True)
					
					doors.append(door)
			
			elif element[0:5] == "Chest": items.append(Chest.fromText(element))
			
			#elif element[0:5] == 'Enemy':
			#	"""Enemy 2 from Top 0 from Left Type 1"""
			#	match = re.search('Enemy (\d+) from ([a-zA-Z]+) (\d+) from ([a-zA-Z]+) Type (\d+)', element)
			#	if match != None:
			#		placed = match.group(1, 2, 3, 4)
			#		etype = match.group(5)
			#		pass
		
		return cls(name, size, place, items, doors)
	
	def findItem(self, name):
		for i in self.items:
			if i.name == name: return i
		return None

	def describe(self, r=False):
		if r: x = output(self.name, dict=False, r=1) + '\n'
		else: output(self.name, dict=False)
		for i in self.items:
			if r: x += output('itemhere', addon=i, r=1)
			else: output('itemhere', addon=i)
			time.sleep(0.1)
			if r: x += '\n'
		for d in self.doors:
			if r: x += output('doorhere', addon=d.direction, r=1)
			else: output('doorhere', addon=d.direction)
			time.sleep(0.1)
			if r: x += '\n'
		if r == 1: return x

	def go(self, direction):
		for d in self.doors:
			if d.direction == direction:
				if not d.locked: return d.room
				else: return "locked"
		return None
#PARSER

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

#converts a string to an integer and returns -1 if string is not a number
def str_to_int(text, default=-1):
	try: response = int(text)
	except ValueError: return default
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
		dice = random.randint(0,10)
		if dice <= 1: crit = 0.5
		elif dice >= 10: crit = 1.5
		else: crit = 1
		damage = ((((((self.pwr + attacker.attk)*2)*temp)-(attacked.dfns/1.1))/3)*crit)+(random.randint(0,20)-10)
		damage = int(damage)
		attacked.take_damage(damage)
		print(str(attacked)+' took '+str(damage)+' damage')
		crit += 5
		if crit == 0.5: print('The attack was not very effective.')
		elif crit == 1.5: print('The attack landed a critical hit!')

def language():
	wait=True
	wait2=True
	while wait:
		while wait2:
			choice = getInput.choice('Language/Idioma', ['English','Espanol (Archivo del Idioma no Esta Presente)','Francais (Fichier de Langue pas present)', 'Quit'])
			if choice == 'English':
				i18n.setlang("en")
				wait2 = False
			elif choice == '': quit('', nosave=True)
			else: output("Invalid option/Opcion incorrecto/L'option invalide", dict=False)
		else: output("Language File Version Incompatible/Version del Archivo del Idioma Incompatible/Version de L'archive du Language Incompatible", dict=True)

