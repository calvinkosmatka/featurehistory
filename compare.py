from sequence import Distance, Character, Sequence, Align
import unicodedata

class Segment(Character):
	"""Order of features:
		syllabic,
		consonantal,
		sonorant,
		continuant,
		delayed release,
		strident,
		distributed,
		lateral,
		anterior,
		coronal,
		nasal,
		voice,
		aspirated,
		glottal,
		high,
		low,
		back,
		round,
		ATR
	"""
	featuredict = {
	"p": "001010101"
	"t": "001010100"
	"k": "101001010"
	"b": "101111110"
	"d": 1
	"g": 1
	"m": 1
	"n": 1
	"ŋ": 1
	"ʔ": 1
	"s": 1
	"z": 1 
	"f": 1
	"v": 1
	
	}
	def d(self, other):
		return 0

class Word(Sequence):
	def __init__(self, word):
		super().__init__(self, unicodedata.normalize('NFD',word), Segment)

	



