import openpyxl
import os
import sys

from compare import Segment, Word, Language, LanguageFamily

"""code for reading a structured excel file"""

def readAlignedFile(filename):
	"""return aligned language family object"""
	"""assumes that the file is structured properly"""
	wb = openpyxl.load_workbook(filename, read_only=True)
	print(wb.get_sheet_names())	
	meanings = wb.get_sheet_names()
	firstsheet = wb.get_sheet_by_name(meanings[0])
	numlangs = firstsheet.max_row-1
	languagenames = [x[0].value for x in firstsheet['A2':'A{}'.format(numlangs+1)]]
	languages = LanguageFamily()
	llist = []
	for i in range(len(languagenames)):
		llist.append(Language(languagenames[i]))
		for j in range(len(meanings)):
			word = []
			for k in range(2, len(wb[j].columns())+1):
				word.append(wb[j].cell(row=i+2, col=k).value)
			llist[i].addAlignedWord(word, meanings[j])
	for lang in llist:
		langugages.addLanguage(lang)
	print(dir(languages))
		
	


if __name__=="__main__":
	readAlignedFile(sys.argv[1])	
	x = Segment("p")
	print(x)
