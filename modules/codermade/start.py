#When starting the game, program must ask if the player is a boy or girl.
def start():
	global gender, frnd_gender, player_name, player_last, player_species, frnd_gndrpn, species
	waiting=True
	while waiting:
		temp = getInput.choice(output('setup1', r=1), [output('boy', r=1), output('girl', r=1)])
		'''Continue fixing language files here'''
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
		temp = temp.title().split()
		try:
			player_last = temp[1]
			player_name = temp[0]
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
	output('setup4', addon=[player_name, player_last])
	i = 0
	time.sleep(2)
	while i != 3:
		i += 1
		output(str(i))
		time.sleep(1)
	output('setup5')
	time.sleep(2)
	output('setup6')
	choice = getInput.choice(output('setup7', r=1), species)-1
	if choice == -1: quit(output('quitmsg', r=1), nosave=True)
	player_species = species[choice]
	output('setup8', addon=[player_species,player_species])
	time.sleep(4)