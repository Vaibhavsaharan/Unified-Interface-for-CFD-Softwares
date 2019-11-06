from tkinter import *
from tkinter import filedialog 
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.ttk import Progressbar
from functools import partial
from shutil import copy2
import shutil
import subprocess
import os

root = Tk()
root.title("Unified-Interface")

def New():  
	top = Toplevel(root)
	top.title("Create Project")
	top.geometry("600x300+%d+%d" % (root.winfo_rootx() + 600,root.winfo_rooty() + 200))
	pathname = StringVar()
	pathname.set(os.getcwd())
	def _browse():
		path = askdirectory(title = 'Select folder to save results')
		pathname.set(path)
	def _Create():
		try:
			os.mkdir(pathname.get()+"/"+CreateEntry.get())
			os.mkdir(pathname.get()+"/"+CreateEntry.get()+"/"+"pre-processing")
			os.mkdir(pathname.get()+"/"+CreateEntry.get()+"/"+"post-processing")
			os.mkdir(pathname.get()+"/"+CreateEntry.get()+"/"+"solver")
			messagebox.showinfo("info",CreateEntry.get()+"file created succesfully")
			projectnameText.set(CreateEntry.get())
			projectpathText.set(os.getcwd()+"/"+projectnameText.get())
			top.destroy()
			cmd="./a "+ projectpathText.get()
			# print(cmd)
			#print(projectpathText.get())
			os.system(cmd)
			refresh_submenu()
			main()
			
		except OSError as error:
			messagebox.showerror("Error",projectnameText.get()+" file already exists")
	createlabel = Label(top, text = 'Project name')
	createlabel.grid(row=2, column=0, pady=(50,10), padx=(10,0))
	createlabel = Label(top, text = 'Project location')
	createlabel.grid(row=3, column=0, pady=(10,10), padx=(10,10))
	CreateEntry = Entry(top, bd =1)
	CreateEntry.grid(row=2, column=1, pady=(50,10), padx=(0,0))
	BrowseEntry = Entry(top, textvariable = pathname, bd =1)
	BrowseEntry.grid(row=3, column=1, columnspan= 2, pady=(10,10), padx=(20,20))
	BrowseEntry.config(width=60)
	button = Button(top, height=1, width=20, text="Create", bg='gray97', command=_Create, relief=GROOVE)
	button1 = Button(top, height=1, width=20, text="Browse", bg='gray97', command=_browse, relief=GROOVE)
	button.grid(row=2, column=2, pady=(50,10), padx=(0,20))
	button1.grid(row=4, column=2, pady=(10,10), padx=(0,20))
	top.mainloop()  

def Open():
	top1 = Toplevel(root)
	top1.title("Open Project")
	top1.geometry("400x300+%d+%d" % (root.winfo_rootx() + 600,root.winfo_rooty() + 200))
	def browsefunc():
		pathofdir = askdirectory(title = 'Choose Project')
		projectpathText.set(pathofdir)
		projectnameText.set(pathofdir[pathofdir.rfind("/")+1:])
		currentdir = os.getcwd()
		os.chdir(pathofdir)
		if os.path.isdir("pre-processing"):
			os.chdir(currentdir)
			top1.destroy()
			cmd="./a "+ pathofdir
			# print(cmd)
			os.system(cmd)
			refresh_submenu()
			main()
			
		else:
			messagebox.showerror("Error","Please select correct Project Directory")
			os.chdir(currentdir)
	browsebutton = Button(top1, height=1, width=20, text="Browse", bg='gray97', command= browsefunc, relief=GROOVE)
	browsebutton.grid(row=2, column=0, pady=(10,10), padx=(120,20))
	labelText = StringVar()
	labelText.set("Open Project")
	pathlabel = Label(top1, textvariable = labelText)
	pathlabel.grid(row=1, column=0, pady=(100,10), padx=(120,20))

# function for getting latest working project
def previous(n):
	path=os.getcwd()+"/filelog"
	count = 0
	# counting number of working project in queu
	with open(path, 'r') as f:
	    for line in f:
	        count += 1
	f.close()
	# getting link of desired project and creating command for running script
	f=open(path)
	for i in range(count-n-1):
		f.readline()
	temp=f.readline()
	pathofdir=temp[:temp.rfind("\n")]
	cmd="./a "+ temp
	# checking selected link is valid or not
	#if valid
	try:
		projectpathText.set(pathofdir)
		projectnameText.set(pathofdir[pathofdir.rfind("/")+1:])
		pwd=os.getcwd()
		os.chdir(pathofdir)
		os.chdir(pwd)
		messagebox.showinfo("info","Now your working project is "+projectpathText.get())
	#else
	except OSError as error:
			messagebox.showerror("Error",projectpathText.get()+" is no longer available")
			return
	os.system(cmd)
	main()


def OpenGeo(gmshfile,makemshbutton):
	top1 = Toplevel(root)
	top1.title("Open File(.geo)")
	top1.geometry("400x300+%d+%d" % (root.winfo_rootx() + 600,root.winfo_rooty() + 200))
	def browsefunc():
		src =  filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("geo files","*.geo"),("all files","*.*")))
		gmshfile.set(src[src.rfind("/")+1:])
		dest = projectpathText.get()+"/"+"pre-processing"
		copy2(src,dest)
		makemshbutton.config(state = 'normal')
		top1.destroy()		
	browsebutton = Button(top1, height=1, width=20, text="Browse", bg='gray97', command= browsefunc, relief=GROOVE)
	browsebutton.grid(row=2, column=0, pady=(10,10), padx=(120,20))
	labelText = StringVar()
	labelText.set("Choose a file...")
	pathlabel = Label(top1, textvariable = labelText)
	pathlabel.grid(row=1, column=0, pady=(100,10), padx=(120,20))

def Preprocessing(gmshfile):
	gmshfile1 = gmshfile.get()
	mshfile = gmshfile1[:gmshfile1.rfind(".")]+".msh"
	cmd = "gmsh -2 "+ projectpathText.get()+"/pre-processing/"+gmshfile.get()
	currentdir = os.getcwd()
	os.chdir(projectnameText.get())
	os.chdir("pre-processing")
	cmd2 = "gmsh "+mshfile 
	os.system(cmd)
	os.system(cmd2)
	os.chdir(currentdir)
	refresh()

def Postprocessing():
	cmd = "python plot_data.py"
	os.system(cmd)
	refresh()


def Solving(flmlfile):
	currentdir = os.getcwd()
	os.chdir(projectnameText.get())
	cmd = "fluidity "+"solver/"+flmlfile.get()
	os.system(cmd)
	os.chdir(currentdir)
	os.chdir("2dtank")
	x = [f.name for f in os.scandir() if f.is_file()]
	os.chdir(currentdir)
	for i in x:
		shutil.move("2dtank/"+i ,"2dtank/post-processing/"+i)
	refresh()

def main():
	btn1.config(state = 'normal')
	btn2.config(state = 'normal')
	btn3.config(state = 'normal')
	btn4.config(state = 'normal')
	refresh()
	pass

def _CreateGeo():
	os.chdir(projectnameText.get())
	os.chdir("pre-processing")
	subprocess.run("gmsh")
	os.chdir("../..")

	pass


def refresh():
	pathmsh = projectpathText.get()+"/pre-processing/"
	pathvtu = projectpathText.get()+"/post-processing/"
	filesmsh = []
	filesvtu = []
	filespara = []
	for r, d, f in os.walk(pathmsh):
		for file in f:
			if '.msh' in file:
				filesmsh.append(file)
	for r, d, f in os.walk(pathvtu):
		for file in f:
			if '.vtu' in file:
				filesvtu.append(file)


	if(len(filesmsh)!=0):
		progress['value'] = 33
	if(len(filesvtu)!=0):
		progress['value'] = 66
	pass

	
#function for setting recent button name
def update_recent_bot(n):
	path=os.getcwd()+"/filelog"
	count = 0
	f=open(path,'a')
	f.close()
	# counting number of working project in queu
	with open(path, 'r') as f:
	    for line in f:
	        count += 1
	f.close()
	if(count<n):
		return "nothing"
	# getting link of desired project and creating command for running script
	f=open(path)
	for i in range(count-n):
		f.readline()
	temp=f.readline()
	pathofdir=temp[:temp.rfind("\n")]
	return pathofdir[pathofdir.rfind("/")+1:]


def refresh_submenu():
	Recent_1.set(update_recent_bot(1))
	Recent_2.set(update_recent_bot(2))
	if Recent_1.get()=="nothing":
		submenu.entryconfigure(1,state=DISABLED,label="no recent1")
	else:
		submenu.entryconfigure(1,label="R1:- "+Recent_1.get(),state='normal')
	if Recent_2.get()=="nothing":
		submenu.entryconfigure(2,state=DISABLED,label="no recent2")
	else:
		submenu.entryconfigure(2,label="R2:- "+Recent_2.get(),state='normal')

def deletepre(gmshoption1,gmshoption2,geolable,popupMenu,gmshcheck,geobutton,geobutton1,makemshbutton):
	gmshoption1.destroy()
	gmshoption2.destroy()
	geolable.destroy()
	popupMenu.destroy()
	gmshcheck.destroy()
	geobutton.destroy()
	geobutton1.destroy()
	makemshbutton.destroy()
	usingsolver()

def deletesolver(solveroption1,solveroption2,solverlable,solverbutton,solverbutton1,popupMenu1,popupMenu2,solvebutton):
	solveroption1.destroy()
	solveroption2.destroy()
	solverlable.destroy()
	popupMenu1.destroy()
	popupMenu2.destroy()
	solvebutton.destroy()
	solverbutton.destroy()
	solverbutton1.destroy()
	usingpost()

def usingpre():
	gmshfile = StringVar()
	gmshfile.set("Choose your .geo file")
	gmsh1 = StringVar()
	geoavailvar = IntVar()
	btn1.config(relief=SUNKEN)
	btn2.config(relief=RAISED)
	btn3.config(relief=RAISED)
	rightframe.grid()
	choices = { '2-dimensional','3-dimensional'}
	gmsh1.set('2-dimensional')
	
	def change_dropdown(*args):
		print( gmsh1.get() )

	gmsh1.trace('w', change_dropdown)

	softwarelabel = Label(rightframe,text = 'GMSH',width = 130, height=0,anchor = CENTER, font=("Helvetica", 20),highlightbackground="black",highlightthickness=1)
	gmshoption1 = Label(rightframe,text = 'Mesh Format',width = 50, height=5,anchor = CENTER, font=("Times", 16))
	gmshoption2 = Label(rightframe,text = 'Geo file available',width = 50, height=2,anchor = CENTER ,font=("Times", 16))
	geolable = Label(rightframe,textvariable = gmshfile,width = 60, height=2,anchor = CENTER, font=("Times", 12))
	popupMenu = OptionMenu(rightframe, gmsh1, *choices)
	gmshcheck = Checkbutton(rightframe, variable= geoavailvar,width=2,height=2)
	makemshbutton = Button(rightframe, height=2, width=20, text="Create mesh", command=partial(Preprocessing,gmshfile), relief=RAISED,bg="lightgreen",fg="black",state=DISABLED)
	geobutton = Button(rightframe, height=1, width=20, text="Browse", command=partial(OpenGeo,gmshfile,makemshbutton), relief=GROOVE)
	geobutton1 = Button(rightframe, height=1, width=20, text="Create",  command=_CreateGeo, relief=GROOVE)
	continuebutton = Button(rightframe, height=2, width=20, text="Continue", command= partial(deletepre,gmshoption1,gmshoption2,geolable,popupMenu,gmshcheck,geobutton,geobutton1,makemshbutton), relief=RAISED,bg="red",fg="white")

	softwarelabel.grid(row = 0,sticky="we",padx=(0,1200))
	gmshoption1.grid(row = 1,sticky="nw")
	gmshoption2.grid(row = 2,sticky="nw")
	popupMenu.grid(row = 1,padx=340 ,sticky="w")
	gmshcheck.grid(row=2,sticky="w",padx=390)
	currentdir = os.getcwd()
	# os.chdir(projectnameText.get())
	# os.chdir("pre-processing")
	path = projectpathText.get()+"/pre-processing/"
	files = []
	for r, d, f in os.walk(path):
		for file in f:
			if '.geo' in file:
				files.append(file)
	if (len(files)==0):
		geolable.grid(row = 2,sticky="w",padx=500)
		geobutton.grid(row = 2,sticky="w",padx=890)
		geobutton1.grid(row = 2,sticky="w",padx=1090)
		gmshcheck.deselect()
	elif (len(files)==1):
		gmshcheck.select()
		gmshfile.set(files[0])
		geolable.grid(row = 2,sticky="w",padx=500)
		makemshbutton.config(state = 'normal')
	else :
		messagebox.showerror("Error","Your Project(pre-processing) Directory cannot contain more than one .geo file")
	makemshbutton.grid(row = 3,sticky="nw",padx=170,pady=30)
	continuebutton.grid(row = 4,sticky="nw",padx=170,pady=570)
	pass

def usingsolver():
	solverdrop1 = StringVar()
	solverdrop2 = StringVar()
	flmlfile = StringVar()
	flmlfile.set("Choose your .flml file")
	btn2.config(relief=SUNKEN)
	btn1.config(relief=RAISED)
	btn3.config(relief=RAISED)
	rightframe.grid_remove()
	rightframe.grid()
	choices1 = { 'Series','Parallel'}
	solverdrop1.set('Parallel')
	choices2 = { '1','2','3','4'}
	solverdrop2.set('4')
	
	def change_dropdown1(*args):
		print( solverdrop1.get() )

	solverdrop1.trace('w', change_dropdown1)

	def change_dropdown2(*args):
		print( solverdrop2.get() )

	solverdrop1.trace('w', change_dropdown2)

	softwarelabel1 = Label(rightframe,text = 'Fluidity',width = 100, height=0,anchor = W, font=("Helvetica", 20),highlightbackground="black",highlightthickness=1)
	softwarelabel2 = Label(rightframe,text = 'OpenFoam',width = 100, height=0,anchor = W, font=("Helvetica", 20),highlightbackground="black",highlightthickness=1)
	solveroption1 = Label(rightframe,text = 'Processor Usage',width = 50, height=5,anchor = CENTER, font=("Times", 16))
	solveroption2 = Label(rightframe,text = 'Number of Processor',width = 50, height=2,anchor = CENTER ,font=("Times", 16))
	solverlable = Label(rightframe,textvariable = flmlfile,width = 60, height=2,anchor = CENTER, font=("Times", 12))
	solverbutton = Button(rightframe, height=1, width=20, text="Browse", command=OpenGeo, relief=GROOVE)
	solverbutton1 = Button(rightframe, height=1, width=20, text="Create",  command=_CreateGeo, relief=GROOVE)
	#solveroption3 = Label(rightframe,text = 'Timestep',width = 50, height=5,anchor = CENTER, font=("Times", 16))
	#solveroption4 = Label(rightframe,text = 'Simulation',width = 50, height=2,anchor = CENTER ,font=("Times", 16))
	popupMenu1 = OptionMenu(rightframe, solverdrop1, *choices1)
	popupMenu2 = OptionMenu(rightframe, solverdrop2, *choices2)
	#BrowseEntry1 = Entry(rightframe)
	#BrowseEntry2 = Entry(rightframe)
	
	solvebutton = Button(rightframe, height=2, width=20, text="Solver", command=partial(Solving,flmlfile), relief=RAISED,bg="lightgreen",fg="black",state=DISABLED)
	continuebutton = Button(rightframe, height=2, width=20, text="Continue", command=partial(deletesolver,solveroption1,solveroption2,solverlable,solverbutton,solverbutton1,popupMenu1,popupMenu2,solvebutton), relief=RAISED,bg="red",fg="white")


	softwarelabel1.grid(row = 0,sticky="w",padx=(00,500))
	softwarelabel2.grid(row = 0,sticky="w",padx=(800,600))
	solveroption1.grid(row = 1,sticky="nw")
	solveroption2.grid(row = 2,sticky="nw")
	#solveroption3.grid(row = 1,sticky="nw",padx=500)
	#solveroption4.grid(row = 2,sticky="nw",padx=500)
	popupMenu1.grid(row = 1,padx=390 ,sticky="w")
	popupMenu2.grid(row = 2,padx=390 ,sticky="w")
	path = projectpathText.get()+"/solver/"
	files = []
	for r, d, f in os.walk(path):
		for file in f:
			if '.flml' in file:
				files.append(file)
	if (len(files)==0):
		solverlable.grid(row = 2,sticky="w",padx=500)
		solverbutton.grid(row = 2,sticky="w",padx=890)
		solverbutton1.grid(row = 2,sticky="w",padx=1090)
		#gmshcheck.deselect()
	elif (len(files)==1):
		#gmshcheck.select()
		flmlfile.set(files[0])
		solverlable.grid(row = 2,sticky="w",padx=500)
		solvebutton.config(state = 'normal')
	else :
		messagebox.showerror("Error","Your Project(solver) Directory cannot contain more than one .flml file")
	
	#BrowseEntry1.grid(row = 1,padx=940 ,sticky="w")
	#BrowseEntry2.grid(row = 2,padx=940 ,sticky="w")

	solvebutton.grid(row = 3,sticky="nw",padx=170,pady=30)
	continuebutton.grid(row = 4,sticky="nw",padx=170,pady=570)
	pass

def usingpost():
	postdrop1 = StringVar()
	postdrop2 = StringVar()
	btn3.config(relief=SUNKEN)
	btn2.config(relief=RAISED)
	btn1.config(relief=RAISED)
	rightframe.grid_remove()
	rightframe.grid()
	choices1 = { 'Volume fraction','Pressure','Velocity'}
	postdrop1.set('Velocity')
	choices2 = { 'debris','frout'}
	postdrop2.set('debris')
	
	def change_dropdown1(*args):
		print( postdrop1.get() )

	postdrop1.trace('w', change_dropdown1)

	def change_dropdown2(*args):
		print( postdrop2.get() )

	postdrop1.trace('w', change_dropdown2)

	postlabel1 = Label(rightframe,text = 'Paraview',width = 100, height=0,anchor = W, font=("Helvetica", 20),highlightbackground="black",highlightthickness=1)
	postlabel2 = Label(rightframe,text = 'Python',width = 100, height=0,anchor = W, font=("Helvetica", 20),highlightbackground="black",highlightthickness=1)
	postoption1 = Label(rightframe,text = 'Animation',width = 50, height=5,anchor = CENTER, font=("Times", 16))
	postoption2 = Label(rightframe,text = 'Plot',width = 50, height=2,anchor = CENTER ,font=("Times", 16))
	postlable3 = Label(rightframe,text = 'Choose your .vtu file',width = 60, height=2,anchor = CENTER, font=("Times", 12))
	postbutton = Button(rightframe, height=1, width=20, text="Browse", command=OpenGeo, relief=GROOVE)
	popupMenu1 = OptionMenu(rightframe, postdrop1, *choices1)
	popupMenu2 = OptionMenu(rightframe, postdrop2, *choices2)
	viewbutton = Button(rightframe, height=2, width=20, text="Play",command = Postprocessing , relief=RAISED,bg="lightgreen",fg="black")
	continuebutton = Button(rightframe, height=2, width=20, text="Exit", command=root.quit, relief=RAISED,bg="red",fg="white")



	postlabel1.grid(row = 0,sticky="w",padx=(00,500))
	postlabel2.grid(row = 0,sticky="w",padx=(800,600))
	postoption1.grid(row = 1,sticky="nw")
	postoption2.grid(row = 2,sticky="nw")
	popupMenu1.grid(row = 1,padx=390 ,sticky="w")
	popupMenu2.grid(row = 2,padx=390 ,sticky="w")
	postlable3.grid(row = 2,sticky="w",padx=500)
	postbutton.grid(row = 2,sticky="w",padx=890)



	viewbutton.grid(row = 3,sticky="nw",padx=170,pady=30)
	continuebutton.grid(row = 4,sticky="nw",padx=170,pady=570)
	pass


projectnameText = StringVar()
projectpathText = StringVar()
menu = Menu(root) 
root.config(menu=menu) 
filemenu = Menu(menu) 

submenu = Menu(filemenu)
Recent_1=StringVar()
Recent_2=StringVar()
#submenu.add_command(label="Recent 2",command=partial(previous,1))		
submenu.add_command(label="no recent",command=partial(previous,0))
submenu.add_command(label="no recent",command=partial(previous,1))
#submenu.add_command(label="refresh",command=partial(ref))
refresh_submenu()
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_command(label='New Project' , command = New, font=('Verdana', 10)) 
filemenu.add_command(label='Open Project', command = Open, font=('Verdana', 10) ) 
filemenu.add_separator() 
filemenu.add_cascade(label='Recent Projects', menu = submenu, font=('Verdana', 10) ) 
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit, font=('Verdana', 10)) 
helpmenu = Menu(menu) 
menu.add_cascade(label='Help', menu=helpmenu) 
helpmenu.add_command(label='About', font=('Verdana', 10)) 
helpmenu.add_command(label='Documentation', font=('Verdana', 10)) 

root.geometry("1600x900")
var1 = IntVar()
var2 = IntVar() 
var3 = IntVar() 
var4 = IntVar() 
var5 = IntVar() 
var6 = IntVar() 
var7 = IntVar() 
var8 = IntVar() 
var9 = IntVar()


topframe = Frame(root,height=14)
bottomframe = Frame(root,height=950)
leftframe  = Frame(bottomframe,width=400,height=950,highlightbackground="black",highlightthickness=1,bg='#bababa')
rightframe  = Frame(bottomframe,width=1640,height=950,highlightbackground="black",highlightthickness=1)


topframe.grid(row=0,sticky="nsew")
bottomframe.grid(row=0,sticky="nsew")
leftframe.grid(column=0,row=1,sticky="nw")
rightframe.grid(column=1,row=1,sticky="nw")



btn1 = Button(leftframe, text = "Pre-Processor", command = usingpre,state = DISABLED, height = 3,width = 40)  
btn2 = Button(leftframe, text = "Solver", command = usingsolver,state = DISABLED,  height = 3,width = 40)  
btn3 = Button(leftframe, text = "Post-Processor", command = usingpost,state = DISABLED,  height = 3,width = 40)  
btn4 = Button(leftframe, text = "Refresh Progress", state = DISABLED, command = refresh,  height = 2,width = 20) 
proglabel0 = Label(leftframe,text = "*********Project-Name*********",anchor = CENTER ,font=("Times", 16),bg='#bababa')
proglabel1 = Label(leftframe,textvariable=projectnameText,anchor = CENTER ,font=("Times", 16),bg='#bababa')
proglabel2 = Label(leftframe,text = "******************************" ,anchor = CENTER ,font=("Times", 16),bg='#bababa') 
prog1 = Label(leftframe,text = 'post-processing',anchor = CENTER ,font=("Times", 16),bg='#bababa')
prog2 = Label(leftframe,text = 'solving',anchor = CENTER ,font=("Times", 16),bg='#bababa')
prog3 = Label(leftframe,text = 'pre-processing',anchor = CENTER ,font=("Times", 16),bg='#bababa')
software = Label(leftframe,text = "Unified-Interface for CFD Softwares" ,anchor = CENTER ,font=("cosmic", 16),bg='#bababa',wraplength=250) 

progress = Progressbar(leftframe, orient = VERTICAL, length = 270, mode = 'determinate') 


btn1.grid(row =0)
btn2.grid(row =1)
btn3.grid(row =2)
proglabel0.grid(row = 3, pady =10)
proglabel1.grid(row = 4, pady =10)
proglabel2.grid(row = 5, pady =10)
btn4.grid(row =6,pady = (100,0))
progress.grid(pady = 30, padx=(265,0), row = 7,rowspan = 3)
prog1.grid(row = 7, pady =(80,30))
prog2.grid(row = 8, pady =(20,20))
prog3.grid(row = 9, pady =(30,100))
software.grid(row = 10, pady =(120,20))

# mshfile = StringVar()
# projectnameText = StringVar()
# projectpathText = StringVar()
# projectnameText.set("Please Open a Project")
# projectpathText.set("**Project-LOCATION**")
# namelabel = Label(leftframe, textvariable = projectnameText)
# pathlabel = Label(rightframe, textvariable = projectpathText)
# namelabel.pack(pady = 5)
# pathlabel.pack(pady = 5)

root.mainloop()
