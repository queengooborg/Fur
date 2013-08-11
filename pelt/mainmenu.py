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
		choice = getInput.choice(output('title', r=1),[output('start', r=1),output('load', r=1, addon='broken2', addonfromdict=True),output('options', r=1),output('quit', r=1)], window=True)
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
				choice_opt = getInput.choice(output('title', r=1),[output('scroll', r=1, addon=scrollspeed),output('annoy', r=1, addon='broken2', addonfromdict=False),output('beta', r=1),output('lang', r=1),output('back', r=1)])
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