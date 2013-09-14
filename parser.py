import sys, re
from time import sleep
import easygui as eg
from pelt import *

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
		print('Parsing level metadata...')
		levelmeta = re.match('Level is "([^"]+)" sized (\d+)x(\d+)', level)
		if not levelmeta: raise SyntaxError('Level name and size not on first line.  It was found as {%s}.' %level)
		name = levelmeta.group(1)
		strsize = levelmeta.group(2,3)
		size = (int(strsize[0]), int(strsize[1]))
		print('Level metadata parsed.  Level is named %s, %s tiles high, and %s tiles wide' %(name, size[0], size[1]))
		
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

if __name__ == '__main__':
	with open('levels/part1.level','rb') as handle:
		level = handle.read()
		l = Level.fromText(level)
		raise EOFError('Parser incomplete')
