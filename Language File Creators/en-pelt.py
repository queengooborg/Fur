# -*- coding: utf-8 -*-

msgs = {'title':'%s',
'title2':'%s - Version %s',
'author':'Made by %s',
'version':'Version %s, Pelt Version %s',
'save1':'Save %s',
'save2':'Save %s: %s',
'save3':'Save to File',
'save4':'Load File',
'savewarning':'WARNING: File belongs to %s %s the %s.  Okay to overwrite?',
'saveerror':'Not a valid save file.',
'colorerror':'Color input was invalid.',
'inputerror':'Invalid Input',
'next':'Next Page',
'yes':'Yes',
'no':'No',
'quit':'Quit',
'back':'Back',
'cancel':'Cancel',
'ok':'Ok',
'open':'open',
'closed':'closed',
'med':'Medium',
'fast':'Fast',
'slow':'Slow',
'boy':'Boy',
'girl':'Girl',
'doormissing':"There is no door in that direction.",
'doorlocked':"You try to open the door but the handle won't budge.",
'directionerror':"That's not a proper direction.",
'itemerror':"I don't see any %s here.",
'cmderror':"I don't know how to do that.",
'with':'with',
'using':'using',
'usingerror':"What do you want to %s the %s with?",
'itemnormal':"This %s doesn't seem to be unusual.",
'chestdescopen':"A chest that contains %s and is open.",
'chestdescclosed':'A closed chest.',
'chestopenerror':'The chest is already open!',
'chestopen':'Opened the chest, %s was inside.',
'chestunlocked':'Unlocked the chest using %s.',
'chestlocked':'Chest is locked with a key.',
'foodpoisoned':"That %s was covered in fatal poison.  You are now dead.",
'foodpoisonedmsg':'User ate a poisoned %s',
'foodeaten':"That %s was very tasty!",
'drinkpoisoned':"That %s had a fatal poison inside.  You are now dead.",
'drinkpoisonedmsg':'User drank poison from a %s',
'playerdesc':'%s %s the %s %s, carrying %s, at %s, Level %s.  Can use the attacks %s',
'attackerror':'Not a valid attack.',
'itemhere':"There is a %s here",
'doorhere':"There is a door to the %s",
'doordesc':"A door to the %s that leads to the %s.",
'attack1':'Punch',
'attack1desc':'A simple punch',
'type1':'Normal',
'lang':'Language',
'iosask':'Are you on an iPhone or iPad?  This is important for gameplay.',
'iosquit':'User did not choose iPhone or iPad.'
}

import pickle, os.path

rootdir = os.path.dirname(os.path.dirname(__file__))
resourcedir = os.path.join(rootdir, 'resources')
langsdir = os.path.join(resourcedir, 'langs')
langdir = os.path.join(langsdir, 'en')

with open(os.path.join(langdir, "en-pelt.lang"), 'wb') as handle: pickle.dump(msgs, handle)