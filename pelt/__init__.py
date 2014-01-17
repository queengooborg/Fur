#PELT Engine
#Created September 12, 2013 at 17:17

peltvers = 122

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

from localio import output, newline, getInput, color
import config, level
from i18n import m, setlang

try:
	import console, notification
	from scene import *
	config.pc = 'iphone'
	config.ios = True
except ImportError:
	import colorama, easygui #, menu, pygame
	colorama.init()
	#pygame.init()
	config.pc = pcinfo()
	config.ios = False
ios = config.ios
pc = config.pc

def sync(vers, officialvers, langversneed, debugmode, title, auth, modules=[], args=[]):
	global version, officialversion, langversneeded, debug, gametitle, author, peltvers
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
		if self.open: output('chestdescopen', addon=', '.join(self.contents))
		else: output('chestdescclosed')
	
	def open(self, inventory):
		if self.locked:
			if self.key in inventory:
				self.locked = False
				output('chestunlocked', addon=self.key)
			else:
				output('chestlocked')
				return
		if self.copen: output('chestopenerror')
		else:
			self.copen = True
			output('chestopen', addon=', '.join(self.contents))
			for item in self.contents: inventory.append(item)
	
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
				setlang("en")
				wait2 = False
			elif choice == '': quit('', nosave=True)
			else: output("Invalid option/Opcion incorrecto/L'option invalide", dict=False)
		else: output("Language File Version Incompatible/Version del Archivo del Idioma Incompatible/Version de L'archive du Language Incompatible", dict=True)

#Gameplay for the game
def gameplay(map):
	global loc, devplayer, player, gender, friend, frnd_gender, player_name, player_last, player_species, frnd_gndrpn, species, frnd_nane, ios
	playing=True
	maploc = 'resources/levels/'+map+'.plf'
	with open(maploc, 'rb') as mapfile: level = parselevel(mapfile)
	color('blue')
	output(level.name, dict=False, s=2)
	color('reset')
	output('gamestart')
	playing=True
	location = level.rooms[0]
	while playing:
		output("")
		cmnd = getCommand(getInput.text(location.describe(r=True)+'\n'+m('gameaction')))

		# single-word commands
		if not cmnd or cmnd['verb'] == m('quitcmd'): quit(m('quitmsg'))
		elif cmnd['verb'] == m('savecmd'):
			save()
			continue
		elif cmnd['verb'] == m('loadcmd'):
			load()
			continue
		elif cmnd['verb'] == m('helpcmd'):
			output('helpquit')
			output('helpsave')
			output('helpload')
			output('helphelp')
			output('helpexamine')
			output('helpeat')
			output('helpdrink')
			output('helptake')
			output('helpgo')
			continue

		# two-word commands
		noun = cmnd.get('noun')
		if not noun: continue

		if cmnd['verb'] == m('gocmd'):
			roomname = location.go(noun)
			if not roomname: output('doormissing')
			elif roomname == "locked": output('doorlocked')
			elif roomname == "invalid": output('directionerror')
			elif roomname == "Finish": quit('broken4')
			else:
				i = 0
				for r in level.rooms:
					if r.name == roomname: break
					else: i += 1
				location = level.rooms[i]
		else:
			# commands that require an item
			item = location.findItem(noun)
			if not item:
				output('itemerror', addon=noun)
			elif cmnd['verb'] == m('examinecmd') and hasattr(item, 'examine'): item.examine()
			elif cmnd['verb'] == m('eatcmd') and hasattr(item, 'eat'): item.eat()
			elif cmnd['verb'] == m('drinkcmd') and hasattr(item, 'drink'): item.drink()
			elif cmnd['verb'] == m('takecmd') and hasattr(player, 'take'): player.take(item)
			elif cmnd['verb'] == m('opencmd') and hasattr(item, 'open'): item.open(player.inventory)
			else: output('cmderror')
