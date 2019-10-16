
import sys
sys.path.append("../src")
from tree import Tree

if __name__ == "__main__":
	newickfn = "io-in.nwk"

	nwk = ''
	with open(newickfn, 'r') as ifd:
		for line in ifd:
			nwk += line.rstrip('\n')
	
	t = Tree(newick=nwk, name='x')

	with open("io-out.nwk", 'w') as ofd:
		ofd.write(t.getNewick())
	
	with open("io-out.json", 'w') as ofd:
		ofd.write(t.getJson())
	
	with open("io-out-pretty.json", 'w') as ofd:
		ofd.write(t.getPrettyJson())
	
