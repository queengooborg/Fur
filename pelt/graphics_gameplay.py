import sys, pygame
from color import *
from level import Room
from menu import dumbmenu as dm

TILESIZE = TILEWIDTH, TILEHEIGHT = 32, 32

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
SIZE = WIDTH, HEIGHT = screen.get_size()
TILECOUNT = TILECOUNTW, TILECOUNTH = WIDTH/TILEWIDTH, HEIGHT/TILEHEIGHT

FONTPATH = '../resources/fonts/Roboto-MediumItalic.ttf'

class PyGameAPI(object):
	def __init__(self, screen):
		self.screen = screen
		self.fonts = {
			'small': pygame.font.Font(FONTPATH, 12),
			'med':   pygame.font.Font(FONTPATH, 18),
			'large': pygame.font.Font(FONTPATH, 24)
		}
		self.clean()
	
	def clean(self): screen.fill(BLACK)
	
	def text(self, msg, pos, size, color=WHITE, antialias=True):
		surface = self.fonts[size].render(msg, antialias, color)
		self.screen.blit(surface, pos)
	
	def dialogue(self, character, msg, color=WHITE, antialias=True):
		position = xpos, ypos = 0, (HEIGHT/4)*3
		size = xsize, ysize = WIDTH, HEIGHT/4
		dbox = pygame.Surface(size, pygame.SRCALPHA)
		dbox.fill(SILVER)
		screen.blit(dbox, position)
		
		self.text(character, (TILEWIDTH*3, 0+ypos),          'large')
		self.text(msg,       (TILEWIDTH*3, TILEHEIGHT+ypos), 'small')
		
		pygame.display.flip()
	
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.KEYDOWN: return

gui = PyGameAPI(screen)

elements = []

class Element(object):
	def __init__(self, name, pos, size, color, alpha=255):
		self.name = name
		assert len(size) == 2
		assert len(pos) == 2
		self.x, self.y = pos
		self.w, self.h = size
		self.surface = pygame.Surface((self.w*TILEWIDTH, self.h*TILEHEIGHT), pygame.SRCALPHA)
		self.color = tuple(list(color)+[alpha])

	def render(self, parent):
		self.surface.fill(self.color)
		parent.blit(self.surface, (self.x*TILEWIDTH, self.y*TILEHEIGHT))

	def move(self, x, y):
		self.x += x
		self.y += y

keys = {
	'up':    pygame.K_UP,
	'down':  pygame.K_DOWN,
	'left':  pygame.K_LEFT,
	'right': pygame.K_RIGHT
}

roomclass = Room("Test Room", (10,8), (1,1), [], [])
room = Element('room', (1,1), roomclass.size, ORANGE)
elements.append(room)

player = Element('player', ((TILECOUNTW/2), (TILECOUNTH/2)), (1,1), SHADOW, alpha=128)
elements.append(player)

def game():
	gui.clean()
	gui.dialogue('Test Character', "Hello, I don't have a name.  But I'm just going to say random stuff.  :)")
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == keys['up']:
					player.move(0,-1)
				if event.key == keys['down']:
					player.move(0,1)
				if event.key == keys['left']:
					player.move(-1,0)
				if event.key == keys['right']:
					player.move(1,0)
				if event.key == pygame.K_ESCAPE: return

		gui.clean()
		for el in elements: el.render(screen)
		pygame.display.flip()

def init():
	global screen
	options = ["Start Game", "Custom Levels", "Options", "Quit"]

	myfont = pygame.font.Font(None, 32)
	gui.clean()
	choice = dm(screen, options, WIDTH // 2, HEIGHT // 2, None, 32, 1.4, GREEN, PURPLE) + 1
	
	if choice == 1:
		game()
	
	elif choice == 3:
		pass
	
	elif choice == 4:
		pygame.quit()
		sys.exit()
	
	else:
		screen.fill(PURPLE)
		text = myfont.render("User picked "+options[choice-1], True, RED)
		textrect = text.get_rect()
		textrect = textrect.move((WIDTH-textrect.width) // 2, (HEIGHT-textrect.height) // 2)
		screen.blit(text, textrect)
		pygame.display.update(textrect)

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					return

if __name__ == '__main__':
	while True: init()
