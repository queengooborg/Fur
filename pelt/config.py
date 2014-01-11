#PELT Config
#Created December 4, 2013 at 15:22

import pickle, os.path

rootdir = os.path.dirname(os.path.dirname(__file__))
resourcedir = os.path.join(rootdir, 'resources')
langdir = os.path.join(resourcedir, 'langs')
optionspath = os.path.join(resourcedir, 'options.pyp')

gui = True

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
		gui = True
	if lang == "English": lang = 'en'
except (pickle.UnpicklingError, IndexError, EOFError):
	scrollspeed = 'Medium'
	scroll = 0.03
	lang = 'en'
	annoy = False
	devplayer = True
	gui = True

def saveopt():
	with open(optionspath, 'wb') as handle: pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
