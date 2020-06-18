#! /bin/env python3

__author__ = "Brandon Pickett"

# ----------- IMPORTS ---------------------------- ||
import sys
from node import Node,MalformedNewickTree

# ---------- FUNCTIONS --------------------------- ||

# ----------- CLASSES ---------------------------- ||
class Tree:
	
	# class level variables (define once, not for every instance of the class)
	# for example:
	# PI = 3.14
	#NEWICK_PUNCT = ":;,()"

	# constructor(s)
	def __init__(self, newick="", name=""):
		# "normal" "public" member fields
		self.root = Node()
		self.name = name

		self.__initializeNodes__(newick)

	# "normal" "public" member functions
	def getLeafLabels(self):
		return self.root.getLeafLabels()

	def getNewick(self):
		return self.root.getNewick() + ";\n"

	def getJson(self):
		return '{"name":"' + self.name + '","root":' + self.root.getJson() + '}'
	
	def getPrettyJson(self):
		#return json.loads(self.getJson())
		return '{\n\t"name": "' + self.name + '",\n\t"root":\n' + self.root.getPrettyJson(indent=2) + '\n}\n'

	# "private" member functions
	def __initializeNodes__(self, newick):
		newick = self.__removeNewickComments__(newick).rstrip()
		index = self.root.initializeNode(newick)

		if index < len(newick):
			if newick[index] == ';':
				index += 1
				newick = newick[index:]
				if newick and not newick.isspace():
					raise MalformedNewickTree(f"Reached end of tree and found semi-colon, but found 1 or more non-space characters after semi-colon.")
			else:
				raise MalformedNewickTree(f"Reached end of tree and expected a semi-colon, but found {newick[index]} instead.")
		else:
			raise MalformedNewickTree("Reached end of tree without encountering a semi-colon")

	def __removeNewickComments__(self, newick):
		keep = ""
		i = 0
		while i < len(newick):
			if newick[i] == "[":
				found_r_bracket = False
				while i < len(newick):
					if newick[i] == ']':
						found_r_bracket = True
						break
					i += 1

				if not found_r_bracket:
					raise MalformedNewickTree("comment had no ending ']'")

				i += 1 # go to char after ']' (or if at len already, it won't matter that its past len)

			elif newick[i] == '"' or newick[i] == "'":
				# this section allows for '[' and ']' inside quoted labels
				found_end_quote = False
				q = newick[i]
				keep += q
				i += 1 # go to char after opening quote
				while i < len(newick):
					keep += newick[i]
					if newick[i] == q:
						found_end_quote = True
						break
					i += 1

				if not found_end_quote:
					raise MalformedNewickTree(f"quoted label had no ending quote ({q})")

				i += 1 # go to char after end quote (or if at len already, it won't matter that its past len)
			else:
				keep += newick[i]
				i += 1
		return keep

	# comparison operators
	#def __lt__(self, other):
	#	return self.root.__lt__(other)
	
	# make str(some_node) meaningful
	def __str__(self):
		return f'{{ name: "{self.header}", root: {str(self.root)} }}'
	
	# make print(some_node) meaningful
	def __repr__(self):
		return "Tree: " + self.__str__()
	

# ------------- MAIN ----------------------------- ||
if __name__ == "__main__":
	sys.stderr.write("ERROR: This is a module, it is meant to be imported -- not run directly!\n")
	sys.exit(1)

