
import sys
sys.path.append("../src")
from tree import Tree

if __name__ == "__main__":
	newickfn = "containsSubtreeBasedOnSetOfLeafLabels-in1.nwk"
	newickfn2 = "containsSubtreeBasedOnSetOfLeafLabels-in2.nwk"

	nwk = ''
	with open(newickfn, 'r') as ifd:
		for line in ifd:
			nwk += line.rstrip('\n')
	
	t = Tree(newick=nwk, name='x')

	nwk = ''
	with open(newickfn2, 'r') as ifd:
		for line in ifd:
			nwk += line.rstrip('\n')

	t2 = Tree(newick=nwk, name='y')

	with open("containsSubtreeBasedOnSetOfLeafLabels-out.txt", 'w') as ofd:
		ofd.write("Tree #1 has the following topology:\n")
		ofd.write(t.getAscii())
		ofd.write("\n#########################\n")
		ofd.write("\nTree #2 has the following topology:\n")
		ofd.write(t2.getAscii())
		ofd.write("\n#########################\n")
		ofd.write("\nFor each subtree in Tree #2, the tree topology will be displayed with the phrase\n'present' or 'not present' to indicate whether that subtree appears also in Tree #1\n")
		ofd.write("\n#########################\n\n")
		for node in t2.generateNodesViaDepthFirstTraversal():
			status = "present" if t.containsSubtreeBasedOnSetOfLeafLabels(node) else "not present"
			ofd.write(node.label + ": " + status + '\n')
			ofd.write(node.getAscii())
			ofd.write("\n###\n")
	
