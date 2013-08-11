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

#define the attributes of an item
class Item(object):
	name = None
	description = None

	def __init__(self, name, description=None):
		self.name = name
		self.description = description

	def examine(self):
		if self.description: output(self.description, dict=False)
		else: output('itemnormal', addon=self.name)

#define food item
class Food(Item):
	def __init__(self, name, description, poison):
		Item.__init__(self, name, description)
		self.poison = poison

	def eat(self):
		if self.poison:
			output('foodpoisoned', addon=self.name)
			quit('foodpoisonedmsg', addon=self.name)
		else: output('foodeaten', addon=self.name)

#define drink item
class Drink(Item):
	def __init__(self, name, description, poison):
		Item.__init__(self, name, description)
		self.poison = poison

	def drink(self):
		if self.poison:
			output('drinkpoisoned', addon=self.name)
			quit('drinkpoisonedmsg', addon=self.name)
		else: output('foodeaten', addon=self.name)


#define the player and characters
class Character(object):
	def __init__(self, location, name, last, species, gender, level, life=100):
		self.inventory = []
		self.location = location
		self.name = name
		self.last = last
		self.species = species
		self.gender = gender
		self.level = level
		self.life = life
		self.attk = 25
		self.dfns = 25
		self.attacks = [Attack(output('attack1', r=1), output('attack1desc', r=1), 20, 0, output('type1', r=1))]

		def take(self, item_name):
			item = self.location.getItem(item_name)
			self.inventory.append(item)
		
		def take_damage(dmg): self.life -= dmg
		
		def get_var(var):
			if var == 'all': return output('playerdesc', r=1, addon=[self.name, self.last, self.gender, self.species, self.inventory, self.location, self.level, self.attacks])
			else:
				try: return self.__getattribute__(var)
				except AttributeError: return None
		
		def use_attack(): pass
		
		def add_attack(attack):
			if type(attack) == Attack: pass
			else: output('attackerror')
		
		def rem_attack(): pass

#define an attack
class Attack(object):
	def __init__(self, name, desc, pwr, bonus, type):
		self.name = name
		self.desc = desc
		self.pwr = pwr
		self.bonus = bonus
		self.type = type
	
	def use(attacker, attacked):
		temp = 1.5 if self.type == attacked.type else 1
		#attack.bonus = 4, 2, 1, 5, 2.5, or 0
		damage = (((((((2*attacker.level/5+2)*attacker.attk*self.pwr)/50)+2)*temp)*self.bonus/10)*random.randint(217, 255))/255
		attacked.take_damage(damage)

#define what a room is
rooms={}
class Room(object):
	def __init__(self, name, items, doors):
		self.name = name
		rooms[name] = self
		self.doors = doors
		self.items = items

	def findItem(self, name):
		for i in self.items:
			if i.name == name: return i
		return None

	def describe(self):
		output(self.name)
		for i in self.items:
			output('itemhere', addon=i.name)
			time.sleep(0.1)
		for d in self.doors:
			output('doorhere', addon=d.direction)
			time.sleep(0.1)

	def go(self, direction):
		for d in self.doors:
			if d.direction == direction:
				if not d.locked: return d.room
				else: return "locked"
		return None

class Door(object):
	def __init__(self, direction, room, key=None):
		self.direction = direction
		self.room = room
		if key:
			self.locked = True
			self.key = key
		else: self.locked = False

	def __str__(self):
		return output('doordesc', r=1, addon=[self.direction,self.room])