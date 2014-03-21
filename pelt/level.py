#PELT Level Information
#Created January 18, 2014 at 16:44

import time
import config
from errors import *
from item import *
from localio import output

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
		if line: temp.append(line)
	
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
			definersearch = re.match("%([^%]+)%([.]+)", line)
			code = definersearch.group(1)
			if code == 'Choice':
				"""this is complicated"""
			elif code == 'Action':
				DialogueAction(other)
			else:
				DialogueSpeech(thing, other)

class Level(object):
	def __init__(self, name, size, author=None, dialogue=None, rooms=[]):
		self.name = name
		self.size = size
		self.author = author
		self.dialogue = dialogue
		self.rooms = rooms
	
	@classmethod
	def fromText(cls, text):
		lines = preprocess(text)
		
		level = lines[0]
		
		#Check and parse level name and size
		#print('Parsing level metadata...')
		levelmeta = re.match('Level is "([^"]+)" sized (\d+)x(\d+) by "([^"]+)"', level)
		if not levelmeta: raise SyntaxError('Level name and size not on first line.  It was found as {%s}.' %level)
		name = levelmeta.group(1)
		strsize = levelmeta.group(2,3)
		author = levelmeta.group(4)
		size = (int(strsize[0]), int(strsize[1]))
		#print('Level metadata parsed.  Level is named %s, %s tiles high, and %s tiles wide, and author is %s' %(name, size[0], size[1], author))
		
		blocks = lines[1:]
		dialogue = getblocks('Dialogue is:', 'Finish Dialogue', blocks, 1)
		d = None #Dialogue.fromLines(dialogue)
		rooms = getblocks('Room is:', 'Finish Room', blocks, 0)
		r = []
		for room in rooms:
			rm = Room.fromText(room)
			r.append(rm)
		
		return cls(name, size, author, d, r)
	
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
		if r: x = self.name + '\n'
		else: output(self.name, dict=False)
		for i in self.items:
			if r: x += output('itemhere', addon=i, r=1)
			else: output('itemhere', addon=i)
			if not config.instmsg: time.sleep(0.1)
		for d in self.doors:
			if r: x += output('doorhere', addon=d.direction, r=1)
			else: output('doorhere', addon=d.direction)
			if not config.instmsg: time.sleep(0.1)
		if r == 1: return x

	def go(self, direction):
		for d in self.doors:
			if d.direction == direction:
				if not d.locked: return d.room
				else: return "locked"
		return None
