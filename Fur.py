title = 'Fur'
author = 'Nightwave Studios'
#Text-based RPG by Kurai Atonitsuka, CEO of Nightwave Studios
#Created May 10, 2013 at 15:14

version=392
officialversion = str(version)+" Omega"
langversneeded = 0.1

#Dependencies:
#	For iPad:
#		Pythonista
#	For PC:
#		Colorama: https://pypi.python.org/pypi/colorama/
#		EasyGUI: http://easygui.sourceforge.net/
#		PyGame: http://www.pygame.org/

#Import PELT
from pelt import *
from pelt.i18n import m

#Initialize config variables (obsolete)
devmode = True
annoy = False
gui = True

import custio

sync(version, officialversion, langversneeded, devmode, title, author, modules=[localio])

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
	species[i] = m(temp)

try: console.clear()
except: pass
	#os.console('cls')
	#os.console('clear')

def quit(msg, nosave=False):
	global ios, devplayer
	if nosave: pass
	else: save()
	color('red')
	#if ios and not devplayer: notification.schedule(m('mailto2'), 15, 'Beep', m('mailto1'))
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
	global version, scrollspeed, scroll, loc, devplayer, annoy, pc, ios, msgs, player, friend
	if ios: temp = m('cancel')
	else: temp = m('ok')
	getInput.alert(m('broken1') %temp)
	#print available choices and wait for the user to pick a valid choice
	while True:
		newline()
		choices = [m('start'), m('custom'), m('options'), m('quit')]
		devchoices = ['Developer: Skip Dialogue']
		if devmode:
			for devchoice in devchoices: choices.append(devchoice)
		choice = getInput.choice(title, choices)#, window=True)
		newline()
		if choice==m('start'):
			wait_sta = True
			while wait_sta:
				choice_sta = getInput.choice(m('start'), [m('new'), m('load'), m('back')])
				if choice_sta == m('new'): start()
				elif choice_sta == m('load'):
					getInput.alert(m('broken3'))
					continue
					i = load()
					if i and devplayer: gameplay()
					elif not i: continue
					elif not devplayer: quit(m('broken4'), nosave=True)
				elif choice_sta == 0: wait_sta = False
				else: output('inputerror')
		elif choice=='Developer: Skip Dialogue':
			player = Ally(loc, player_name, player_last, species, gender, 1)
			friend = Ally(loc, frnd_nane, player_last, 'Fox', frnd_gender, 1)
			gameplay('part1')
		elif choice==m('custom'):
			custmenu()
		elif choice==m('options'):
			wait_opt = True
			while wait_opt:
				choice_opt = getInput.choice(m('title'), [m('scroll' %scrollspeed), m('annoy'), m('beta'), m('lang'), m('back')])
				if choice_opt == m('scroll' %scrollspeed):
					if scrollspeed == m('slow'):
						scrollspeed = m('med')
						scroll=0.03
					elif scrollspeed == m('med'):
						scrollspeed = m('fast')
						scroll=0.01
					else:
						scrollspeed = m('slow')
						scroll=0.05
				elif choice_opt == m('annoy'):
					getInput.alert(m('broken3'))
					continue
					if not annoy:
						getInput.alert(m('annoyon'))
						annoy = True
					else:
						getInput.alert(m('annoyoff'))
						annoy = False
				elif choice_opt==m('beta'):
					if not devplayer:
						getInput.alert(m('betaon'))
						devplayer = True
					else:
						getInput.alert(m('betaoff'))
						devplayer = False
				elif choice_opt == m('lang'): language()
				elif choice_opt == 0:
					with open('options.pyp', 'wb') as handle:
						pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
					wait_opt=False
				else: output('inputerror')
		elif choice==0: quit(m('quitmsg'), nosave=True)
		else: output('inputerror')

#Menu for custom levels
def custmenu():
	output('custtitle', s=3)
	#custio.connect()
	while True:
		choice = getInput.choice(m('custtitle'), [m('custstart'), m('custdown'), m('custup'), m('custcreate'), m('back')])
		if choice == m('custstart'): pass
		elif choice == m('custdown'): pass
		elif choice == m('custup'): pass
		elif choice == m('custcreate'): custio.custcreate()
		elif choice == 0: return False
		else: output('inputerror')

#When starting the game, program must ask if the player is a boy or girl.
def start():
	global gender, frnd_gender, player_name, player_last, player_species, frnd_gndrpn, species
	waiting=True
	while waiting:
		temp = getInput.choice(m('setupgndr'), [m('boy'), m('girl')])
		if temp == m('boy'):
			gender=output('boy', r=1, modifier="lower")
			frnd_gender=output('girl', r=1, modifier="lower")
			frnd_gndrpn=m('she')
		elif temp == m('girl'):
			gender=output('girl', r=1, modifier="lower")
			frnd_gender=output('boy', r=1, modifier="lower")
			frnd_gndrpn=m('he')
		else: quit(m('quitmsg'), nosave=True)
		waiting=False
	player_species = getInput.choice(m('setuprace'), species)
	if player_species == 1: quit(m('quitmsg'), nosave=True)
	waiting = True
	while waiting:
		temp = getInput.text(m('setupname'))
		temp = temp.title().split(' ')
		try:
			player_name = temp[0]
			player_last = temp[1]
			waiting = False
		except:
			if temp:
				temp = temp[0]
				while waiting:
					temp2 = getInput.text(m('setuplast') %temp)
					temp2 = temp2.title()
					if temp2:
						player_name = temp
						player_last = temp2
						waiting = False
					else: output('inputerror')
			else: output('inputerror')
	output('setupeyeclose', addon=(player_name, player_last), s=2)
	i = 0
	while i != 3:
		i += 1
		output(str(i)+"...", dict=False, newline=False)
		time.sleep(1)
	newline()
	output('setupeyeopen', addon=(player_species), s=4)
	newline()
	part1()

#part 1 init
def part1():
	global gender,player_name,player_last,frnd_gender,frnd_nane,frnd_last,devplayer,player,friend
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
	if frnd_gender == output('girl', r=1, modifier='lower'): temp2 = output('her', r=1)
	else: temp2 = output('him', r=1)
	output('p1m8', addon=(frnd_gender, temp, temp2, temp2), s=0.5)
	output('p1m9', s=0.5)
	output('p1m10', s=2)
	output('p1m11', newline=False, s=1)
	waiting = True
	while waiting:
		frnd_name=getInput.text(m('setup9') %(frnd_gndrpn, frnd_gender))
		if frnd_name == None or frnd_name == 0: quit(m('nofriendnameerror'))
		frnd_name = frnd_name.title()
		i = False
		if frnd_name: waiting = False
		else: m('nofriendnameerror') %(frnd_gndrpn, frnd_gender)
	player = Ally(loc, player_name, player_last, species, gender, 1)
	friend = Ally(loc, frnd_nane, player_last, 'Fox', frnd_gender, 1)
	output('p1m12', addon=frnd_name, s=2)
	output('p1m13', s=1)
	output('p1m14', addon=player_name, s=2)
	if player_species == output('fox', r=1): temp = m('meyou')
	else: temp = m('you')
	output('p1m15', addon=(frnd_name, player_name, player_species, temp), s=2)
	output('p1m16', s=1)
	if player_species == m('fox'): temp = m('foxdesc')
	elif player_species == m('dragon'): temp = m('dragondesc')
	else:
		temp = m('p1m18') %frnd_gender+'  '
		if player_species == m('wolf'): temp += m('wolfdesc')
		elif player_species == m('cat'): temp += m('catdesc')
		elif player_species == m('bird'): temp += m('birddesc')
		elif player_species == m('bear'): temp += m('beardesc')
		elif player_species == m('mouse'): temp += m('mousedesc')
		elif player_species == m('otter'): temp += m('otterdesc')
	output('p1m17', addon=temp, s=0.5)
	output('p1m19', s=3)
	output('p1m20', addon=frnd_name, s=1)
	output('p1m21', addon=player_species, s=2)
	output('p1m22', s=2)
	output('p1m23', s=1)
	output('p1m24', addon=(frnd_name, player_species, frnd_gndrpn), s=3)
	output('p1m25', s=2)
	output('p1m26', addon=frnd_name, s=1)
	output('p1m27', s=5)
	newline()
	output('helpquit')
	output('helpsave')
	output('helpload')
	output('helphelp')
	output('helpexamine')
	output('helpeat')
	output('helpdrink')
	output('helptake')
	output('helpgo')
	gameplay('part1')

def gameplay(map):
	global loc, devplayer, player, gender, friend, frnd_gender, player_name, player_last, player_species, frnd_gndrpn, species, frnd_nane, ios
	playing=True
	#quit(output('broken4', r=1))
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

def init(args = None):
	global ios, pc
	if ios:
		choice = getInput.choice(m('iosask'), ['iPhone','iPad'])
		if choice == 1: pc = 'iPhone'
		elif choice == 2: pc = 'iPad'
		else: quit(m('iosquit'), nosave=True)

	if not args:
		args = sys.argv[1:]
	if len(args) > 0:
		if "nostory" in args:
			loc = 'p1MainRoom'
			gameplay()
		elif "betatester" in args: config.devplayer = True
		elif "annoy" in args: config.annoy = True
		elif "nogui" in args: config.gui = False

	mainmenu()

if __name__ in "__main__":
	try: init()
	except SystemExit: pass