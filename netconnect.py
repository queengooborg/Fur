#Fur Network Connection Functions
#Created Febuary 20, 2014 at 15:11

import webbrowser, urllib2, sys, json
from pelt import localio

def output(msg, *args, **kwargs): print msg

def connect(url='', browser=False):
	try:
		if browser:
			webbrowser.open(site+url)
			localio.getInput.alert('Click Ok/Cancel...')
		else: return urllib2.urlopen(site+url, None, 10).read()
	except (urllib2.URLError, urllib2.HTTPError) as error:
		output('Sorry, cannot connect to the web page: %s' %url)
		print error
		return False

def poutput(msg, newline=True, noscroll=False):
	for c in msg:
		sys.stdout.write(c)
		if not noscroll:
			sys.stdout.flush()
			sleep(0.03)
	if newline: sys.stdout.write('\n')
	sys.stdout.flush()

domain = "kageashi.no-ip.biz"
#domain = "localhost"
site = "http://"+domain+"/furcommunity/"

success = connect() # test connection