try:
	from Fur import *
	init()
except:
	import console, traceback
	
	console.set_color(0, 0.8, 0)
	print("Type: "+str(sys.exc_info()[0]))
	
	console.set_color(0.8, 0, 0)
	print("\n\n"+traceback.format_exc())
