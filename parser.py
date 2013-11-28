#PELT Level Parser
#Created November 4, 2013 at 18:58
#Last modified October 31, 2013 at 14:04

import sys, re
from pelt import *

if __name__ == '__main__':
	with open('levels/part1.plf','rb') as handle: parselevel(handle)
