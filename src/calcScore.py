#! /bin/env python3

__author__ = "Brandon Pickett"
__copyright_owner__ = "Brandon Pickett"
__copyright_year__ = "2019"
__version__ = "0.0.1-alpha"

# ----------- IMPORTS ---------------------------- ||
import sys
import argparse
from tree import Tree

# ---------- FUNCTIONS --------------------------- ||
def handleArgs():
	# define the main argument parser
	parser = argparse.ArgumentParser(prog="calcScore.py", add_help=False, allow_abbrev=True, 
									formatter_class=argparse.RawTextHelpFormatter, 
									description="Calculate the taxa resiliency for a provided tree. In effect, the question is\n" 
									"\"how resilient is the tree topology to the removal of taxa?\" To determine this,\n" 
									"we remove a taxon from the alignment and build a new tree, comparing it to the\n" 
									"original tree. To avoid anomalies, a new tree is built multiple times (say 50).\n" 
									"This is process is repeated for each taxon. Thus, if 100 taxa are in a given\n" 
									"tree and 50 replicates are performed for the removal of each taxon then 5,000\n" 
									"new trees are built. This package assumes the following has been performed:\n" 
									"\t1- The original alignment of all taxa\n" 
									"\t2- A tree built with all taxa\n" 
									"\t3- \"jackknifing\" the alignment (making one copy per taxon in the tree,\n" 
									"\t   minus that taxon)\n" 
									"\t4- New trees built using the \"jackknifed\" alignments with a\n" 
									"\t   pre-determined level of replication\n" 
									"This package compares the \"jackknifed\" trees (trees missing one taxon) with the\n" 
									"original tree. The effect on various clades in the original tree is quantified\n" 
									"and each node receives a score in the output tree. The score is meaningless for\n" 
									"the root node, leaf nodes, and parent of leaf nodes.\n" 
									"The program must have access to all the relevant trees (i.e., the original/main\n" 
									"tree and the \"jackknifed\" trees) and a mapping of which trees are associated\n" 
									"with which taxa. A default directory structure and file naming scheme is assumed.\n" 
									"Some program arguments change the assumptions about the directory structure\n" 
									"and/or file naming scheme. If your files are organized differently, the best\n" 
									"choice is to provide a list of file names with the associated taxa names.")

	# define argument groups
	input_group = parser.add_argument_group("Input Options", "These options affect how input files are found and/or interpreted.")
	output_group = parser.add_argument_group("Output Options", "These options affect which and how output files are generated.")
	misc_group = parser.add_argument_group("Misc. Options", "")

	# 	define input group options
	#		main tree
	input_group.add_argument("-m", "-mt", "--main-tree", dest="main_tree", metavar="tree.nwk", action="store", nargs=1, type=str, required=False,  default="data/mainTree/tree.nwk", 
						help="The main tree in Newick format for which you wish to determine the resiliency\n" 
						"against the removal of taxa." 
						" [data/mainTree/tree.nwk]\n \n")
	#		jackknife alignments and trees <-- delete
	#		jackknife trees
	input_group.add_argument("-d", "-jd", "--jackknife-dir", dest="jack_dir", metavar="path/to/jackknife/", action="store", nargs=1, type=str, required=False, default="data/jackknife", 
						help="The directory in which the jackknife data exists. Unless specified by other\n" 
						"options, two subdirectories are expected: \"aln\" and \"tree\"." 
						" [data/jackknife]\n \n")
	#			jackknife alignments <-- delete
	#input_group.add_argument("-a", "-ja", "--jackknife-aln", dest="jack_aln_dir", metavar="path/to/jackknife/aln/", action="store", nargs=1, type=str, required=False, default="data/jackknife/aln",  <-- delete
	#					help="The directory in which the jackknife alignment data exists. The directory should\n" <-- delete
	#					"contain one file per taxon in the main tree. Each file should be in fasta format.\n"  <-- delete
	#					"Unless specified by other options, the file names should match the taxa names in\n" <-- delete
	#					"the main tree file (case-sensitive!) and have the \".fa\" file extension (e.g.,\n" <-- delete
	#					"Cignobilis.fa). This option overrides -jd/--jackknife-dir for the jackknife\n"  <-- delete
	#					"alignment directory."  <-- delete
	#					" [data/jackknife/aln]\n \n") <-- delete
	#input_group.add_argument("-g", "--jackknife-aln-fofn", dest="jack_aln_fofn", metavar="path/to/alns.tsv", action="store", nargs=1, type=str, required=False, default=None,  <-- delete
	#					help="Instead of using -d, and -a to provide the jackknifed alignments, you may use\n"  <-- delete
	#					"this option to provide a list of filenames. The file must be in tab-separated\n"  <-- delete
	#					"value (tsv) format. Exactly two columns must exist on every line. No header/title\n"  <-- delete
	#					"line should exist. The first column should contain the taxon name\n"  <-- delete
	#					"(case-sensitive!). The second column should contain the path (absolute -or-\n"  <-- delete
	#					"relative to the directory from which the program is being run) to a jackknifed\n"  <-- delete
	#					"alignment file in Fasta format. This option overrides -d, and -a for the\n"  <-- delete
	#					"jackknife alignment files. The following is an example of how the file should\n"  <-- delete
	#					"look:\n"  <-- delete
	#					"\tCignobilis\tdata/jackknife/aln/Cignobilis.fa\n"  <-- delete
	#					"\tRmuscosa\tdata/jackknife/aln/Rmuscosa.fa\n"  <-- delete
	#					"\tAglossodonta\tdata/jackknife/aln/Aglossodonta.fa\n"  <-- delete
	#					"\tOclarkiistomias\tdata/jackknife/aln/Oclarkiistomias.fa\n"  <-- delete
	#					"\t...\n \n") <-- delete
	#			jackknife trees <-- delete
	input_group.add_argument("-t", "-jt", "--jackknife-tree", dest="jack_tree_dir", metavar="path/to/jackknife/tree/", action="store", nargs=1, type=str, required=False, default="data/jackknife/tree", 
						help="The directory in which the jackknife tree data exists. The directory should\n"
						"contain one subdirectory per taxon in the main tree. Each directory name should\n"
						"match the taxon name from the main tree file (case-sensitive!). In turn, each\n"
						"subdirectory should contain tree files in Newick format. Unless specified  by\n"
						"other options, the file names should be tree-${num}.nwk, where ${num} ranges from\n"
						"1-${rep}, where ${rep} is the number of jackknife replicates. In thoery, your\n"
						"files should fit in a nice range from 1-${rep}, but that is not strictly\n"
						"necessary. Using this option, the program will search for all files in the\n"
						"directory specified by -jt/--jackknife-tree that match the reg. exp.\n"
						"\"tree-\d+\.nwk\". This option overrides -jd/--jackknife-dir for the jackknife\n"
						"tree directory." 
						" [data/jackknife/tree]\n \n")
	input_group.add_argument("-e", "-te", "--tree-ext", dest="jack_tree_fn_ext", metavar=".ext", action="store", nargs=1, type=str, required=False, default=".nwk", 
						help="When using -jd or -jt, the assumed filename extension for the tree files is\n"
						"\".nwk\". If your files are named differently you may specify a different file\n"
						"extension here. This is useful if you used IQ-TREE to generate your trees as the\n"
						"output Newick trees are in files with the extension \".treefile\". Note that this\n"
						"changes only the end of the expected filename pattern. The beginning of the\n"
						"filename must still match this reg. exp: \"tree-\d+\". For more control over the\n"
						"filenames, you will need to use other options." 
						" [.nwk]\n \n")
	input_group.add_argument("-f", "--jackknife-tree-fofn", dest="jack_tree_fofn", metavar="path/to/trees.tsv", action="store", nargs=1, type=str, required=False, default=None, 
						help="Instead of using -d, -t, and -e to provide the jackknifed trees, you may use this\n"
						"option to provide a list of filenames. The file must be in tab-separated value\n"
						"(tsv) format. Exactly two columns must exist on every line. No header/title line\n"
						"should exist. The first column should contain the taxon name (case-sensitive!).\n"
						"The second column should contain the path (absolute -or- relative to the\n"
						"directory from which the program is being run) to a jackknifed tree file in\n"
						"Newick format. This option overrides -d, -t, and -e for the jackknife tree files.\n"
						"The following is an example of how the file should look:\n" 
						"\tCignobilis\tdata/jackknife/tree/Cignobilis/tree-1.treefile\n" 
						"\t...\n" 
						"\tCignobilis\tdata/jackknife/tree/Cignobilis/tree-50.treefile\n" 
						"\tRmuscosa\tdata/jackknife/tree/Rmuscosa/tree-1.treefile\n" 
						"\t...\n" 
						"\tRmuscosa\tdata/jackknife/tree/Rmuscosa/tree-50.treefile\n" 
						"\tAglossodonta\tdata/jackknife/tree/Aglossodonta/tree-1.treefile\n" 
						"\t...\n" 
						"\tAglossodonta\tdata/jackknife/tree/Aglossodonta/tree-50.treefile\n" 
						"\tOclarkiistomias\tdata/jackknife/tree/Oclarkiistomias/tree-1.treefile\n" 
						"\t...\n" 
						"\tOclarkiistomias\tdata/jackknife/tree/Oclarkiistomias/tree-50.treefile\n" 
						"\t...\n \n")

	# 	define output group options
	#		newick format
	output_group.add_argument("-n", "-on", "--output-nwk", dest="output_nwk", metavar="out.nwk", action="store", nargs=1, type=str, required=False, default="out.nwk", 
						help="The output tree in Newick format with the taxon resiliency score in a comment\n"
						"after the branch length. To replace the branch length with the taxon resiliency\n"
						"score, specify the flag -r/--replace-branch-len." 
						" [out.nwk]\n \n")
	output_group.add_argument("-r", "-rb", "--replace-branch-len", dest="replace_branch_len", action="store_true", required=False, 
						help="Specify this flag to replace the branch length with the taxon resiliency score in\n" 
						"the output Newick tree.\n \n")
	#		json format
	output_group.add_argument("-j", "-oj", "--output-json", dest="output_json", metavar="out.json", action="store", nargs=1, type=str, required=False, default="out.json", 
						help="The output tree in json format. Each node will have a label (which may be empty),\n" 
						"branch length (which may be empty), and metadata with name/value pairs. The taxon\n" 
						"resiliency score will be assigned with the name \"taxon-resiliency\"." 
						" [out.json]\n \n")
	output_group.add_argument("-p", "-op", "--output-json-pretty", dest="output_json_pretty", metavar="out_pretty.json", action="store", nargs=1, type=str, required=False, default="out_pretty.json", 
						help="The output tree in json format. Each node will have a label (which may be empty),\n" 
						"branch length (which may be empty), and metadata with name/value pairs. The taxon\n" 
						"resiliency score will be assigned with the name \"taxon-resiliency\".\n" 
						"[out_pretty.json]\n \n")

	# 	define misc. group options
	misc_group.add_argument("-c", "--cite", dest="display_citation", action="store_true", required=False,
							help="Describe how to cite this program.\n \n")
	misc_group.add_argument("-h", "--help", action="help", help="Show this help message and exit.\n \n")
	misc_group.add_argument("-l", "--license", dest="display_license", action="store_true", required=False,
							help="Display the license under which this software is released (MIT).\n \n")
	misc_group.add_argument("-v", "--version", dest="display_version", action="store_true", required=False,
							help="Display the program version and exit.\n \n")
	
	# parse the arguments
	args = parser.parse_args()

	# process arguments, as needed
	# 	display some information, quit immediately
	if args.display_citation or args.display_license or args.display_version:
		if args.display_citation:
			print("Citation:\n" 
				"Please include a link to this repository and the following citation:\n" 
				"\n" 
				"Pickett BD, Powell GS, Ridge PG, Bybee SM. Paper title. _journal_. Year.\n" 
				"\tVolume(Issue):pages.\n", 
				file=sys.stdout)
		if args.display_license:
			print("License:\n" 
				f"Copyright (c) {__copyright_year__} {__copyright_owner__}\n" 
				"\n" 
				"All rights reserved. Written permission is required before any\n" 
				"portion of this project may be used.\n" 
				"\n" 
				"This work will likely be released under an MIT license in the\n" 
				"future. If that occurs, the license will likely look like this:\n" 
				"\n" 
				"=================================================================\n" 
				"Permission is hereby granted, free of charge, to any person\n" 
				"obtaining a copy of this software and associated documentation\n" 
				"files (the \"Software\"), to deal in the Software without\n" 
				"restriction, including without limitation the rights to use,\n" 
				"copy, modify, merge, publish, distribute, sublicense, and/or sell\n" 
				"copies of the Software, and to permit persons to whom the\n" 
				"Software is furnished to do so, subject to the following\n" 
				"conditions:\n" 
				"\n" 
				"The above copyright notice and this permission notice shall be\n" 
				"included in all copies or substantial portions of the Software.\n" 
				"\n" 
				"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND,\n" 
				"EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES\n" 
				"OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\n" 
				"NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT\n" 
				"HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,\n" 
				"WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\n" 
				"FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR\n" 
				"THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n" 
				"=================================================================\n", 
				file=sys.stdout)
		if args.display_version:
			print(f"Version: {__version__}\n", file=sys.stdout)
		sys.exit(0)
	
	#	mutually exclusive input options


	# return the parsed arguments object
	return args

# ----------- CLASSES ---------------------------- ||
# None

# ------------- MAIN ----------------------------- ||
if __name__ == "__main__":
	# handle the arguments
	args = handleArgs()
	sys.exit(0)
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
	
else:
	sys.stderr.write("ERROR: This is not a module, it is meant to run directly -- not imported!\n")
	sys.exit(1)

