#Function that prints the messages
def output(msg, dict=True, newline=True, noscroll=False, addon=None, addonfromdict=False, modifier="normal", r=0):
	global scroll, styles, annoy, msgs
	#modifier = caps, title, lower, normal (when modifier isn't present)
	if msg == '': dict=False
	if dict: msg = msgs[msg]
	if addon:
		if type(addon) == type([]):
			i = 1
			for add in addon:
				addfromdict = addonfromdict[i-1]
				if addfromdict:
					add = msgs[add]
				re.sub('ADDON'+str(1),add,msg)
				i += 1
		else:
			if addon: re.sub('ADDON',addon,msg)
	if modifier == 'caps': msg = msg.upper()
	elif modifier == 'title': msg = msg.title()
	elif modifier == 'lower': msg = msg.lower()
	if r == 0:
		for c in msg:
			if annoy: color('random')
			sys.stdout.write(styles+c)
			if not noscroll:
				sys.stdout.flush()
				time.sleep(scroll)
		if newline: sys.stdout.write('\n')
		if noscroll: sys.stdout.flush()
		color('reset')
		sys.stdout.write(styles)
		sys.stdout.flush()
	elif r == 1: return msg