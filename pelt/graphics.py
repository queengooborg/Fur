try: 
	import scene
	import Image
	mod = scene
except ImportError: 
	import pygame
	mod = pygame
	
#Initialize graphics classes	
class GraphicsIO(object):
	def __init__(self, *args, **kwargs):
		pass
	def splash(self, title, logo, timeout):
		pass
	
class SceneIO(GraphicsIO):
	def __init__(self, *args, **kwargs):
		GraphicsIO.__init__(self, *args, **kwargs)
		
	class splash(Scene):
		def __init__(self, title, logo, timeout):
			self.title = title
			self.logo = logo
			self.timeout = timeout
			Scene.__init__(self)
			scene.run(self)
							
		def draw(self):
			
				
	
class PyGameIO(GraphicsIO):
	pass

#Splash screen
