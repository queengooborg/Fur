import sys, re
from time import sleep
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
			if max and len(blocks) >= max: return blocks
		i += 1
	return blocks
	
class DialogueSpeech(object):
	def __init__(self, speaker, text):
		self.speaker = speaker
		self.text = text
	
	def __str__(self):
		return self.speaker+": "+self.text

class Dialogue(object):
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

def getdialogue(data):
	response = getblocks('Dialogue is:', 'End Dialogue', data, 1)
	'''
		%Player% {Player's Dialogue}
		%Friend1% {Friend1's Dialogue}
		%Action% {The Action, remember you can put %Player% and %Friend1% in the action}
		%Choice% {Question}
			${Choice 1}$ {Action or Dialogue} $
			${Choice 2}$ {Action or Dialogue} $
		%End Choice%
	'''
	
def preprocess(data):
	#To begin, remove comments
	output('Removing comments...')
	data = re.sub('\[.*?\]','',data)
	output('Comments removed')
	sleep(0.2)

	#Then, remove all blank lines
	output('Removing blank lines...')
	data = data.split('\n')
	temp = []
	for line in data:
		if line:
			temp.append(line)
	data = temp
	output('Blank lines removed')
	sleep(0.2)
	
	# XXX Finally, collapse all whitespace
	return data

def parserooms(data):
	rooms = getblocks('Room called "([\w\s]+)" sized (\d+)x(\d+) placed \w(\d+)x(\d+)', 'Finish Room', data, 0)
	for room in rooms:
		pass

def parselevel(level):
	output('PELT Level Parser, starting...')
	
	#preprocess level
	data = preprocess(level.read())
	
	#Check and parse level name and size
	output('Parsing level metadata...')
	line1 = re.match('Level is "([\w\s]+)" sized (\d+)x(\d+)', data[0])
	if not line1: raise SyntaxError('Level name and size not on first line.')
	levelname = line1.group(1)
	levelsize = line1.group(2,3)
	output('Level metadata parsed.  Level is named %s, %s tiles high, and %s tiles wide' %(levelname, levelsize[0], levelsize[1]))
	
	#Check and parse dialogue
	output('Parsing dialogue...')
	dialogue = getdialogue(data)
	sleep(0.2)
	output('Dialogue parsed (Note: Dialogue parsing is currently unmade)')
	
	#Parse rooms
	output('Parsing rooms...')
	parserooms(data)
	sleep(0.2)
	output('Rooms parsed (Note: Room parsing is currently unmade)')

if __name__ == '__main__':
	with open('demo.level','rb') as handle:
		parselevel(handle)
		raise EOFError('Parser incomplete')
