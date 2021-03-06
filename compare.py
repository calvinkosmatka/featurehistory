from sequence import Distance, Character, Sequence, Align
import unicodedata
from tabulate import tabulate
from functools import reduce
import math
from Bio import Phylo
from Bio.Phylo import TreeConstruction

class Segment(Character):
	"""Order of features:
		syllabic,
		consonantal,
		sonorant,
		anterior
		coronal
		back
		high
		low
		nasal
		voice
		cont
		round
		strident
		lateral
		del. rel.
		ATR
		spr gl
		constr gl
		distributed
	"""
	features = [
	'syllabic',
	'consonantal',
	'sonorant',
	'anterior',
	'coronal',
	'back',
	'high',
	'low',
	'nasal',
	'voice',
	'continuant',
	'round',
	'strident',
	'lateral',
	'delayed release',
	'ATR',
	'spead gl',
	'constricted gl',
	'distributed'
	]
	featuredict = {
	#     scsacbhlnvcrsldascd
	"p": "0101000000000000000",
	"t": "0101100000000000000",
	"k": "0100011000000000000",
	"b": "0101000001000000000",
	"d": "0101100001000000000",
	"g": "0100011001000000000",
	"m": 1,
	"n": "0111100011000000000",
	"ŋ": "0110011011000000000",
	"ŋ̩": "0110011011000000000",
	"ʔ": "0000000000000000000",
	"h": "0000000000100000000",
	"s": "0101100000101000000",
	"z": "0101100001101000000",
	"ʃ": "0100101000101000000",
	"f": 1,
	"v": 1,
	"x": "0100011000100000000",
	"ɣ": "0100011001100000000",
	"j": "0010101001100000000",
	"r": "0111100001100000000",
	"ʁ": "0100010001100000000",
	"ʁ̞": "0110010001100000000",
	"ɹ": "0111100001100000000",
	"χ": "0100010000100000000",
	"ɾ": "0111100001100000000",
	"θ": "0101100000100000000",
	"tʰ":"0101100000000000100",
	"ʰt":"0101100000000000100",
	"ç": "0100101000101000000",
	"ç": "0100101000101000000", 
	"k̟ʰ":"0100011000000001100",
	"kʰ":"0100011000000000100",
	"w": "0010011001110000000",
	"l": "0111100001100100000",
	" ": "-------------------"	
	}
	AIdimensions = [
	'son',
	'cons',
	'GW',
	'GT',
	'LH',
	'TR',
	'SP',
	'TH',
	'TT',
	'TC',
	'TG',
	'L',
	'A'
	]
	"""	0 means unspecified
		1 neutral
		2 high on AI chart
		3 low on AI
	"""
	AIfeaturedict = {
	#     scwtltshtcgla
	"p": "0101000000000000000",
	"t": "0101100000000000000",
	"k": "0100011000000000000",
	"b": "0101000001000000000",
	"d": "0101100001000000000",
	"g": "0100011001000000000",
	"m": 1,
	"n": "0111100011000000000",
	"ŋ": "0110011011000000000",
	"ŋ̩": "0110011011000000000",
	"ʔ": "0000000000000000000",
	"h": "0000000000100000000",
	"s": "0101100000101000000",
	"z": "0101100001101000000",
	"ʃ": "0100101000101000000",
	"f": 1,
	"v": 1,
	"x": "0100011000100000000",
	"ɣ": "0100011001100000000",
	"j": "0010101001100000000",
	"r": "0111100001100000000",
	"ʁ": "0100010001100000000",
	"ʁ̞": "0110010001100000000",
	"ɹ": "0111100001100000000",
	"χ": "0100010000100000000",
	"ɾ": "0111100001100000000",
	"θ": "0101100000100000000",
	"tʰ":"0101100000000000100",
	"ʰt":"0101100000000000100",
	"ç": "0100101000101000000",
	"ç": "0100101000101000000", 
	"k̟ʰ":"0100011000000001100",
	"kʰ":"0100011000000000100",
	"w": "0010011001110000000",
	"l": "0111100001100100000",
	" ": "-------------------"	
	}
	def d(self, other):
		return 0
	def __repr__(self):
		string = ""
		string += "/{}/\n".format(self._char)
		for i in range(len(Segment.features)):
			string += "["+("-" if Segment.featuredict[self._char][i]=="0" else "+")+Segment.features[i]+"]\n"
		return string
	def getBinary(self):
		print(self._char)
		return Segment.featuredict[self._char]	

class Word(Sequence):
	def __init__(self, segments, meaning):
		for i in range(len(segments)):
			if segments[i]==None:
				segments[i]=" "
		super().__init__(segments, Segment)
		self.meaning = meaning
	def setCognacyClass(self, c):
		self._cognacyclass = c
	def getCognacyClass(self):
		return self._cognacyclass
	def __repr__(self):
		return "".join(self.string)+" : "+self.meaning	
	def getBinary(self):
		string = ""
		for s in self._seq:
			string += s.getBinary()
		return string
		# "".join([s.getBinary() for s in self._seq])	
class Language:
	"""contains words and meanings"""
	def __init__(self, name):
		self.words = []
		self.name = name
	def addAlignedWord(self, seq, meaning):
		#TODO distinguish between non-aligned and aligned words
		# Should only be thought about after I have alignment algorithm
		self.words.append(Word(seq, meaning))
		
		#rebuild list of phones every time we add a word
		self.phones = list(set([ word.string[i] for word in self.words for i in range(len(word.string))]))
		
	def buildCorrespondenceMatrix(self, otherlang):
		matrix = [[0 for p in otherlang.phones] for q in self.phones]
		for i in range(len(self.words)):
			for j in range(len(self.words[i].string)):
			#implicit assumption that the words have the same length
				s1 = self.words[i].string[j]
				s2 = otherlang.words[i].string[j]
				matrix[self.phones.index(s1)][otherlang.phones.index(s2)] += 1
		return matrix
	def correspondenceProbability(self, otherlang):
		scm = self.buildCorrespondenceMatrix(otherlang)
		# ignore insertions/deletions for calculating distance
		ignoreInsertions = False 
		ignoreDeletions = False 
		if ignoreInsertions:
			scm.pop(self.phones.index(" "))
		if ignoreDeletions:
			j = otherlang.phones.index(" ")
			for i in range(len(scm)):
				scm[i].pop(j)
		return correspondenceProbability(scm, "hypergeometric")
	def d(self, otherlang):
		return -math.log(self.correspondenceProbability(otherlang))
def correspondenceProbability(matrix, dist="binomial"):
	prod = 1
	for row in matrix:
		if sum(row)>0:
			if dist=="binomial":
				l = [(x/sum(row))**x for x in row]
				v = reduce(lambda x,y: x*y, l)
				prod *= v
			if dist=="hypergeometric":
				l = [math.factorial(x) for x in row]
				v = reduce(lambda x,y: x*y, l)
				v = v/math.factorial(sum(row))
				prod *= v
	return prod

class LanguageFamily:
	"""contains languages with words matching meanings"""
	def __init__(self):
		self.languages = []
	def addLanguage(self, lang):
		if isinstance(lang, Language):
			self.languages.append(lang)
		if isinstance(lang, str):
			self.languages.append(Language(lang))
	def setMeanings(self, meanings):
		self.meanings = meanings
	def getMeanings(self):
		return self.meanings
	def __repr__(self):
		headers = ["Language", *self.meanings]
		rows = []
		for l in self.languages:
			r = [l.name]
			for word in l.words:
				r.append("".join(word.string))
			rows.append(r)
		return tabulate(rows, headers=headers)
	def writeNexusStub(self, fil):
		"""
		fil is a uri pointing to the desired output file
		clears file before writing
		"""
		f = open(fil, "w")
		numchars = 0 #fix this
		f.write("ntaxa = {0}, nchar = {1}\n".format(len(self.languages), numchars)) 
		for lang in self.languages:
			f.write(lang.name + "\t\t")
			for word in lang.words:
				f.write(word.getBinary())
			f.write("\n")
		f.close()
	def distanceMatrix(self):
		matrix = [[0 for _ in self.languages] for _ in self.languages]
		for i in range(len(self.languages)):
			for j in range(len(self.languages)):
				if i!=j:
					matrix[i][j] = self.languages[i].d(self.languages[j])
		return matrix
	def UPGMA(self, f=min):
		"""builds a tree via UPGMA, and uses the passed in function to deal with asymmetric 'distances'"""
		m = self.distanceMatrix()
		for i in range(len(self.languages)):
			for j in range(i, len(self.languages)):
				m[i][j] = f(m[i][j],m[j][i])
				m[j][i] = m[i][j]
		predm = [[m[i][j] for j in range(i+1)] for i in range(len(self.languages))]
	#	print(predm)
		dm = TreeConstruction._DistanceMatrix([l.name for l in self.languages], predm)
		constructor = TreeConstruction.DistanceTreeConstructor(method='upgma')
		upgmatree = constructor.upgma(dm)
		Phylo.draw_ascii(upgmatree)
	#	indices = range(len(self.languages))
	#	while len(indices)>1:
	#		#find minimum distance in m
	#	
	#		#join indices as  tuple
	#		#recalculate m
			
		return m
	def NJ(self, f=min):
		m = self.distanceMatrix()
		for i in range(len(self.languages)):
			for j in range(i, len(self.languages)):
				m[i][j] = f(m[i][j],m[j][i])
				m[j][i] = m[i][j]
		predm = [[m[i][j] for j in range(i+1)] for i in range(len(self.languages))]
	#	print(predm)
		dm = TreeConstruction._DistanceMatrix([l.name for l in self.languages], predm)
		constructor = TreeConstruction.DistanceTreeConstructor(method='nj')
		njtree = constructor.nj(dm)
		Phylo.draw_ascii(njtree)

