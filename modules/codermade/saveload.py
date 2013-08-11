#Save and load functions
def saveload(save):
	waiting = True
	while waiting:
		saves = range(10)
		saveslist = list[saves]
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
		choice = str_to_int(choice)
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
								overwrite = getInput.choice(output('savewarning', addon=[file[2], file[3], file[4]], r=1),[output('yes', r=1),output('no', r=1)])
								if overwrite == 1: return response
								elif overwrite == 2: overwait = False
								else: output('inputerror')
						else: return response
			except: return response
		else:
			output('saveerror')
			output('')

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
				loc = file[0]
				gender = file[1]
				player_name = file[2]
				player_last = file[3]
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