#PELT Menu
#Created Febuary 3, 2014 at 14:23

import sys, pygame
#from pelt import *
from menu import dumbmenu as dm
pygame.init()
pygame.font.init()

# Colors (R, G, B)
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
PURPLE = 101, 39, 170

while True:
	options = ["Start Game", "Custom Levels", "Options", "Quit"]

	size = width, height = 0, 0
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	size = width, height = screen.get_size()
	myfont = pygame.font.Font(None, 32)

	screen.fill(BLACK)

	choice = dm(screen, options, width // 2, height // 2, None, 32, 1.4, GREEN, PURPLE) + 1

	if choice == 4:
		pygame.quit()
		sys.exit()

	screen.fill(PURPLE)
	text = myfont.render("User picked "+options[choice], True, RED)
	textrect = text.get_rect()
	textrect = textrect.move((width-textrect.width) // 2, (height-textrect.height) // 2)
	screen.blit(text, textrect)
	pygame.display.update(textrect)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				pygame.quit()
				sys.exit()