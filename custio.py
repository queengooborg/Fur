#Fur Custom Level Functions
#Created November 26, 2013 at 18:32

import socket

#socket.settimeout(30)

import urllib2
import easygui as eg
from pelt import str_to_int, localio
import pelt

def internet(page, timeout=10):
	pass #return urllib2.urlopen(page, timeout)

def poutput(msg, newline=True, noscroll=False):
	for c in msg:
		sys.stdout.write(c)
		if not noscroll:
			sys.stdout.flush()
			sleep(0.03)
	if newline: sys.stdout.write('\n')
	sys.stdout.flush()

domain = "http://kageashi.no-ip.biz/furcommunity/"

def connect():
	output('Connecting to KageASHI...')
	try: success = None #urllib2.urlopen(domain, None, 10)
	except:
		output('Sorry, cannot connect to KageASHI.  More details will be shown in a new window.')
		eg.exceptionbox()

def custcreate():
	#Level Metadata
	
	level = []
	
	op = ['Name','Height','Width']
	
	while True:
		metadata = localio.getInput.multtext("Enter the name and size (in tiles) of the level.", op)
		if metadata: break
	
	level.append("Level is "+metadata[op[0]]+" sized "+metadata[op[1]]+"x"+metadata[op[2]])
	
	#Dialogue
	
	dialexists = localio.getInput.choice("Would you like to add dialogue to the level?", ['Yes', 'No'])
	if dialexists == "Yes": dialexists = True
	else: dialexists = False
	
	dialogue = []
	
	if dialexists:
		options = ["Add Section", "Character Speech", "Action", "Choice", "Give Stat or Item", "Finish Dialogue"]
		output("Note: All dialogue before you add a section will run before the level loads.", dict=False)
		wait = True
		while wait:
			type = localio.getInput.choice("Dialogue Creation Interface", options)
			if type == options[0]:
				sectionname = localio.getInput.text("What is the name of the section?  (Leave blank to cancel)")
				if sectionname: dialogue.append("&"+sectionname)
			elif type == options[1]:
				op = ["Character", "Dialogue"]
				speech = localio.getInput.multtext("Speech (Use %Player%, %Friend1%, %Friend2%, etc. to get that character's name in the dialogue (ex. if Friend1 is named Vulpis, 'Hello %Friend1%' would say 'Hello Vulpis'))", op)
				if speech: dialogue.append("%"+speech[op[0]]+"% "+speech[op[1]])
			elif type == options[2]:
				action = localio.getInput.text("Action (Use %Player%, %Friend1%, %Friend2%, etc. to get that character's name in the dialogue (ex. if Friend1 is named Vulpis, 'Hello %Friend1%' would say 'Hello Vulpis'))")
				if action: dialogue.append("%Action% "+action)
			elif type == options[3]:
				choiceques = localio.getInput.text("Choice: What do you want to ask the player?")
				if choiceques: choicedial = ["%Choice% "+choiceques]
				else: choicedial = None
				if choicedial: output("Choice creation is not ready yet.", dict=False)
				# XXX create choice interface
			elif type == option[4]:
				op = ["Stat", "Item"]
				statitem = localio.getInput.choice("Give Stat or Item", op)
				if statitem == op[0]:
					opt = ["Name", "Player", "Amount (0 will remove stat)"]
					orgmsg = "Give Stat"
					msg = orgmsg
					waiting = True
					while waiting:
						stat = localio.getInput.multtext(msg, opt)
						if stat:
							msg = orgmsg
							amount = str_to_int(stat[opt[2]])
							if amount < 0: msg = "Amount is not a valid number.  "+msg
							else:
								dialogue.append("*Stat "+stat[opt[0]]+" "+stat[opt[1]]+" "+stat[opt[2]])
								waiting = False
						else: waiting = False
				elif statitem == op[1]:
					opt = ["Name", "Amount (any number above 0)"]
					orgmsg = "Give Item"
					msg = orgmsg
					waiting = True
					while waiting:
						item = localio.getInput.multtext(msg, opt)
						if item:
							msg = orgmsg
							invalid = -1000
							amount = str_to_int(stat[opt[2]], default=invalid)
							if amount != invalid: msg = "Amount is not a valid number.  "+msg
							else:
								dialogue.append("*Item "+item[opt[0]]+" "+stat[opt[1]])
								waiting = False
						else: waiting = False
			elif type == option[5]:
				waiting = False
			else: localio.output("inputerror")
	
	level.append("Dialogue is:")
	if dialogue != []:
		for dialogu in dialogue: level.append("\t"+dialogu)
	level.append("Finish Dialogue")
	
	
		
	# XXX continue with program

