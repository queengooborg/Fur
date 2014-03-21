#PELT Gameplay
#Created Febuary 27, 2014 at 13:57

import os
import config, level
from color import makeColor
from localio import output, getInput
from i18n import m

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

#Gameplay, text edition
def textplay(level):
	playing = True
	makeColor('blue')
	output(level.name, dict=False, s=2)
	makeColor('reset')
	output('gamestart')
	playing=True
	location = level.rooms[0]
	location.describe()
	while playing:
		output("")
		cmnd = getCommand(getInput.text('\n'+m('gameaction')))
		
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
			output('helpdescribe')
			output('helphelp')
			output('helpexamine')
			output('helpeat')
			output('helpdrink')
			output('helptake')
			output('helpgo')
			continue
		elif cmnd['verb'] == m('describecmd'):
			location.describe()
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

def gameplay(map):
	mapfile = os.path.join(config.mapdir, map+'.plf')
	with open(mapfile, 'rb') as mapdata: l = level.parselevel(mapdata)
	textplay(l)
