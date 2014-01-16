try:
	from Fur import * #Imports Fur
	init() #runs the game start function
except:
	import console, traceback
	
	console.set_color(0, 0.8, 0) #sets the color to green
	print("Type: "+str(sys.exc_info()[0])) #prints the type of exception
	
	console.set_color(0.8, 0, 0) #sets the color to red
	print("\n\n"+traceback.format_exc()) #prints error information
