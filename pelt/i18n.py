#PELT I18N (Internationalization)
#Created December 4, 2013 at 15:30

import config
import os.path, pickle, re

def setlang(lang):
	global msgs
	langdir = os.path.join(config.langdir, lang)
	msgs = {}
	for l in os.listdir(langdir):
		langfile = os.path.join(langdir, l)
		if not "Icon" in l:
			if not "desktop.ini" in l:
				if not ".DS_Store" in l:
					with open(langfile, 'rb') as handle: msgs.update(pickle.load(handle))
	config.lang = lang
	config.saveopt()
	
def m(key, r=0, modifier='normal', color=False):
	global msgs
	if r == 1: print "You should fix this message, it has m('"+key+"', r=1).  Remove the r=1"
	msg = msgs[key]
	if not color: re.sub(msg, "\[[^\]]\]", "")
	return msg
	#if modifier == 'caps': msg = msgs[key].upper()
	#elif modifier == 'title': msg = msgs[key].title()
	#elif modifier == 'lower': msg = msgs[key].lower()
	#return msg

setlang('en')