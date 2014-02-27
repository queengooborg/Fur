#Some elements from PyLaunchpad were used in this code.  They are surrounded by # --- # and #! --- !#

def print_message(midi):
	if midi.isNoteOn():
		print 'ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity()
	elif midi.isNoteOff():
		print 'OFF:', midi.getMidiNoteName(midi.getNoteNumber())
	elif midi.isController():
		print 'CONTROLLER', midi.getControllerNumber(), midi.getControllerValue()


import rtmidi
from sys import exit
midiin  = rtmidi.RtMidiIn()  #initialize MIDI input
midiout = rtmidi.RtMidiOut() #initialize MIDI output
midiout.openPort(0)

#predefine some midi messages
reset = rtmidi.MidiMessage(0xb0, 0, 0)
setDrumMode = rtmidi.MidiMessage(0xb0, 0, 2)

# --------------------------------------------------------------------------- #

def _orderAll(levels):
	for y in range(8):
		for x in range(8):
			yield levels[x][7-y]
	x = 8
	for y in range(8):
		yield levels[x][7-y]
	
	y = 8
	for x in range(8):
		yield levels[x][y]

def light(x, y, red, green):
	if not 0 <= x <= 8: raise LaunchPadError("Bad x value %s" % x)
	if not 0 <= y <= 8: raise LaunchPadError("Bad y value %s" % y)
	if not 0 <= red <= 3: raise LaunchPadError("Bad red value %s" % red)
	if not 0 <= green <= 3: raise LaunchPadError("Bad green value %s" % green)
	
	velocity = 16*green + red + 8 + 4
	
	if y==8:
		if x != 8:
			note = 104 + x
			midiout.sendMessage(rtmidi.MidiMessage(0xb0,note,velocity))
		return
	
	if x==8:
		# Last column runs from 100 - 107
		note = 107-y;
	elif x<4:
		note = 36 + x + 4*y
	else:
		# Second half starts at 68, but x will start at 4
		note = 64 + x + 4*y
	
	midiout.sendMessage(rtmidi.MidiMessage(0x90,note,velocity))

def lightAll(levels):
	velocity = 0
	for level in _orderAll(levels):
		red = level[0]
		green = level[1]
		if velocity:
			velocity2 = 16*green + red + 8 + 4
			midiout.sendMessage(rtmidi.MidiMessage(0x92, velocity, velocity2))
			velocity = 0
		else:
			velocity = 16*green + red + 8 + 4
	light(0,0,levels[0][0][0],levels[0][0][1])

def lightAllTest():
	grid = []
	for x in range(9):
		grid.append([])
		for y in range(9): grid[x].append( (x%4, y%4) )

	lightAll(grid)

#! ------------------------------------------------------------------------- !#

midiout.sendMessage(reset)
midiout.sendMessage(setDrumMode)
lightAllTest()

ports = range(midiin.getPortCount())
if ports:
	for i in ports:
		print midiin.getPortName(i)
	midiin.openPort(i)
	while True:
		try:
			m = midiin.getMessage(250) # some timeout in ms
			if m != None:
				print_message(m)
		except KeyboardInterrupt: exit()
else:
	print 'NO MIDI INPUT PORTS!'