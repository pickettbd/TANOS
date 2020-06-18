
import sys
sys.path.append("../src")
from tree import Tree

if __name__ == "__main__":
	newickfn = "getEachSubTreeLeafLabelSets-in.nwk"

	nwk = ''
	with open(newickfn, 'r') as ifd:
		for line in ifd:
			nwk += line.rstrip('\n')
	
	t = Tree(newick=nwk, name='x')

	with open("getEachSubTreeLeafLabelSets-out.txt", 'w') as ofd:
		for leaf_label_set in t.getEachSubTreeLeafLabelSets():
			ofd.write(''.join(leaf_label_set) + '\n')
	
