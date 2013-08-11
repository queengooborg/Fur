class getinput():
	def __init__(self):
		self.network = False
		self.firstmsg = True
	
	def network(self):
		if ios:
			if self.network:
				console.hide_activity()
				self.network = False
			else:
				console.show_activity()
				self.network = True
		else: pass

	def text(self, msg):
		if ios and __name__ in '__main__': choice = console.input_alert(msg, '', '', 'Ok')
		else: choice = easygui.enterbox(msg=msg, title=output('title2', r=1, addon=str(version)))
		return choice
	
	def choice(self, msg, choices, window=False):
		if ios and __name__ in '__main__':
			temp = choices[-1]
			if temp == output('quit', r=1) or temp == output('back', r=1) or temp == output('cancel', r=1): choices.remove(temp)
			try:
				if len(choices) == 1: choice = console.alert(msg, '', choices[0])
				elif len(choices) == 2: choice = console.alert(msg, '', choices[0], choices[1])
				elif len(choices) == 3: choice = console.alert(msg, '', choices[0], choices[1], choices[2])
				else:
					waiting = True
					page = 1
					while waiting:
						try:
							b = 2
							choice = console.alert(msg, '', choices[0+(page-1)*2], choices[1+(page-1)*2], "Next Page")
						except IndexError: 
							b = 1
							try: 
								choice = console.alert(msg, '', choices[0+(page-1)*2], output('next', r=1))
							except IndexError:
								page = 0
								choice = 1+b
							except KeyboardInterrupt: return 0
						except KeyboardInterrupt: return 0
						if choice == 1+b:
							if page <= len(choices) // 2: page += 1
							else: page = 1
						else:
							return choice+(page-1)*2
				return choice
			except KeyboardInterrupt: return 0
		else:
			if not window:
				choice = easygui.buttonbox(msg=msg, title="Fur - Version "+str(version), choices=choices)
				i = 1
				for c in choices:
					if choice == c: return i
					else: i += 1
			else:
				choice = menu.main(choices)
				time.sleep(0.1)
				return choice

	def alert(self, msg):
			if ios and __name__ in '__main__':
				try: console.alert('',msg)
				except KeyboardInterrupt: pass
			else:
				easygui.msgbox(title="Fur - Version "+str(version), msg=msg)

getInput = getinput()