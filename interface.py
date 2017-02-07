import cmd
from read_excel import readAlignedFile

class CompareSuite(cmd.Cmd):
	intro = "historical linguistics suite"
	prompt = "> "
	languagefamily = None
	def do_load(self, arg):
		'Load an excel file with aligned language data'
		self.languagefamily = readAlignedFile(arg)
	def do_list(self, arg):
		'List some properties of the language family'
		if arg == "languages":
			for lang in self.languagefamily.languages:
				print(lang.name)
		if arg == "meanings":
			for m in self.languagefamily.meanings:
				print(m)
	def do_write(self, arg):
		'Write active language family to file as nexus stub'
		self.languagefamily.writeNexusStub(arg)
	def do_matrix(self, arg):
		'Write out pairwise phonetic distance matrix for current lang fam'
		m = self.languagefamily.distanceMatrix()
		for x in m:
			print(x)
	def do_quit(self, arg):
		return True

if __name__=="__main__":
	CompareSuite().cmdloop()
