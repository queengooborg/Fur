#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
from sys import exit
font.init()

def credit(text,font,color):

	try: text = text.decode('utf-8')
	except: pass

	try: color = Color(color)
	except: color = Color(*color)

	clk = time.Clock()

	scr = display.get_surface()
	scrrect = scr.get_rect()
	bg = scr.copy()

	w,h = font.size(' ')
	Rright = scrrect.centerx + w*3
	Rleft = scrrect.centerx - w*3


	foo = []
	for i,l in enumerate(text.splitlines()):
		a,b,c = l.partition('\\')
		u = False
		if a:
			if a.startswith('_') and a.endswith('_'):
				u = True
				a = a.strip('_')
			rect = Rect((0,0),font.size(a))
			if b: rect.topright = Rleft,scrrect.bottom+h*i
			else: rect.midtop = scrrect.centerx,scrrect.bottom+h*i
			foo.append([a,rect,u])
		u = False
		if c:
			if c.startswith('_') and c.endswith('_'):
				u = True
				c = c.strip('_')
			rect = Rect((0,0),font.size(c))
			rect.topleft = Rright,scrrect.bottom+h*i
			foo.append([c,rect,u])

	y = 0
	while foo and not event.peek(QUIT):
		for e in event.get():
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				quit()
				exit()
		event.clear()
		y -= 1
		for p in foo[:]:
			r = p[1].move(0,y)
			if r.bottom < 0:
				foo.pop(0)
				continue
			if not isinstance(p[0],Surface):
				if p[2]: font.set_underline(1)
				p[0] = font.render(p[0],1,color)
				font.set_underline(0)
			scr.blit(p[0],r)
			if r.top >= scrrect.bottom:
				break
		clk.tick(40)
		display.flip()
		scr.blit(bg,(0,0))

	display.flip()



