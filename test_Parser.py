import Parser
import unittest

class ParserTest(unittest.TestCase):
	def testPreprocessComment(self):
		lines = Parser.preprocess("[]")
		self.assertEqual([], lines)
	
	def testPreprocessBlanklines(self):
		testdata = """Hello
		
		Goodbye"""
		lines = Parser.preprocess(testdata)
		self.assertEqual(['Hello','Goodbye'], lines)
	
	def testPreprocess(self):
		testPreprocessComment()
		test
	
	def test_getblock(self):
		r = Parser.getblocks('X', 'Y', ['6','X',' ', 'b', 'Y', 'foo', 'X', 'bar', 'baz', 'foobar', 'Y', 'X', 'T', 'Y'], 2)
		self.assertEqual(r, [[' ', 'b'], ['bar','baz','foobar']])
	
if __name__ == '__main__':
	unittest.main()