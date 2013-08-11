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