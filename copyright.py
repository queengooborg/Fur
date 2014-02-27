#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
from pelt import credit, config
from os.path import join

display.set_mode((0,0), FULLSCREEN)

text = """CREDITS
_                                                 _

_Storyline_\\Kurai Atonitsuka (Dark Tailed)
\\Black Ice (Torrin Rich)

_Programming_\\Kurai Atonitsuka (Dark Tailed)
\\Light Apacha (Mike Glover)

_Beta Testing_\\Silver Powell (Sagan Oliphant)
\\Black Ice (Torrin Rich)
\\Luce Renard (Elliot Lialias)
\\Conor Hakai (Logan Mitchell)


Fur and the PELT Enging Made By:
Nightwave Studios

_                                                 _

©Copyright 2013-14"""

#~ use '\\' to align the text

font = font.Font(join(config.fontdir, "Roboto-MediumItalic.ttf"),20)
color = 0xa0a0a000

credit(text,font,color)
