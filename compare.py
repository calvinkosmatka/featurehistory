from sequence import Distance, Character, Sequence, Align
import unicodedata

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
	"p": "0101000000000000000",
	"t": "001010100",
	"k": "101001010",
	"b": "101111110",
	"d": 1,
	"g": 1,
	"m": 1,
	"n": 1,
	"ŋ": 1,
	"ʔ": 1,
	"s": 1,
	"z": 1,
	"f": 1,
	"v": 1
	
	}
	def d(self, other):
		return 0
	def __repr__(self):
		string = ""
		print(Segment.featuredict[self._char])
		for i in range(len(Segment.features)):
			string += "["+("-" if Segment.featuredict[self._char][i]=="0" else "+")+Segment.features[i]+"]\n"
		return string
		

class Word(Sequence):
	def __init__(self, segments, meaning):
		super().__init__(self, unicodedata.normalize('NFD',segments), Segment)
		self.meaning = meaning
	def setCognacyClass(self, c):
		self._cognacyclass = c
	def getCognacyClass(self):
		return self._cognacyclass
	
class Language:
	"""contains words and meanings"""
	def __init__(self):
		self.words = []
	def addAlignedWord(self, seq, meaning):
		self.words.append(Word(seq, meaning))

class LanguageFamily:
	"""contains languages with words matching meanings"""
	def __init__(self):
		self.languages = []
	def addLanguage(self, lang):
		if isinstance(lang, Language):
			self.languages.append(lang)
		if isinstance(lang, str):
			self.languages.append(Language

