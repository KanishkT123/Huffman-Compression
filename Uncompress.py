def treewalker(tree, counter):
	'''Takes a base huffman tree and a compression counter and returns a dictionary of letter and compression pairs.'''
	if debug:
		print "Generating a dictionary from the given huffman tree list"
	if len(tree) == 0:
		return
	if len(tree) == 1:
		if type(tree[0]) is list:
			treewalker(tree[0], counter)
		if type(tree[0]) is str:
			d[tree[0]] = counter
	elif type(tree[0]) is str:
		d[tree[0]] = counter+'0'
		treewalker(tree[1], counter+'1')
	elif type(tree[0]) is list:
		 treewalker(tree[0], counter+'0') 
		 treewalker(tree[1], counter+'1')

def filereader():
	'''Takes in an input file, and then outputs it's contents.'''
	if debug:
		print "About to take in an input file and try to decode it."
	trial = False
	while not trial:
		filename = raw_input("Enter a file name pls and thenks: ")
		if ".HUFFMAN" in filename:
			try:
				myfile = open(filename, "rb")
				contents = myfile.read()
				myfile.close()
				print "Original File: " + str(filename)
				if debug:
					print "Input operation was succesful"
				trial = True
			except:
				print "You haven't given me the right name!!"
				continue
	return [contents, filename]

def filewriter(string, name):
	"""Takes a string and a filename, and writes the string to a .DECODED file type."""
	if debug:
		print "About to try to write the file to be originalfile.HUFFMAN.DECODED"
	name = name+ ".DECODED"
	print "File written to file named: " + str(name)
	myfile = open(name, "wb")
	myfile.write(string)
	myfile.close()
	return

def spacefinder(string):
	'''Finds the first space in a compressed string (essentially the break where the huffman tree and the compressed string break off)
	Then evaluates everything before that first space (should ideally be a list added in via the compress function'''
	x = string.index('   ')
	tree = eval(string[:x])
	#I don't like using eval. If I could import ast, I would use ast.literal_eval. //TODO: FIX THIS, MAKE IT SECURE.
	return tree

d = {}
#Global variables, much like the devil, are useful once you sell your soul. 

def dictionaryreversal():
	'''Reverses the key value pairs of a given dictionary. Used in order to effectively uncompress the huffman compressed string.'''
	dictb = {}
	for element in d:
	  dictb[d[element]] = element
	return dictb


def finder(dict, string):
	"""Finds the character translation of an uncompressed string by looking for it in a dictionary. If it isn't there, then it just increments the string by one."""
	counter = 0
	newstring = ''
	counter = 0
	newstring = ''
	startpoint = string.index('   ')+3
	string = string[startpoint:]
	while len(string) != 0:
		try:
			newstring += dict[string[:counter]]
			string = string[counter:]
			counter = 0
		except:
			counter = counter + 1
	return newstring

def main():
	S = filereader()
	if debug:
		print S[0 ]
	hufftree = spacefinder(S[0])
	if debug:
		print hufftree
	treewalker(hufftree, '')
	if debug:
		print d
	newdict = dictionaryreversal()
	if debug:
		print newdict
	newstring = finder(newdict, S[0])
	if debug:
		print newstring
	filewriter(newstring, S[1])


if __name__ == "__main__":
    main() 
