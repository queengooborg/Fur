import parser
import unittest

class ParserTest(unittest.TestCase):
	# def testPreprocess(self):
# 		testdata = """Hello
# 		[Hi there]
# 		Goodbye"""
# 		lines = parser.preprocess(testdata)
# 		self.assertEqual(['Hello','Goodbye'], lines)
# 	
# 	def testMultiLineComment(self):
# 		testdata = """Hello
# 		[Hi
# 		there]
# 		Goodbye"""
# 		lines = parser.preprocess(testdata)
# 		self.assertEqual(['Hello','Goodbye'], lines)
# 	
# 	def testMultiCharacterGetBlocks(self):
# 		v = parser.getblocks('Foo', 'bar', ['Foo','baz','bastard','bar'], 1)
# 		self.assertEqual(v, [['baz', 'bastard']])
# 	
# 	def testGetBlocks(self):
# 		r = parser.getblocks('X', 'Y', ['6','X',' ', 'b', 'Y', 'foo', 'X', 'bar', 'baz', 'foobar', 'Y', 'X', 'T', 'Y'], 2)
# 		self.assertEqual(r, [[' ', 'b'], ['bar','baz','foobar']])
	
	def testParseLevel(self):
		level = """Level is "Whatever the Heck" sized 2x3
		
		Dialogue is:
		Finish Dialogue
		
		Room is:
			Called "Main Room" sized 17x10 placed A20x27
			Door to "Balcony" on Top 1 from Left
			Door to "Hallway" on Top 2 from Right locked with "Rusty Key"
			Door to "Play Room" on Bottom 4 from Right locked with "Silver Key"
			Trapdoor to "Chest Room" 1 from Left 2 from Bottom locked with "Fire Circle" (Hidden)
		Finish Room
		"""
		
		l = parser.Level.fromText(level)
		self.assertEqual(l.name, "Whatever the Heck")
		self.assertEqual(l.size, (2,3))
		print rooms
	
if __name__ == '__main__':
	unittest.main()