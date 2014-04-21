import sys, pygame

#Color Name			R,   G,   B
BLACK =				0,   0,   0
GRAY = GREY =		149, 149, 149
WHITE =				255, 255, 255
RED =				255, 0,   0
GREEN =				0,   255, 0
BLUE =				0,   0,   255
ORANGE =			255, 112, 0
YELLOW =			255, 255, 0
AQUA =				0,   191, 243
PURPLE =			101, 39,  170
LIME =				138, 211, 60
SILVER =			161, 161, 161
FUCHSIA =			255, 0,   255
NAVY =				0,   0,   128
OLIVE =				128, 128, 0
TEAL =				0,   128, 128
SHADOW =			78,  30,  132

TILECOUNT = len(sys.argv) > 1 and int(sys.argv[1]) or 16
TILESIZE = TILEWIDTH, TILEHEIGHT = 32, 32
SIZE = WIDTH, HEIGHT = TILEWIDTH * TILECOUNT, TILEHEIGHT * TILECOUNT

elements = []

class Element(object):
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
		self.surface = pygame.Surface(TILESIZE, pygame.SRCALPHA)

	def render(self, parent):
		self.surface.fill(tuple(list(SHADOW)+[128]))
		parent.blit(self.surface, (self.x, self.y))

	def move(self, x, y):
		self.x += x * TILEWIDTH
		self.y += y * TILEHEIGHT

player = Element('player', (WIDTH/2)-(TILEWIDTH/2), (HEIGHT/2)-(TILEHEIGHT/2))
elements.append(player)

pygame.init()
screen = pygame.display.set_mode(SIZE)

def dialogue(character, msg, color=WHITE, antialias=True):
	position = xpos, ypos = 0, (HEIGHT/4)*3
	size = xsize, ysize = WIDTH, HEIGHT/4
	dbox = pygame.Surface(size, pygame.SRCALPHA)
	dbox.fill(SILVER)
	
	font = pygame.font.Font('../resources/fonts/Roboto-MediumItalic.ttf', 24)
	fontsurface = font.render(character, antialias, color)
	dbox.blit(fontsurface, (TILEWIDTH*3, 0))
	screen.blit(dbox, position)
	pygame.display.flip()
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN: return

dialogue('Test Character', "Hello, I don't have a name.  But I'm just going to say random stuff.  :)")

def main():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					player.move(-1,0)
				if event.key == pygame.K_d:
					player.move(1,0)
				if event.key == pygame.K_w:
					player.move(0,-1)
				if event.key == pygame.K_s:
					player.move(0,1)
				if event.key == pygame.K_ESCAPE: sys.exit()

		screen.fill(BLACK)
		for el in elements: el.render(screen)
		pygame.display.flip()

main()