#PELT Config
#Created December 4, 2013 at 15:22

import pickle, os.path, sys

join = os.path.join

rootdir = os.path.dirname(os.path.dirname(__file__))
resourcedir = join(rootdir, 'resources')
langdir = join(resourcedir, 'langs')
fontdir = join(resourcedir, 'fonts')
mapdir = join(resourcedir, 'levels')
optionspath = os.path.join(resourcedir, 'options.pyp')

args = sys.argv[1:]

devplayer = False
annoy = False
gui = True
color = True
instmsg = False

if len(args) > 0:
	if "nostory" in args:
		loc = 'p1MainRoom'
		gameplay()
	if "betatester" in args: devplayer = True
	if "annoy" in args: annoy = True
	if "nogui" in args: gui = False
	if "nocolor" in args: color = False
	if "instmsg" in args: instmsg = True

try:
	with open(optionspath, 'rb') as handle:
		handle = pickle.load(handle)
		lang = handle[0]
		scrollspeed = handle[1]
		if scrollspeed == 'Fast': scroll = 0.01
		elif scrollspeed == 'Medium': scroll = 0.03
		elif scrollspeed == 'Slow': scroll = 0.05
		annoy = handle[2]
		devplayer = handle[3]
	if lang == "English": lang = 'en'
except (pickle.UnpicklingError, IndexError, EOFError):
	scrollspeed = 'Medium'
	scroll = 0.03
	lang = 'en'
	annoy = False
	devplayer = True

def saveopt():
	with open(optionspath, 'wb') as handle: pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
