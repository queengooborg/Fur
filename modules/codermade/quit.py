def quit(msg, nosave=False):
	global ios, devplayer
	if nosave: pass
	else: save()
	color('red')
	if ios and not devplayer: notification.schedule(output('mailto2', r=1), 15, 'Beep', output('mailto1', r=1))
	if msg: sys.exit(msg)
	else: sys.exit(0)