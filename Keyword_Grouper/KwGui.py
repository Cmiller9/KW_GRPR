#Standard Modules
from Tkinter import *
import tkFileDialog
from ScrolledText import *
from collections import defaultdict
import csv
import os

#Custom Modules
from keywordGroupObject import word_grouper
from Scraper import Suggest, Suggestions
#import Suggestions

class ImportList(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent

		#Frame for import canvas
		self.importListFrame = Frame(root, bg="gray", borderwidth=1, width=75)
		self.importListFrame.pack(fill=BOTH, expand=True, side=LEFT)

		#Canvas for list of keywords
		list1Canvas = Canvas(self.importListFrame, bg='gray', height=100, width=75)
		list1Canvas.pack(fill=BOTH, expand=True, side=TOP)

		#Scrollbar for Import List
		list1Scroll = Scrollbar(list1Canvas)
		list1Scroll.pack(side=RIGHT, fill=Y)

		#The Import list is a listbox that will take the keywords imported from file
		self.importList = Listbox(list1Canvas, relief=FLAT, selectmode="extended")
		self.importList.pack(fill=BOTH, expand=True, side=LEFT)

		#Set the scrolling for the ListBox
		self.importList.config(yscrollcommand=list1Scroll.set)
		list1Scroll.config(command=self.importList.yview)

		self.importList.bind("<BackSpace>", self.parent.del_word_key)

class Buttons(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent

		#Frame to hold buttons
		buttonFrame = Frame(parent.importListFrame, bg="#E8E8E8", relief=FLAT, borderwidth=2)
		buttonFrame.pack(fill=BOTH, side=BOTTOM, anchor=SW)

		#Construct Button Frame Grid
		buttonFrame.grid_rowconfigure(0, weight=1)
		buttonFrame.grid_rowconfigure(1, weight=1)

		buttonFrame.grid_rowconfigure(0, weight=1)
		buttonFrame.grid_rowconfigure(1, weight=1)

		button1 = Button(buttonFrame, text="Get Keywords", width=10, 
			highlightbackground='#E8E8E8',command=self.parent.parent.fill_list)
		button1.grid(row=0, column=0, sticky=NW)

		button2 = Button(buttonFrame, text="Clear List", width=10, 
			highlightbackground='#E8E8E8',command=self.parent.parent.del_list)
		button2.grid(row=0, column=1, sticky=NE)

		button3 = Button(buttonFrame, text="Delete Item", width=10, 
			highlightbackground='#E8E8E8',command=self.parent.parent.del_word)
		button3.grid(row=1, column=0)

		button4 = Button(buttonFrame, text="Process", width=10, 
			highlightbackground='#E8E8E8',command=self.parent.parent.makeGroups)
		button4.grid(row=1, column=1)


class Groups(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent

		#Frame for keyword groups
		groupFrame = Frame(root, relief=RAISED, bg="#E8E8E8")
		groupFrame.pack(fill=BOTH, expand=True, side=LEFT, padx=50, pady=50)

		groupHeader = Label(groupFrame,text='Keyword Groups', 
				font=("Helvetica",24),pady=10, bg="#E8E8E8")
		groupHeader.pack(fill=BOTH, expand = True, side=TOP)

		#Canvas for keyword groups
		groupCanvas = Canvas(groupFrame, bg='black', width=100, relief=SUNKEN)
		groupCanvas.pack(fill=BOTH, expand=True, side=TOP)

		#Scrollbar for Group List
		groupScroll = Scrollbar(groupCanvas, bg="#E8E8E8")
		groupScroll.pack(side=RIGHT, fill=Y)

		#The Group list is a listbox that will display the Keyword Group Dict
		self.groupList = Listbox(groupCanvas, bd=1, height=15, width=25, relief=SUNKEN)
		self.groupList.bind("<<ListboxSelect>>", self.parent.onselect)

		#Delete Key for Removing Keyword Groups
		self.groupList.bind("<BackSpace>", self.parent.del_group_key)

		#Double click to add keywords to selected group
		self.groupList.bind("<Double-Button-1>", self.parent.add_keyword_dc)
		self.groupList.pack(fill=BOTH, expand=True, side=LEFT)

		#Set the scrolling for the Keyword Groups
		self.groupList.config(yscrollcommand=groupScroll.set)
		groupScroll.config(command=self.groupList.yview)

		#Delete Button
		grpDel = Button(groupFrame, width=10, text="Delete Group", highlightbackground="#E8E8E8",
			command=self.parent.del_group)#command=lambda groupList=groupList: groupList.delete(ANCHOR))
		grpDel.pack(side=BOTTOM)

		#Add Group Button that creates a pop up to add a group
		grpAdd = Button(groupFrame, width=10, text="Add Group", highlightbackground='#E8E8E8',
			command=parent.group_window)
		grpAdd.pack(side=TOP)

class Keywords(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent

		klFrame = Frame(root, relief=RAISED, bg="#E8E8E8")
		klFrame.pack(fill=BOTH, expand=True, side=LEFT, padx=50, pady=50)

		#Header text for the keyword list 
		klHeader = Label(klFrame,text='Keywords', 
				font=("Helvetica",24),pady=10, bg="#E8E8E8")
		klHeader.pack(fill=BOTH, expand = True, side=TOP)

		#Canvas for keyword groups
		klCanvas = Canvas(klFrame, bg='black', width=100, relief=SUNKEN)
		klCanvas.pack(fill=BOTH, expand=True)

		#Scrollbar for Group List
		kwScroll = Scrollbar(klCanvas)
		kwScroll.pack(side=RIGHT, fill=Y)

		#The Group list is a listbox that will display the Keyword Group Dict
		self.kwList = Listbox(klCanvas, bd=1, height=15, width=25, relief=SUNKEN, selectmode="extended")
		self.kwList.bind("<BackSpace>",self.parent.del_kw_key)
		self.kwList.pack(fill=BOTH, expand=True, side=LEFT)

		#Set the scrolling for the Keyword Groups
		self.kwList.config(yscrollcommand=kwScroll.set)
		kwScroll.config(command=self.kwList.yview)

		#Delete kw Button
		kwDel = Button(klFrame, width=15, text="Delete Keyword", highlightbackground="#E8E8E8",
			command=self.parent.del_kw)#command=lambda kwList=kwList: kwList.delete(ANCHOR))
		kwDel.pack(side=BOTTOM)

		#Button to initiate popup to add keywords to group
		addKw = Button(klFrame, width=15, text="Add Keyword", highlightbackground="#E8E8E8",
			command=self.parent.keyword_window)
		addKw.pack(side=TOP)

class Add_Keywords(Frame):
	def __init__(self, parent, app):
		Frame.__init__(self, parent)
		self.parent = parent
		parent.title = "Add Keywords"
		self.app = app

		#Frame to hold keyword list text
		kwTextFrame = Frame(self.parent, bg="#E8E8E8", relief=RAISED)
		kwTextFrame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)

		#Canvas for keyword list text
		kwgroupCanvas = Canvas(kwTextFrame, bg="#E8E8E8", width=100, relief=SUNKEN)
		kwgroupCanvas.pack(fill=BOTH, expand=True)

		#Keyword list test box
		kwText = ScrolledText(kwgroupCanvas, wrap=WORD, width=25, 
			height=15, relief=SUNKEN, highlightthickness=0, bd=1, padx=1, pady=1)
		kwText.pack(fill=BOTH, side=BOTTOM, expand=True)

		#@add_wrapper
		def add_kw():
			#Find current group selected
				current_word = self.app.group_select

				#Get text from add keywords text box
				text = kwText.get('1.0', 'end-1c').splitlines()
				for line in text:
					self.app.key_group.keyword_groups[current_word].append(line)

				kwText.delete('1.0',END)
				return text

		#Add Keyword Button
		add_key = Button(kwTextFrame, width=15, text="Add Keyword(s)", 
			highlightbackground="#E8E8E8", command=add_kw)
		add_key.pack(side=BOTTOM)

class Add_Group(Frame):
	def __init__(self, parent, app):
		Frame.__init__(self, parent)
		self.parent = parent
		self.app = app

		#Frame to hold Keyword Group new Entry and new keywords text box
		addKGFrame = Frame(parent, bg="#E8E8E8", relief=RAISED)
		addKGFrame.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)

		#Label for Entry Box
		addGroupLabel = Label(addKGFrame, text="Enter New Group Name",bg="#E8E8E8")
		addGroupLabel.pack(side=TOP)

		#Entry Box for new Keyword Group
		self.addGroup = Entry(addKGFrame, width=30, relief=SUNKEN)
		self.addGroup.pack(side=TOP, fill=X, expand=True, pady=5)

		#Label for New Keywords for Group Text Box
		addKGLabel = Label(addKGFrame, text="Enter New Keywords (Optional)",bg="#E8E8E8")
		addKGLabel.pack(side=TOP, fill=X, expand=True, pady=5)

		#Canvas for Text Box to Enter New Keywords for New Group
		addKGCanvas = Canvas(addKGFrame, bg="#E8E8E8", relief=SUNKEN)
		addKGCanvas.pack(side=TOP, fill=BOTH, expand=True, pady=5)

		#Keywords for new group scrollable text box
		self.addKGText = ScrolledText(addKGCanvas, wrap=WORD, width=25, 
			height=15, relief=SUNKEN, highlightthickness=0, bd=1, padx=1, pady=1)
		self.addKGText.pack(fill=BOTH, side=TOP, expand=True)

		#Button to add new Keyword Group and Keywords
		addKGButton = Button(addKGFrame, text="Add Group", 
			width=30, highlightbackground='#E8E8E8', command=self.group_add)
		addKGButton.pack(side=TOP, fill=BOTH, expand=True)

	#Function to add the keyword group
	def group_add(self):
		newGroup = self.addGroup.get()
		if newGroup != "":
			self.app.key_group.keyword_groups[newGroup] = []

			text = self.addKGText.get('1.0', 'end-1c').splitlines()
			for line in text:
				self.app.key_group.keyword_groups[newGroup].append(line)
			self.app.Groups.groupList.delete(0, END)
			for x in self.app.key_group.keyword_groups:
				self.app.Groups.groupList.insert(END, '%s' % x)

			self.addKGText.delete('1.0', END)
			self.addGroup.delete(0, END)

class MainApplication(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.Import = ImportList(self)
		self.Buttons = Buttons(self.Import)
		self.Groups = Groups(self)
		self.Keywords = Keywords(self)
		self.parent = parent
		self.menubar = Menu(self)
		self.parent.config(bg="#E8E8E8")

	#HELPER VARIBLES AND OBJECT DECLARATIONS-----------------
		
		self.group_select = None #Keeps track of currently selected keyword group
		self.key_group = word_grouper("z","a") #Declare Keyword Group Object which does the backend work
		self.suggest_keywords = defaultdict(lambda: []) #Keep track of words for which we have already scraped Google

	#END HELPERS---------------------------------------------

		self.Import.pack(fill=BOTH, expand=True, side=LEFT)
		self.Buttons.pack(fill=BOTH, side=BOTTOM, anchor=SW)
		self.Groups.pack(fill=BOTH, expand=True, side=LEFT, padx=50, pady=50)
		self.Keywords.pack(fill=BOTH, expand=True, side=LEFT, padx=50, pady=50)

	#MENU---------------------------------------------------------

		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Import", command = self.fill_list)
		self.filemenu.add_command(label="Export", command = self.exp_file)
		self.filemenu.add_command(label="Export As CSV", command = self.exp_csv)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command = self.parent.quit)
		self.menubar.add_cascade(label="File", menu=self.filemenu)

		self.editmenu = Menu(self.menubar, tearoff=0)
		self.editmenu.add_command(label = "Split Keywords", command = self.makeGroups) #same as process button
		self.editmenu.add_command(label = "Clear Import List", command = self.del_list)
		self.editmenu.add_command(label = "Clear All", command = self.clear_all) #erase everything
		self.editmenu.add_command(label="Get Google Suggestions", 
							command = lambda: self.get_suggestions('http://google.com/complete/search?output=toolbar&q=',
							self.suggest_keywords))
		self.menubar.add_cascade(label="Edit", menu=self.editmenu)

		self.groupmenu = Menu(self.menubar, tearoff=0)
		self.groupmenu.add_command(label = "Add Keyword Group", command = self.group_window)
		self.groupmenu.add_command(label = "Delete keyword Group", command = self.del_group)
		self.groupmenu.add_separator()
		self.groupmenu.add_command(label = "Add Keyword(s)", command = self.keyword_window)
		self.groupmenu.add_command(label = "Delete Keyword(s)", command = self.del_kw)
		self.menubar.add_cascade(label="Keywords", menu=self.groupmenu)

		self.parent.config(menu=self.menubar)

	#END MENU-----------------------------------------------------

	#TOP LEVEL WINDOWS--------------------------------------------
	
	def keyword_window(self):
		self.newWindow = Toplevel()
		self.newWindow.config(bg="#E8E8E8")
		self.key_pop = Add_Keywords(self.newWindow, self)
		self.newWindow.wm_title("Add Keywords")

	def group_window(self):
		self.newWindow = Toplevel()
		self.newWindow.config(bg="#E8E8E8")
		self.key_pop = Add_Group(self.newWindow, self)
		self.newWindow.wm_title("Add Groups")

	#END TOP LEVEL WINDOWS----------------------------------------

	#IMPORT LIST BUTTON FUNCTIONS---------------------------------

	def fill_list(self):
		ftypes = [('Text files', '*.txt')]
		dlg = tkFileDialog.Open(root, filetypes = ftypes)
		fl = dlg.show()
		self.key_group.in_file = fl

		if fl != '':
			x = open(fl,"r")
			for line in x:
				self.Import.importList.insert(END, line)
				self.key_group.gui_wordlist.append("%s" % line)

	def del_word(self):
		#Get current importList selction
		selection = self.Import.importList.curselection()
		for i in range(len(selection)):
			value = self.Import.importList.get(selection[-1-i])
			self.key_group.gui_wordlist.remove(value)
			self.Import.importList.delete(selection[-1-i])

	def del_word_key(self, event):
		#Get current importList selction
		selection = self.Import.importList.curselection()
		for i in range(len(selection)):
			value = self.Import.importList.get(selection[-1-i])
			self.key_group.gui_wordlist.remove(value)
			self.Import.importList.delete(selection[-1-i])


	def del_list(self):
		self.Import.importList.delete(0, END)
		self.key_group.gui_wordlist = []

	def makeGroups(self):
		self.key_group.gui_input()
		self.key_group.make_groups()
		self.key_group.make_keywords()

		self.Groups.groupList.delete(0, END)
		for x in self.key_group.keyword_groups:
			self.Groups.groupList.insert(END, "%s" % x)
		self.Import.importList.delete(0, END)
		self.key_group.renew()

	#END IMPORT LIST BUTTON FUNCTIONS---------------------------------

	#MENU FUNCTIONS---------------------------------------------------

	#Export Keywords to File
	def exp_file(self):
		f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
		if f is None:
			return
		for key in self.key_group.keyword_groups:
			self.key_group.keyword_groups[key] = set(self.key_group.keyword_groups[key])
			f.write("------------- \n")
			f.write(key+"\n")
			f.write("------------- \n")
			for value in self.key_group.keyword_groups[key]:
				kwords = value
				f.write(value+"\n")
		f.close()

	def exp_csv(self):
		in_path = tkFileDialog.asksaveasfilename(defaultextension=".csv")
		self.key_group.write_to_csv(in_path)

	def get_suggestions(self,URL, suggest_keywords):
		#dummy = [["test%s" %x]*10 for x in range(26)]
		qry = self.group_select
		if suggest_keywords[qry] == []:
			for a in Suggest.google_az_suggestions(URL,qry):
				suggest_keywords[qry].append(a)
		Suggestions.suggest_window(dummy,self.key_group.keyword_groups[qry])# suggest_keywords[qry]

	def clear_all(self):
		self.Import.importList.delete(0, END)
		self.Keywords.kwList.delete(0, END)
		self.Groups.groupList.delete(0, END)
		self.key_group.refresh()

	#END MENU FUNCTIONS-----------------------------------------------

	#KEYWORD LIST FUNCTIONS-------------------------------------------

	#Del kw Button function
	def del_kw(self):
		#Find what word group is currently selected with the variable group_select
		current_word = self.group_select
		#Get current self.Keywords.kwlist selction
		selection = self.Keywords.kwList.curselection()
		for i in range(len(selection)):
			value = self.Keywords.kwList.get(selection[-1-i])
			self.Keywords.kwList.delete(selection[-1-i])
			self.key_group.keyword_groups[current_word].remove(str(value))

	#Del kw Key function
	def del_kw_key(self, event):
		#Find what word group is currently selected with the variable group_select
		current_word = self.group_select
		#Get current self.Keywords.kwlist selction
		selection = self.Keywords.kwList.curselection()
		for i in range(len(selection)):
			value = self.Keywords.kwList.get(selection[-1-i])
			self.Keywords.kwList.delete(selection[-1-i])
			self.key_group.keyword_groups[current_word].remove(str(value))

	#END KEYWORD LIST FUNCTIONS---------------------------------------

	#GROUP LIST FUNCTIONS---------------------------------------------

	def onselect(self, event):
		#Tkinter passes an event object to onselect()
		self.Keywords.kwList.delete(0, END)
		w = event.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		
		self.group_select = value

		#Creates even/odd gray/white bg colors
		i = 0
		for word in self.key_group.keyword_groups[value]:
			if i % 2 == 0:
				self.Keywords.kwList.insert(END, word)
				self.Keywords.kwList.itemconfig(i,bg="#EBECF5")
			else:
				self.Keywords.kwList.insert(END, word)
			i += 1

	#Delete Group Button Function
	def del_group(self):
		selection = self.Groups.groupList.curselection()
		value = self.Groups.groupList.get(selection[0])
		del self.key_group.keyword_groups[value]
		self.Groups.groupList.delete(ANCHOR)
		#Clear selected Groups self.Keywords.KwList
		self.Keywords.kwList.delete(0, END)

	#Delete Group Key Function
	def del_group_key(self, event):
		selection = self.Groups.groupList.curselection()
		value = self.Groups.groupList.get(selection[0])
		del self.key_group.keyword_groups[value]
		self.Groups.groupList.delete(ANCHOR)
		#Clear selected Groups self.Keywords.KwList
		self.Keywords.kwList.delete(0, END)

	#Call Popup for Keyword Adding from double click on KW group
	def add_keyword_dc(self, event):
		add_kw_window()

	#END GROUP LIST FUNCTIONS-----------------------------------------

if __name__ == '__main__':
	root = Tk()
	app = MainApplication(root)
	root.wm_title("Keyword Grouper")
	root.mainloop()