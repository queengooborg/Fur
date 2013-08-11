def language():
	global lang, msgs
	wait=True
	wait2=True
	while wait:
		while wait2:
			choice = getInput.choice('Language/Idioma', ['English','Espanol (Archivo del Idioma no Esta Presente)','Francais (Fichier de Langue pas present', 'Quit'])
			if choice == 1:
				lang = "English"
				with open('options', 'wb') as handle: pickle.dump([lang, scrollspeed, annoy, devplayer], handle)
				wait2=False
			elif choice == 0 or choice == 4: quit('', nosave=True)
			else: output("Invalid option/Opcion incorrecto/L'option invalide", dict=True)
		if lang == "English":
			with open('english.lang', 'rb') as handle: msgs = pickle.load(handle)
		else: output("Language File Version Incompatible/Version del Archivo del Idioma Incompatible/Version de L'archive du Language Incompatible", dict=True)