# Attack
# Items
# Magic
# Skill
# Flee

import pelt
pelt.sync(313, True, 'Fur')

class Battle(object):
	def __init__(self, players, enemies):
		self.players = players
		self.enemies = enemies
	
	def main(self):
		while True:
			for c in self.getPlayers:
				if type(c) == Ally:
					action = pelt.getInput.choice('What to do?',['Attack','Er...','Um...'])
					if action == 'Attack': self.attack(c)
				elif type(c) == Enemy:
					pass
	
	def getPlayers(self):
		chars = self.players + self.enemies
		return [c in chars if c.life > 0]

	def attack(self, player):
		attack = pelt.getInput.choice('Which Attack?', player.attacks)
		enemy = pelt.getInput.choice('Attack Who?', self.enemies)
		attack.use(player, enemy)

	def items():
		pass

	def magic():
		pass

	def skill():
		pass

	def flee():
		pass

if __name__ in '__main__':
	player = pelt.Ally('Somewhere', 'Dark', 'Tailed', 'Wolf', 'Boy', 1)
	friend = pelt.Ally('Somewhere', 'Moon', 'Tailed', 'Fox', 'Girl', 1)
	enemy = pelt.Enemy('Sunwing', 1, 50)
	
	battle = Battle([player, friend], [enemy])
	battle.main()