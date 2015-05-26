from Tkinter import *
import string

# find the longest string in suggestions and use to set checkbox width
def long_string(array):
	n = len(array)
	maxlen = 37 # 37 is min length checkbox labels should be with looking weird
	for i in xrange(n):
		for j in array[i]:
			maxlen = max(len(j),maxlen)
	return maxlen

def suggest_window(array, sgt_list):
	
	# Helper arrays
	add_words = {}
	cb_list = []
	cb_v_list = []
	
	#FUNCTIONS FOR SUGGEST WINDOW
	def add_suggestions(sgt_list,cb_list):
		for key in add_words:
			#print key
			sgt_list.append(add_words[key][0])
			add_words[key][1].deselect()

	def add_word(i, j, add_words):
		var = "%d%d" %(i, j)
		if cb_v_list[i][j].get() == "1":
			del add_words[var]
		else:
			add_words[var] = [cb_v_list[i][j].get(), cb_list[i][j]]
		#print add_words

	# create scrolled canvas
	al = Toplevel()
	al.columnconfigure(0,weight=1)
	al.config(bg="#E8E8E8")
	al.rowconfigure(0,weight=1)
	header = Frame(al)
	header.pack(side= TOP, expand = YES)

	footer = Frame(al, relief=FLAT)
	footer.pack(side=BOTTOM, expand=YES)

	htxt = Label(header,text='Pick your Google suggested keywords', 
		font=("arial",24),pady=10,bg="#E8E8E8")
	htxt.pack()

	root = Frame(al, bd=2,relief='groove') #text='Data'
	root.pack(side = TOP, expand = YES)

	add = Button(footer, width=15, text="Add Words", highlightbackground="#E8E8E8",
	command= lambda: add_suggestions(sgt_list,cb_list))
	add.pack(side=BOTTOM, expand=YES)

	vscrollbar = Scrollbar(root)
	vscrollbar.grid(row=0, column=1, sticky=N+S)

	hscrollbar = Scrollbar(root, orient=HORIZONTAL)
	hscrollbar.grid(row=1, column=0, sticky=E+W)

	canvas = Canvas(root, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
	canvas.grid(row=0, column=0, ipadx=300, ipady=400, sticky=N+S+E+W)

	vscrollbar.config(command=canvas.yview)
	hscrollbar.config(command=canvas.xview)

	# make the canvas expandable
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)

	# create canvas contents
	overframe = Frame(canvas, height=100, width=100, padx=20, pady=20)
	overframe.pack(fill=BOTH, expand=True)

	x = string.ascii_lowercase
	maxlen = long_string(array) - 10
	for i in range(len(array)):
		cb_v_list.append([])
		cb_list.append([])
		#Label Frame for the keyword suggestion boxes
		label = LabelFrame(overframe, text = x[i].upper(), font=("arial", 18))
		label.grid(row=(i/3), column=(i%3)+5, padx=15, pady=8, 
			sticky = NW)#, ipadx=50)

		#Canvas for keyword suggestion checkboxes
		sc = Canvas(label, bg="#E8E8E8", relief=SUNKEN)
		sc.pack(expand=True, ipadx=10)

		for j in xrange(10):
			cb_v_list[i].append(StringVar())
			cb_list[i].append([])
			try:
				cb_list[i][j] = Checkbutton(sc, text=array[i][j], justify=LEFT, 
					width=maxlen, variable=cb_v_list[i][j],
					onvalue=array[i][j], offvalue= 1,
					command=lambda i=i, j=j: add_word(i, j, add_words))
				cb_list[i][j].deselect()
			except:
				cb_list[i][j] = Checkbutton(sc, text="-", justify=LEFT, 
					state=DISABLED, width=maxlen)

			cb_list[i][j].pack(fill=BOTH, expand=True)
			if j%2 == 0:
				cb_list[i][j].config(bg="#EBEFF2")

	def _on_mousewheel(event):
		canvas.yview_scroll(-1*event.delta, "units")
	def _x_mouse(event):
		canvas.xview_scroll(-1*event.delta, "units")

	# Bind mousewheel to scroll
	canvas.bind_all("<MouseWheel>", _on_mousewheel)
	canvas.bind_all("<Shift-MouseWheel>", _x_mouse)

	canvas.create_window(0, 0, anchor=NW, window=overframe)
	overframe.update_idletasks()
	canvas.config(scrollregion=canvas.bbox("all"))
	root.wait_window()


