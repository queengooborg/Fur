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