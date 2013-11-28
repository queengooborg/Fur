#Fur Custom Level Functions
#Created November 26, 2013 at 18:32
#Last modified November 26, 2013 at 19:10

import socket

#socket.settimeout(30)

import urllib2
import easygui as eg

def internet(page, timeout=10):
	pass #return urllib2.urlopen(page, timeout)

def output(msg, newline=True, noscroll=False):
	for c in msg:
		sys.stdout.write(c)
		if not noscroll:
			sys.stdout.flush()
			sleep(0.03)
	if newline: sys.stdout.write('\n')
	sys.stdout.flush()

domain = "http://kageashi.no-ip.biz/furcommunity/"

def connect():
	output('Connecting to KageASHI...')
	try: success = urllib2.urlopen(domain, None, 10)
	except:
		output('Sorry, cannot connect to KageASHI.  More details will be shown in a new window.')
		eg.exceptionbox()