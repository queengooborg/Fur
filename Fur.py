#Fur
#Text-based RPG by Dark Tailed
#Created May 10, 2013 at 15:14 
#Last edited August 27, 2013 at 13:38
version=311
langversneeded=0.1
#Dependencies:
	#For iPad:
	#	Pythonista
	#For PC:
	#	Colorama: https://pypi.python.org/pypi/colorama/
	#	EasyGUI: http://easygui.sourceforge.net/
	#	PyGame: http://www.pygame.org/

from pelt import *
givevers(version, True)

#initialize variables
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
		choice = getInput.choice(output('title', r=1),[output('start', r=1),output('load', r=1),output('options', r=1),output('quit', r=1)])#, window=True)
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
				choice_opt = getInput.choice(output('title', r=1),[output('scroll', r=1, addon=scrollspeed),output('annoy', r=1),output('beta', r=1),output('lang', r=1),output('back', r=1)])
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
		temp = temp.title().split(' ')
		try:
			player_name = temp[0]
			player_last = temp[1]
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
	output('setup4', addon=(player_name, player_last))
	i = 0
	time.sleep(2)
	while i != 3:
		i += 1
		output(str(i), dict=False)
		time.sleep(1)
	output('setup5')
	time.sleep(2)
	output('setup6')
	choice = getInput.choice(output('setup7', r=1), species)-1
	if choice == -1: quit(output('quitmsg', r=1), nosave=True)
	player_species = species[choice]
	output('setup8', addon=(player_species,player_species))
	time.sleep(4)

#part 1 init
def part1():
	global loc,gender,player_name,player_last,frnd_gender,frnd_nane,frnd_last,devplayer
	playing = True
	output('p1m1', s=2)
	output('p1m2', s=2)
	output('p1m3', s=3)
	output('p1m4', addon=player_species, s=2)
	output('p1m5', s=2)
	output('p1m6', addon=(frnd_gender, frnd_gender), s=4)
	output('p1m7', s=3)
	if frnd_gndrpn == output('he', r=1): temp = output('he', r=1, modifier='title')
	else: temp = output('she', r=1, modifier='title')
	if frnd_gender == output('girl', r=1): temp2 = output('her', r=1)
	else: temp2 = output('his', r=1)
	output('p1m8', addon=(frnd_gender, temp, temp2, temp2), s=0.5)
	output('p1m9', s=0.5)
	output('p1m10', s=2)
	output('p1m11', newline=False, s=1)
	waiting = True
	title = output('setup9', r=1, addon=(frnd_gndrpn, frnd_gender))
	while waiting:
		frnd_name=getInput.text()
		frnd_name = frnd_name.title()
		i = False
		if frnd_name: waiting = False
		else: output('nofriendnameerror', r=1, addon=(frnd_gndrpn, frnd_gender))
	output('p1m12', addon=frnd_name, s=2)
	output('p1m13', s=1)
	output('p1m14', addon=player_name, s=2)
	if player_species == output('fox', r=1): temp = output('meyou', r=1)
	else: temp = output('you', r=1)
	output('p1m15', addon=(frnd_name, player_name, player_species, temp), s=2)
	output('p1m16', s=1)
	if player_species == output('fox', r=1): temp = output('foxdesc', r=1)
	elif player_species == output('dragon', r=1): temp = output('dragondesc', r=1)
	else:
		temp = output('p1m18', r=1, addon=frnd_gender)
		if player_species == output('wolf', r=1): temp += output('wolfdesc', r=1)
		elif player_species == output('cat', r=1): temp += output('catdesc', r=1)
		elif player_species == output('bird', r=1): temp += output('birddesc', r=1)
		elif player_species == output('bear', r=1): temp += output('beardesc', r=1)
		elif player_species == output('mouse', r=1): temp += output('mousedesc', r=1)
		elif player_species == output('otter', r=1): temp += output('otterdesc', r=1)
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

try: init()
except: easygui.exceptionbox()