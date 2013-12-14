msgs = {'nofriendnameerror':"You didn't type your friend's name!  Remember, %s is a %s.",
'he':'he',
'she':'she',
'her':'her',
'him':'him',
'his':'his',
'meyou':"me and you",
'you':"you",
'wolf':"Wolf",
'cat':"Cat",
'dragon':"Dragon",
'bear':"Bear",
'fox':"Fox",
'mouse':"Mouse",
'bird':"Bird",
'otter':"Otter",
'broken1':'There are some parts of the game that are broken at the moment.  Those parts will be fixed soon.  To close these popup alerts, press "%s"',
'broken2':'Broken ATM',
'broken3':"It's broken at the moment!",
'broken4':"Next part is still in development.  Please load in a developer save to unlock the next part.",
'start':'Start Game',
'new':'New Game',
'load':'Load Game (Broken ATM)',
'custom':'Community Levels',
'options':'Options',
'scroll':'Scroll Speed (%s)',
'annoy':'Annoyance Mode (Broken ATM)',
'beta':'Beta Tester Mode',
'annoyon':"Annoyance mode now active.",
'betaon':"Beta tester mode now active.",
'annoyoff':"Annoyance mode revoked.",
'betaoff':"Beta tester mode revoked.",
'quitmsg':"Quit on user's demand.",
'custtitle':"Custom Levels Menu",
'custstart':'Start Level',
'custdown':'Download Level',
'custup':'Upload Level',
'custcreate':'Create Level',
'setupgndr':'Are you a boy or a girl?',
'setuprace':"Choose an animal.",
'setupname':'Your name is?',
'setuplast':'%s...and your last?',
'setupeyeclose':'%s %s...Good.  Now you may enter the gates and find yourself in "Fur"...close your eyes and count to 3, then open your eyes...',
'setupeyeopen':"You should've opened your eyes by now.  Good.  You have finished your rebirth.  You will enter Quilar as a half-%s...",
'p1m1':'???: ...',
'p1m2':'???: ...Hey...',
'p1m3':'???: ...Wake up...',
'p1m4':'???: ...Hey, you lazy %s!',
'p1m5':'???: Wake up!',
'p1m6':'You slowly open your eyes.  A young %s about your age is trying to shake you awake.  You notice something strange about the %s, but your eyes are still blurred from waking up.',
'p1m7':"???: You're awake!  I've been shaking you for over an hour or so!",
'p1m8':"Your eyes focus and you figure out why the %s looked so strange.  %s was fox-like, with fur covering %s entire body, and a big tail sticking out behind %s.",
'p1m9':"Your eyes widen and you quickly push yourself back into the wall.  You then raise your arms ready to attack.",
'p1m10':'You: Who are you?',
'p1m11':"???: Me?  My name is...",
'setup9':'Enter the name of your friend, remember, %s is a %s.',
'p1m12':"%s.  What's yours?",
'p1m13':"You lower your fists.",
'p1m14':"You: ...I'm %s.",
'p1m15':"%s: %s...it's a funny name for a %s like %s!",
'p1m16':"You: What?",
'p1m17':"You then look down at yourself.  %s",
'foxdesc':"You also look just like a fox, with a tail and everything.",
'dragondesc':"You have scales and the tail of a dragon.  In your throat you feel a hot presence.",
'p1m18':"They are in a similar state to those of the %s's.",
'birddesc':"However you have feathers down your arms like wings and a retrice.  You feel your face and find a bird's beak for your mouth.",
'wolfdesc':"However you look more like a wolf with a wolf's tail.  You feel your face and find a big snout.",
'catdesc':"However your hands have very sharp claws and you look more like a cat.",
'beardesc':"However you have big hands, big feet, and a short, stubby tail.  You have brown fur just like a bear.",
'mousedesc':"However you have small hands, a skinny tail, and big ears, just like a mouse.",
'otterdesc':"However your hands look more like an otter's.  You feel your face and find wet quills.  Behind you is a long tail.",
'p1m19':"You start to panic inside.  You think 'what is going on?'",
'p1m20':"%s: ...What?",
'p1m21':"You tell yourself to calm down so you can figure out why you're half-%s.",
'p1m22':"You: I'm a human though...",
'p1m23':"You accidentally said the last part out loud.  You meant only to think it.",
'p1m24':"%s: WHAT!  You can't be, you've got every aspect of a %s anthro...(%s comes close to you and sniffs you, then pulls back)...and you smell just like one too.",
'p1m25':"You: Yeah, thanks.",
'p1m26':"%s: I didn't mean it like that!",
'p1m27':"You: I don't know what's going on, but we're going to have to find out.  Where are we?",
'p1title':'PART 1: The Awakening',
'gamestart':"You are in a room.",
'gameaction':"What will you do?",
'gameinputerror':"I didn't understand what you typed.",
'helpquit':'quit - Saves and quits the game.',
'quitmsg':"Quit on user's demand.",
'quitcmd':'quit',
'savecmd':'save',
'helpsave':'save - Saves the game',
'loadcmd':'load',
'helpload':'load - Loads the game from a save file (dangerous)',
'helpcmd':'help',
'helphelp':'help - Displays this message',
'examinecmd':'examine',
'helpexamine':'examine [item] - shows description of item',
'eatcmd':'eat',
'helpeat':'eat [item] - If item is food, will eat item',
'drinkcmd':'drink',
'helpdrink':'drink [item] - if item is a drink, will drink item',
'takecmd':'take',
'helptake':'take [item] - if item is movable, will take item',
'gocmd':'go',
'helpgo':'go [direction] - Go through the door in the defined direction',
'opencmd':'open',
}

import pickle, os.path

rootdir = os.path.dirname(os.path.dirname(__file__))
resourcedir = os.path.join(rootdir, 'resources')
langsdir = os.path.join(resourcedir, 'langs')
langdir = os.path.join(langsdir, 'xn')

with open(os.path.join(langdir, "xino.lang"), 'wb') as handle: pickle.dump(msgs, handle)
