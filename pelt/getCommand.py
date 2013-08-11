def getCommand(sentence):
	''' Read a command from the user and parse it.
	This parser understands some simple sentences:
		* just a verb: 'quit'
		* verb followed by a noun: 'eat sandwich'
		* verb noun 'with' noun: 'kill monster with sword'

	Return a dictionary of the parsed words, or None if the
	command couldn't be parsed.
	'''
	cmnd = {}
	words = sentence.lower().split()

	if len(words) == 0: return None

	cmnd['verb'] = words[0].lower()

	if len(words) > 1: cmnd['noun'] = words[1].lower()

	if len(words) > 2:
		if words[2] == output('with', r=1) or words[2] == output('using', r=1):
			if len(words) > 3: cmnd['using'] = words[3]
			else:
				output('usingerror', addon=[verb, noun])
				return None
		else: cmnd['extra'] = words[2:]
	return cmnd