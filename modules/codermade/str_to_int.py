#converts a string to an integer and returns -1 if string is not a number
def str_to_int(text):
	try: response=int(text)
	except ValueError: return -1
	return response