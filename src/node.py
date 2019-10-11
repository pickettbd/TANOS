#! /bin/env python3

__author__ = "Brandon Pickett"

# ----------- IMPORTS ---------------------------- ||
import sys

# ---------- FUNCTIONS --------------------------- ||

# ----------- CLASSES ---------------------------- ||
class MalformedNewickTree(Exception):
	pass

class Node:
	
	# class level variables (define once, not for every instance of the class)
	# for example:
	# PI = 3.14

	# constructor(s)
	def __init__(self):
		# "normal" "public" member fields

		# 	children: immediate children Nodes
		self.children = []
		#	label: used to store a taxon name for leaf Nodes or clade name for internal nodes
		self.label = ""
		#	metadata: Here we enable the storage
		#	of multiple name value pairs.
		#	The values can be numbers or strings.
		#	To get the standard branch length, simply use
		#	self.metadata["branch_length"].
		self.metadata = {}
		#if kwargs is not None:
		#	for k,v in kwargs.iteritems():
		#		self.metadata[str(k)] = str(v)


		# "private" member fields
		##	__subtree_leaf_names: # used to store all taxa names in this part of the tree
		#self.__subtree_leaf_names = []
		##	__subtree_leaf_scores: # used to store the percentage of jackknifed trees that
		##	had the clade of __subtree_leaf_names omitting the element at the parallel
		##	position in __subtree_leaf_scores
		#self.__subtree_leaf_scores = []
	
	def initializeNode(self, newick, index=0):
		# 1- conceptual str.lstrip() beginning at position index 
		index = self.__consumeNewickWhitespace__(newick, index=index)

		# 2- process children (recursively if neeeded)
		while index < len(newick) and ( newick[index] == '(' or newick[index] == ',' ):
			index += 1 # get past the recursive signal (left paren or comma)
			self.children.append(Node())
			index = self.children[-1].initializeNode(newick, index=index)
			index = self.__consumeNewickWhitespace__(newick, index=index)

		# 3- process label (quote or unquoted)
		if index < len(newick):
			if newick[index] == '"' or newick[index] == "'":
				# quoted label present
				self.label, index = self.__getQuotedNewickLabel__(newick, index)
				index = self.__consumeNewickWhitespace__(newick, index=index)
			elif not newick[index] in "),:;":
				# unquoted label present
				self.label, index = self.__getUnquotedNewickLabel__(newick, index)
				index = self.__consumeNewickWhitespace__(newick, index=index)
		else:
			raise MalformedNewickTree("Reached end of tree (while about to process a potential label) without encountering a semi-colon")

		# 4- process branch length
		if index < len(newick):
			index = self.__getFromNewickAndPossiblySetBranchLength__(newick, index)

		else:
			raise MalformedNewickTree("Reached end of tree (while about to process a potential branch length) without encountering a semi-colon")

		# 5- process end of node (possibly of entire tree)
		if index < len(newick):
			if newick[index] == ')':
				index += 1 # get past the )
				return index # position of char after )

			elif newick[index] == ',' or newick[index] == ';':
				return index # position of comma or semi-colon

			else:
				raise MalformedNewickTree("Reached what should have been the end of a node (and possibly the entire tree), but found a character other than a right paren, comma, or semi-colon")
					
		else:
			raise MalformedNewickTree("Reached end of tree (while expecting either a right paren, comma, or semi-colon) without encountering a semi-colon")

	def __consumeNewickWhitespace__(self, newick, index=0):
		while index < len(newick) and newick[index].isspace():
			index += 1
		return index

	def __getQuotedNewickLabel__(self, newick, index=0):
		if ( len(newick) - index ) > 1:
			if newick[index] == '"' or newick[index] == "'":
				starting_index = index # deep copy
				q = newick[index]
				index += 1 # get past opening quote
				while index < len(newick):
					if newick[index] == q:
						index + 1 # get past closing quote
						return newick[starting_index:index], index
					index += 1

				raise MalformedNewickTree("quoted label had no closing quote")
			else:
				raise MalformedNewickTree("attempted to extract the end position of a quoted label from a newick string, but the starting position provided was not a quote")
		else:
			raise MalformedNewickTree("attempted to extract a the end position of a quoted label, but the newick string had <2 characters remaining")

	def __getUnquotedNewickLabel__(self, newick, index=0):
		starting_index = index # deep copy
		index += 1 # get past first label character (which is already validated)
		while index < len(newick) and not ( newick[index].isspace() or newick[index] in "),:;" ):
			index += 1
		return newick[starting_index:index], index
	
	def __getFromNewickAndPossiblySetBranchLength__(self, newick, index=0):
		if newick[index] == ':':
			# branch length present
			i += 1 # get past the ':'
			index = self.__consumeNewickWhitespace__(newick, index=index)
			if index < len(newick):
				branch_length_str = ''
				while index < len(newick) and not ( newick[index].isspace() or newick[index] in '),;' ):
					branch_lenth_str += newick[index]
					index += 1
				# index is either past end (we didn't find a semi-colon),
				# or it is a right paren, comma, semi-colon, or space
				if index < len(newick):
					try:
						branch_length = float(branch_length_str) if '.' in branch_length_str else int(branch_length_str)
						self.metadata["branch_length"] = branch_length
					except ValueError:
						raise MalformedNewickTree(f"Found branch length ({branch_length_str}), but it was not an int or a float.")
				else:
					raise MalformedNewickTree(f"Found branch length ({branch_length_str}) after ':', but reached end of tree without encountering a semi-colon")
			else:
				raise MalformedNewickTree("Expected branch length after ':', but found nothing.")

			# index is either a right paren, comma, semi-colon, or space
			# now let's skip past spaces to ensure it is one of the other three
			index = self.__consumeNewickWhitespace__(newick, index=index)

		return index

	# comparison operators
	#def __lt__(self, other):
	#	return False
	
	# "normal" "public" member functions
	def getNewick(self):
		# TODO

	def getJson(self):
		# TODO
	
	# make str(some_node) meaningful
	def __str__(self):
		return f'\{ label: "{self.label}", metadata: {str(self.metadata)}, children: {len(children)} \}'
	
	# make print(some_node) meaningful
	def __repr__(self):
		return "Node: " + self.__str__()
	

# ------------- MAIN ----------------------------- ||
if __name__ == "__main__":
	sys.stderr.write("ERROR: This is a module, it is meant to be imported -- not run directly!\n")
	sys.exit(1)

