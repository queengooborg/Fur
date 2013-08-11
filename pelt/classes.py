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