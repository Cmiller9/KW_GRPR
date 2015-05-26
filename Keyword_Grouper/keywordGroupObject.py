#THIS IS THE KEYWORD GROUPER OBJECT IT WILL STORE A LIST OF KEYWORDS FROM A TXT FILE
#ITS INTERNAL METHODS WILL CREATE THE KEYWORD GROUPED LIST OUTPUT (TXT FORM AS WELL)

#Import defaultdict to give dictionaries used default values
from collections import defaultdict

import csv

#DEFINING THE OBJECT AS WORD_GROUPER WHICH WILL BE IMPORTED BY THE GROUPER SCRIPT
class word_grouper(object):

#Initialize the variables for the object which include the in and out file as well
#as a slew of helper arrays for grouping	
	exception_list = ["i","and","the","is","what", "with", "with the"
                      "a","what is", "is the", "and the", "and is"] #List of phrases and words to not track

	def __init__(self,in_file,out_file, word_count = 3, granularity = 4):
		self.in_file = in_file
		self.out_file = out_file
		self.word_count = word_count # max numbers of words that can make up a keyword 
		self.granularity = granularity # abs(kw group - largest kw group) <= granularity
		self.input_keywords = [] #Keywords read from text file
		self.words_to_group = [] #Helper array for what words to group in kw lists
		self.word_frequencies = defaultdict(lambda: 0) #Frequency of keyword - 
		#appearances in original list
		self.keyword_groups = defaultdict(lambda: []) #The grouped keywords - 
		#Dict of keys with value lists
		self.gui_wordlist = []

#AFTER SETTING INITIAL VALUES NEXT IS A LIST OF FUNCTIONS THAT WILL BE USED TO
#GATHER INPUT KEYWORDS AND GROUP THEM INTO lists

	#Clears all data --- complete refresh
	def refresh(self):
		self.input_keywords = []
		self.words_to_group = [] 
		self.word_frequencies = defaultdict(lambda: 0)
		self.keyword_groups = defaultdict(lambda: [])
		self.gui_wordlist = []

	#Clears the frequency and words to group data so new keywords can be added
	#without messing up existing keyword groups
	def renew(self):
		self.words_to_group = []
		self.word_frequencies = defaultdict(lambda: 0)

	#Write the final keyword groups to a csv file
	def write_to_csv(self,path="keywordCSV.csv"):
		with open(path, "wb") as outfile:
			w = csv.writer(outfile)
			w.writerow(self.keyword_groups.keys())
			vals = self.keyword_groups.values()
			rows = map(None, *vals)
			for row in rows:
				w.writerow(row)

	#Write the final keyword groups to the specified outfile -
	#iterate through the keyword_groups dict and print each key and value
	def write_to_file(self):
		fil = open(self.out_file,"w")
		for key in self.keyword_groups:
			self.keyword_groups[key] = set(self.keyword_groups[key])
			fil.write("------------- \n")
			fil.write(key+"\n")
			fil.write("------------- \n")
			for value in self.keyword_groups[key]:
				kwords = value
				fil.write(value+"\n")
		fil.close()
	
	#Make the keyword groups by taking the most frequent mentioned words and -
	#adding all their mentions under their dict entry
	def make_keywords(self):
		for _ in xrange(len(self.input_keywords)):
			current_keyword = self.input_keywords.pop().strip().split(" ")
			phrase = " ".join(current_keyword)
			for x in self.words_to_group:
				y = x[0]
				if y in current_keyword:
					self.keyword_groups[y].append(" ".join(current_keyword))
				elif y in phrase:
					self.keyword_groups[y].append(" ".join(current_keyword))

	#Find the top words to make into keyword groups by iterating through the top
	#word mentions - choosing the most mentioned and those mentioned 2 or less
	#times than the top mentioned word
	def make_groups(self):
		kw_groups = []
		max_word = max(self.word_frequencies.iterkeys(), 
			key=(lambda key: self.word_frequencies[key]))
		value = int(self.word_frequencies[max_word])
		for word in self.word_frequencies:
			if abs(self.word_frequencies[word] - value) <= self.granularity:
				kw_groups.append([word,self.word_frequencies[word]])
		kw_groups = sorted(kw_groups, key=lambda l:l[1], reverse=True)
		self.words_to_group = kw_groups

	#Get the input keywords and frequency by opening the supplied keywords text file
	#Iterating through it, adding each line to input_keywords and counting 
	#word mentions by adding to a dict value for a key of each word	
	def get_input(self):
		x = open(self.in_file,"r")
		for line in x:
			all_words = []
			self.input_keywords.append(line.lower())
			w = line.strip().split(" ")
			#Create all combinations of line of words in file
			for y in range(1,len(w)+1):
				all_words += map(list, zip(*(w[i:] for i in range(y))))
			#Count the mentions of all words found in the input_file - 
			#that are not in the exception list
			for word in all_words:
				word_word = " ".join(word)
				if word_word.lower() not in self.exception_list:
					self.word_frequencies[word_word.lower()] += 1
		x.close()

	def gui_input(self):
		for line in self.gui_wordlist:
			all_words = []
			self.input_keywords.append(line.lower())
			w = line.strip().split(" ")
			#Create combinations of line of words in file
			for y in range(1,self.word_count):
				all_words += map(list, zip(*(w[i:] for i in range(y))))
			#Count the mentions of all words found in the input_file - 
			#that are not in the exception list
			for word in all_words:
				word_word = " ".join(word)
				if word_word.lower() not in self.exception_list:
					self.word_frequencies[word_word.lower()] += 1

	#Runs through all the functions and performs them to create the keyword groups
	#that will print to the out_file
	def perform_actions(self):
		self.get_input()
		self.make_groups()
		self.make_keywords()
		self.write_to_file()




