
import sys
sys.path.append("../src")
from tree import Tree

if __name__ == "__main__":
	newickfn = "getEachSubTreeLeafLabelSetStrs-in.nwk"

	nwk = ''
	with open(newickfn, 'r') as ifd:
		for line in ifd:
			nwk += line.rstrip('\n')
	
	t = Tree(newick=nwk, name='x')

	with open("getEachSubTreeLeafLabelSetStrs-out.txt", 'w') as ofd:
		ofd.write('\n'.join(t.getEachSubTreeLeafLabelSetStrs()) + '\n')
	
