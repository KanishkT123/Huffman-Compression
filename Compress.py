import sys
debug = False

d = {}
def filereader():
	'''Takes in an input file, and then outputs it's contents.'''
	if debug:
		print "Reading file"
	trial = False
	while not trial:
		filename = raw_input("Enter a file name pls and thenks: ")
		if ".txt" in filename:
			try:
				myfile = open(filename, "rb")
				contents = myfile.read()
				myfile.close()
				print "Original File: " + str(filename)
				if debug:
					print "File Reading was succesful"
				trial = True
			except:
				continue
	return [contents, filename]

def filewriter(string, name):
	if debug:
		print "Writing to a file and appending .HUFFMAN to the filename"
	name = name+ ".HUFFMAN"
	myfile = open(name, "wb")
	myfile.write(string)
	myfile.close()
	return

def uniques():
	'''Returns a set of all the unique letters of a long string or file.'''
	y = filereader()
	S = y[0]
	if debug:
		print "Finding all the unique letters using the built in set function"
	uniqueletters = (set(S))
	return [S, uniqueletters, y[1]]

def counter(S1, S2):
	'''Counts the number of occurrences of a particular letter in a long string.
	Only works for single characters, which is the intended function. Don't try to break it.'''
	mycount = 0
	for i in S2:
		if S1 == i:
			mycount += 1
	return mycount

def database(longstring, stringset):
	'''Creates a database of letter and occurrence pairs inside a list (a list of lists) 
	and orders the list in value ascending of appearances.'''
	d = []
	if debug:
		print "The database is currently being created. This is basically a list of frequencies of individual characters in the string."
	for i in stringset:
		d = d+ [[i, counter(i, longstring)]]
	d.sort(key=lambda x: int(x[1]))
	return d

def insertsort(largelist, entry):
	'''Takes two values: A list of lists, and a single list with format: [list, integer].
	Then inserts the entry list into the largelist in ascending order of integer values and returns the list'''
	if len(largelist) == 0:
		return [entry]
	for i in range(len(largelist)):
		if i+1 == len(largelist):
			largelist.append(entry)
			return largelist
		else:
			if largelist[i][1] <= entry[1] and largelist[i+1][1]>= entry[1]:
				return largelist[:i+1] + [entry] + largelist[i+1:]

def treegenmap(frequencies):
	'''Generates a huff tree in the form of a list from a list of letters and frequencies given to it in order.'''
	if debug:
		print "The huffman tree is being generated atm. This means that an insertion sort and list splicing and appending are both working properly."
	p = []
	for value in frequencies:
		p.append(value)
	while len(p)>1:
		l = p[0]
		r = p[1]
		p = p[2:]
		node = [l,r]
		newinsert = [node, l[1]+r[1]]
		p = insertsort(p, newinsert)
	return p[0]

def cleanup(tree):
	'''Takes a huffman tree and returns only the letter values, without any of the frequencies.'''
	if len(tree) == 1:
		return tree[0]
	if len(tree) == 2 and type(tree[1]) is int:
		return cleanup(tree[0])
	if len(tree) == 2 and type(tree[1]) is list:
		return [cleanup(tree[0])] + [cleanup(tree[1])]


def treewalker(tree, counter):
	'''Takes a base huffman tree and a compression counter and returns a dictionary of letter and compression pairs.'''
	if debug:
		print "If you got here, that means that the tree cleanup function which eliminates all the frequencies from the huffman tree was succesful"
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


def compress(longstring):
	'''Takes a long string and compresses it using the global dictionary.'''
	if debug:
		print "The dictionary is apparently functional and hasn't been tampered with. The compression is taking placing using a loop and the global dictionary"
	newstring = ''
	for i in longstring:
		newstring = newstring + d[i]
	thereturn = newstring
	otherstring = ''
	max8 = len(newstring)/8
	while len(newstring) >= 8:
		otherstring += str(chr(int(newstring[:8],2)))
		newstring = newstring[8:]
	otherstring +=  chr(int(newstring,2))
	return [thereturn, otherstring]


def dictionaryadder(hufftree, huffstring):
	"""Adds the dictionary to the start of the compressed string."""
	y = str(len(huffstring[0])) + '   ' + str(hufftree)
	newhuff = y + '   ' + huffstring[1]
	if debug:
		print "The compression worked (did not crash.) The dictionary was added to the start of the huffman string, with three spaces between the dictionary and the compressed string."
	return newhuff

def main():
	"""Main function that runs the program."""
	inside = uniques()
	print "Unique Characters: " + str(len(inside[1]))
	print "Total Bytes: " + str(sys.getsizeof(inside[0]))
	dataset = database(inside[0], inside[1])
	hufftree = cleanup(treegenmap(dataset))
	treewalker(hufftree, '')
	huffedup = compress(inside[0])
	filesize = 0
	if len(huffedup[0])%8 > 0:
		filesize = len(huffedup[0])/8 + 1
	else:
		filesize = len(huffedup[0])/8
	dictsize = 0
	if len(str(hufftree))%8 > 0:
		dictsize = len(str(hufftree))/8 + 1
	else:
		dictsize = len(str(hufftree))/8
	huffedup = dictionaryadder(hufftree, huffedup)
	filewriter(huffedup, inside[2])
	print "Compresed filename: " + inside[2] + '.HUFFMAN'
	print "Compressed text length in bytes: " + str(filesize)
	print "Dictionary Overhead: " + str(dictsize)
	print "Total Compressed filesize: " + str(dictsize + filesize)
	print "Actual Compression Ratio: " + str(float(dictsize+filesize)/float(sys.getsizeof(inside[0])))
	print "Asymptotic Ratio: " + str(float(filesize)/float(sys.getsizeof(inside[0])))
	if debug:
		print "This is the global dictionary that was created."
		print d


if __name__ == "__main__":
    main() 
