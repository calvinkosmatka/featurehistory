
class Distance(object):
	"""Abstract class for objects where pairwise distance can be computed"""
	def d(self, other):
		"""A well defined metric
			1. d(x,y)==0 <=> x==y
			2. d(x,y)>=0 forall x, y
			3. d(x,y) + d(y,z)>=d(x,z) forall x,y,z
		"""
		return 0


class Character(Distance):
	def __init__(self, char):
		self._char = char
	def d(self, other):
		if self._char == other._char:
			return 0
		return 1

class Sequence(Distance):
	def __init__(self, string, chartype):
		self._seq = [chartype(x) for x in string]
		self.string = string
		self.chartype = chartype
	def d(self, other):
		s = 0
		for (c1, c2) in Align(self, other):
			s += c1.d(c2)
		return s
	def __repr__(self):
		return str(self._seq)

class Align(Distance):
	"""An object representing an aligned pair of sequences"""
	def __init__(self, seq1, seq2):
		self._s1 = seq1
		self._s2 = seq2
		self._alignedsequence = self.align(self._s1, self._s2)
	def __contains__(self, x):
		return x in self._alignedsequence
	def align(self, s1, s2):
		"""Implement smith-waterman here"""
		
		return zip(s1, s2)
