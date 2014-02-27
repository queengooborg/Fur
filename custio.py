#Fur Custom Level Functions
#Created November 26, 2013 at 18:32

#socket.settimeout(30)

import webbrowser, urllib2, sys, json
from pelt import localio

def output(msg, *args, **kwargs):
	print msg

def connect(url='', browser=False):
	try:
		if browser:
			webbrowser.open(site+url)
			localio.getInput.alert('Click Ok/Cancel...')
		else:
			return urllib2.urlopen(site+url, None, 10).read()
	except (urllib2.URLError, urllib2.HTTPError) as error:
		output('Sorry, cannot connect to KageASHI.')
		print error
		return None

def poutput(msg, newline=True, noscroll=False):
	for c in msg:
		sys.stdout.write(c)
		if not noscroll:
			sys.stdout.flush()
			sleep(0.03)
	if newline:
		sys.stdout.write('\n')
	sys.stdout.flush()

domain = "kageashi.no-ip.biz"
#domain = "192.168.1.4"
site = "http://"+domain+"/furcommunity/"

def levellist():
	levelraw = connect('levels/popular')
	levels = json.loads(str(levelraw))
	print "There are", len(levels), 'levels'
	for level in levels:
		print level

def custcreate():
	#Level Metadata
	
	level = []
	
	op = ['Name','Height','Width']
	
	while True:
		metadata = localio.getInput.multtext("Enter the name and size (in tiles) of the level.", op)
		if metadata:
			break
	
	level.append("Level is "+metadata[op[0]]+" sized "+metadata[op[1]]+"x"+metadata[op[2]])
	
	#Dialogue
	
	dialexists = localio.getInput.choice("Would you like to add dialogue to the level?", ['Yes', 'No'])
	if dialexists == "Yes":
		dialexists = True
	else:
		dialexists = False
	
	dialogue = []
	
	if dialexists:
		options = ["Add Section", "Character Speech", "Action", "Choice", "Give Stat or Item", "Finish Dialogue"]
		output("Note: All dialogue before you add a section will run before the level loads.", dict=False)
		wait = True
		while wait:
			type = localio.getInput.choice("Dialogue Creation Interface", options)
			if type == options[0]:
				sectionname = localio.getInput.text("What is the name of the section?  (Leave blank to cancel)")
				if sectionname:
					dialogue.append("&"+sectionname)
			elif type == options[1]:
				op = ["Character", "Dialogue"]
				speech = localio.getInput.multtext("Speech (Use %Player%, %Friend1%, %Friend2%, etc. to get that character's name in the dialogue (ex. if Friend1 is named Vulpis, 'Hello %Friend1%' would say 'Hello Vulpis'))", op)
				if speech:
					dialogue.append("%"+speech[op[0]]+"% "+speech[op[1]])
			elif type == options[2]:
				action = localio.getInput.text("Action (Use %Player%, %Friend1%, %Friend2%, etc. to get that character's name in the dialogue (ex. if Friend1 is named Vulpis, 'Hello %Friend1%' would say 'Hello Vulpis'))")
				if action:
					dialogue.append("%Action% "+action)
			elif type == options[3]:
				choiceques = localio.getInput.text("Choice: What do you want to ask the player?")
				if choiceques:
					choicedial = ["%Choice% "+choiceques]
				else:
					choicedial = None
				if choicedial:
					output("Choice creation is not ready yet.", dict=False)
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
							if amount < 0:
								msg = "Amount is not a valid number.  "+msg
							else:
								dialogue.append("*Stat "+stat[opt[0]]+" "+stat[opt[1]]+" "+stat[opt[2]])
								waiting = False
						else:
							waiting = False
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
							if amount != invalid:
								msg = "Amount is not a valid number.  "+msg
							else:
								dialogue.append("*Item "+item[opt[0]]+" "+stat[opt[1]])
								waiting = False
						else:
							waiting = False
			elif type == option[5]:
				waiting = False
			else:
				localio.output("inputerror")
	
	level.append("Dialogue is:")
	if dialogue != []:
		for dialogu in dialogue: level.append("\t"+dialogu)
	level.append("Finish Dialogue")
	
	# XXX add enemies
	
	roomexists = False
	wait = True
	roomdata = []
	while wait:
		waiting = True
		msg = "Add a New Room"
		while waiting:
			op = ["Room Name", "Height", "Width", "Floor Letter" "X Placement", "Y Placement"]
			me = localio.getInput.multtext(msg, op)
			msg = "Add a New Room"
			if metadata:
				h = str_to_int(me['Height'])
				w = str_to_int(me['Width'])
				x = str_to_int(me['X Placement'])
				y = str_to_int(me['Y Placement'])
				if -1 not in [h, w, x, y] and len(me["Floor Letter"]) < 1:
					roomdata.append("Called "+me['Room Name']+" sized "+me['Height']+"x"+me['Width']+" placed "+me['Floor Letter']+me['X Placement']+"x"+me['Y Placement'])
					wait = False
				else:
					msg = "Invalid input.  "+msg
			else:
				if roomexists:
					wait = False
				else:
					msg = "You need to add at least one room.  "+msg
		
		waitin = True
		while waitin:
			opt = ["Create Door", "Create Trapdoor", "Create Chest", "Finish Room"]
			choice = localio.getInput.choice("Add Elements to "+me['Room Name'], opt)
			if choice == opt[0]:
				data = localio.getInput.multtext(opt[0], ["To Room", "On Wall", "Blocks From Wall", "From Wall"], ["Locked With Key", "Properties"])
				placement = str_to_int(data['Blocks From Wall'])
				if not placement == -1:
					door = "Door to "+data['To Room']+" on "+data['On Wall']+" "+data['Blocks From Wall']+" from "+data['From Wall']
					if data['Locked With Key']:
						door += " locked with "+data['Locked With Key']
						if data['Properties']:
							door += " ("+data['Properties']+")"
				else:
					print "Blocks From Wall is an invalid choice"
			elif choice == opt[1]:
				data = localio.getInput.multtext(opt[0], ["To Room", "From First Wall", "Blocks From First Wall", "From Second Wall", "Blocks From Second Wall"], ["Locked With Key", "Properties"])
				placemen1 = str_to_int(data['Blocks From First Wall'])
				placemen2 = str_to_int(data['Blocks From Second Wall'])
				if not placemen1 == -1 or placemen2 == -1:
					door = "Door to "+data['To Room']+" on "+data['Blocks From First Wall']+" from "+data['On First Wall']+" and "+data['Blocks From Second Wall']+" from "+data['From Second Wall']
					if data['Locked With Key']:
						door += " locked with "+data['Locked With Key']
						if data['Properties']:
							door += " ("+data['Properties']+")"
				else:
					print "Blocks From Wall is an invalid choice"
			elif choice == opt[2]:
				data = localio.getInput.choice("Create Chest", ["X Placement", "Y Placement", "Items"])
		
		"""Room is:
	Called {Room Name} sized {Height}x{Width} placed {X Coord}x{Y Coord}
    <To make a Door or Trapdoor> {Door/Trapdoor} to {Room} <Optional> locked with {Key Name} <Optional> ({Properties}) </Optional> </Optional> <If Door> on {Left/Right/Top/Bottom} {Pixels} from {Left/Right/Top/Bottom} </If Door> </To make a Door or Trapdoor>
    <To make a Chest> Chest placed {X Coord in Room}x{Y Coord in Room} with ({Item 1}, {Item 2}, {Etc.}) </To make a Chest>
Finish Room
]"""
		
	# XXX continue with program

