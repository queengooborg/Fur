#Pelt Colors
#Created Febuary 5, 2014 at 17:53

import sys
import colorama
import config

#Color Name			R,    G,    B
BLACK =				0,    0,    0
GRAY = GREY =		149,  149,  149
WHITE =				255,  255,  255
RED =				255,  0,    0
GREEN =				0,    255,  0
BLUE =				0,    0,    255
ORANGE =			255,  112,  0
YELLOW =			255,  255,  0
AQUA =				0,    191,  243
PURPLE =			101,  39,   170
LIME =				138,  211,  60
SILVER =			161,  161,  161
FUCHSIA =			255,  0,    255
NAVY =				0,    0,    128
OLIVE =				128,  128,  0
TEAL =				0,    128,  128
SHADOW =			78,   30,   132

#Launchpad Colors
LpRed = 7
LpOrange = 83
LpGreen = 124
LpYellow = 127

try: styles = colorama.Fore.WHITE #Set color to default...
except: styles = '' #...and set to a blank string if on iOS

def color(color):
	global styles
	try: #If styles is greater than 20, reset...
		if len(styles) > 20: styles = colorama.Fore.WHITE
		styles = colorama.Fore.WHITE
	except: pass #...or pass if on iOS
	if color == 'red':
		try: console.set_color(1.0, 0.0, 0.0)
		except: styles += colorama.Fore.RED
	elif color == 'green':
		try: console.set_color(0.2, 0.8, 0.2)
		except: styles += colorama.Fore.GREEN
	elif color == 'blue':
		try: console.set_color(0.0, 0.0, 1.0)
		except: styles += colorama.Fore.CYAN
	elif color == 'yellow':
		try: console.set_color(0.6, 0.6, 0.1)
		except: styles += colorama.Fore.YELLOW
	elif color == 'darkblue':
		try: console.set_color(0.6, 0.6, 1.0)
		except: styles += colorama.Fore.BLUE
	elif color == 'magneta':
		try: console.set_color(1.0, 0.2, 1.0)
		except: styles += colorama.Fore.MAGENTA
	elif color == 'reset':
		try:
			console.set_color(0.2, 0.2, 0.2)
			console.set_font()
		except: styles += colorama.Fore.WHITE
	elif color == 'random':
		try: console.set_color(random.random(),random.random(),random.random())
		except:
			list = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN, colorama.Fore.WHITE]
			styles += random.choice(list)
	elif color == 'bold':
		try: console.set_font('Helvetica', 32.0)
		except: pass
	else: output('colorerror')
	if styles and config.color:
		sys.stdout.write(styles)
		sys.stdout.flush()