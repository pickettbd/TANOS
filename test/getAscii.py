
import sys
sys.path.append("../src")
from tree import Tree

if __name__ == "__main__":
	newickfn = "getAscii-in.nwk"

	nwk = ''
	with open(newickfn, 'r') as ifd:
		for line in ifd:
			nwk += line.rstrip('\n')
	
	t = Tree(newick=nwk, name='x')

	with open("getAscii-out.txt", 'w') as ofd:
		ofd.write(t.getAscii())
	
