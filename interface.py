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
			for i in range(len(self.languagefamily.languages)):
				print(str(i) + ") " + self.languagefamily.languages[i].name)
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
	def do_correspondence(self, arg):
		args = arg.split(" ")
		print(args)
		l1 = self.languagefamily.languages[int(args[0])]
		l2 = self.languagefamily.languages[int(args[1])]
		scm = l1.buildCorrespondenceMatrix(l2)
		print("Correspondence matrix for " + l1.name + "->" + l2.name)
		print("p(" + l1.name + "," + l2.name + ") = " + str(l1.correspondenceProbability(l2)))
		print("d(" + l1.name + "," + l2.name + ") = " + str(l1.d(l2)))
		print("  \t" + "  ".join(l2.phones))
		for i in range(len(scm)):
			print(l1.phones[i] + "\t" + str(scm[i]))
	def do_quit(self, arg):
		return True

if __name__=="__main__":
	CompareSuite().cmdloop()
