#PELT Battle Sequence
#Created September 3, 2013 at 13:20

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
	
	def getPlayers(self):
		chars = self.players + self.enemies
		return [c for c in chars if c.life > 0]
	
	def main(self):
		while True:
			for c in self.getPlayers():
				if type(c) == pelt.Ally:
					action = pelt.getInput.choice('What to do?',['Attack','Er...','Um...'])
					if action == 'Attack': self.attack(c)
				elif type(c) == pelt.Enemy:
					pass

	def attack(self, player):
		atk = pelt.getInput.choice('Which Attack?', player.attacks)
		enemy = pelt.getInput.choice('Attack Who?', self.enemies)
		atk.use(player, enemy)

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