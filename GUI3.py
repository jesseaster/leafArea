# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

import tkinter as tk
import loadProject
import capturePic
import datetime
from PIL import Image, ImageTk


LARGE_FONT= ("Verdana", 12)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        # Initialize Window
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        pages = (StartPage, CreateNewProject, LoadExistingProject, LeafInterface)
        # Load all pages
        for F in pages:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    # shows the desired frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        label = tk.Label(self, text="Leaf Area Calculator", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Create New Project",
                            command=lambda: controller.show_frame(CreateNewProject))
        button.pack()

        button2 = tk.Button(self, text="Load Existing Project",
                            command=lambda: controller.show_frame(LoadExistingProject))
        button2.pack()


class CreateNewProject(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.variableProjectName = tk.StringVar()
        label = tk.Label(self, text="Project Name", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        entry = tk.Entry(self,
                         textvariable = self.variableProjectName)
        entry.pack()

        button1 = tk.Button(self, text="Create Project",
                command=lambda: self.getResponse(parent, controller, entry))
        button1.pack()

        button2 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()
        
    def getResponse(self, parent, controller, entry):
        projectName = self.variableProjectName.get()
        print(projectName)
        ld = loadProject.LoadProject()
        ld.newProject(projectName)
        loadExisting = self.controller.get_page(LoadExistingProject)
        loadExisting.refreshOptions(self, parent)
        controller.show_frame(LoadExistingProject)


class LoadExistingProject(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose Project", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        lp = loadProject.LoadProject()
        
        OPTIONS = lp.getProjects()


        self.variableProjectName = tk.StringVar(self)
        self.variableProjectName.set(OPTIONS[0]) # default value

        self.option = tk.OptionMenu(self, self.variableProjectName, *OPTIONS)
        self.option.pack()

        button1 = tk.Button(self, text="Load Project",
                            command=lambda: self.getResponse(parent, controller))
        button1.pack()
        
    def refreshOptions(self, parent, controller):
        lp = loadProject.LoadProject()
        self.option['menu'].delete(0, 'end')
        OPTIONS = lp.getProjects()
        for choice in OPTIONS:
            self.option['menu'].add_command(label=choice, command=tk._setit(self.variableProjectName, choice))

    def getResponse(self, parent, controller):
        print(self.variableProjectName.get())
        leafInterface = self.controller.get_page(LeafInterface)
        leafInterface.variableProjectName.set(self.variableProjectName.get())
        controller.show_frame(LeafInterface)
        
class LeafInterface(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.variableProjectName = tk.StringVar()
        variableCaterID = tk.StringVar()
        variableLeafID = tk.StringVar()
        variableCaterInstar = tk.StringVar()
        variableCaterAlive = tk.StringVar()
        variableCaterAlive.set('Yes')
        variableDate = tk.StringVar()
        variableDate.set(datetime.datetime.now().strftime("%m/%d/%Y"))
        variableTime = tk.StringVar()
        variableTime.set(datetime.datetime.now().strftime("%H:%M"))
        variableLeafArea = tk.StringVar()
        variableNotes = tk.StringVar()
        
        variables = [variableCaterID,
                    variableLeafID,
                    variableCaterInstar,
                    variableCaterAlive,
                    variableDate,
                    variableTime,
                    variableLeafArea,
                    variableNotes]
        
        def callback():
            variableLeafID.set(variableCaterID.get())
            variableCaterInstar.set('4')
            return True

        labelProjectName = tk.Label(self,
                                    textvariable=self.variableProjectName,
                                    font=LARGE_FONT).grid(row=0)
        labelCaterID = tk.Label(self,
                                width=15,
                                text="Caterpillar ID",
                                anchor='w'
                                ).grid(row=1)
        entryCaterID = tk.Entry(self,
                                width=50,
                                textvariable=variableCaterID,
                                validate="focusout",
                                validatecommand=callback
                                ).grid(row=1, column=1)

        labelLeafID = tk.Label(self,
                                width=15,
                                text="Leaf ID",
                                anchor='w'
                                ).grid(row=2)
        entryLeafID = tk.Entry(self,
                                width=50,
                                textvariable=variableLeafID,
                                ).grid(row=2, column=1)

        labelCaterInstar = tk.Label(self,
                                width=15,
                                text="Caterpillar Instar",
                                anchor='w'
                                ).grid(row=3)
        entryCaterInstar = tk.Entry(self,
                                width=50,
                                textvariable=variableCaterInstar,
                                ).grid(row=3, column=1)

        labelCaterAlive = tk.Label(self,
                                width=15,
                                text="Caterpillar Alive",
                                anchor='w'
                                ).grid(row=4)
        entryCaterAlive = tk.Entry(self,
                                width=50,
                                textvariable=variableCaterAlive,
                                ).grid(row=4, column=1)

        labelDate = tk.Label(self,
                                width=15,
                                text="Date",
                                anchor='w'
                                ).grid(row=5)
        labelDate2 = tk.Label(self,
                                width=45,
                                textvariable=variableDate,
                                anchor='w'
                                ).grid(row=5, column=1)

        labelTime = tk.Label(self,
                                width=15,
                                text="Time",
                                anchor='w'
                                ).grid(row=6)
        labelTime2 = tk.Label(self,
                                width=45,
                                textvariable=variableTime,
                                anchor='w'
                                ).grid(row=6, column=1)

        labelLeafArea = tk.Label(self,
                                width=15,
                                text="Leaf Area",
                                anchor='w'
                                ).grid(row=7)
        entryLeafArea = tk.Entry(self,
                                width=50,
                                textvariable=variableLeafArea,
                                ).grid(row=7, column=1)

        labelNotes = tk.Label(self,
                                width=15,
                                text="Notes",
                                anchor='w'
                                ).grid(row=8)
        entryNotes = tk.Entry(self,
                                width=50,
                                textvariable=variableNotes,
                                ).grid(row=8, column=1)

        labelImage = tk.Label(self,
                                width=15,
                                text="Image",
                                anchor='w'
                                ).grid(row=9)

        image = Image.open("leaf.png")
        image = image.resize((320, 256), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        photo = ImageTk.PhotoImage(image)
        
        labelImage2 = tk.Label(self,
                                image=photo,
                                bg='gray'
                                )
        labelImage2.image = photo
        labelImage2.grid(row=9, column=1, padx=10, pady=10)
        
        
        button1 = tk.Button(self, text="Take Picture",
                command=lambda: self.getImage(parent, controller, variableLeafArea, labelImage2))
        button1.grid(row=10, padx=10, pady=10)

        button2 = tk.Button(self, text="Submit",
                            command=lambda: self.getResponse(parent, controller, variables))
        button2.grid(row=10, column=1, padx=10, pady=10)
        
    def getImage(self, parent, controller, variableLeafArea, labelImage2):
        cp = capturePic.CapturePic()
        image = cp.capturePic()
        image = Image.fromarray(image)
        #image = Image.open("leaf2.png")
        image = image.resize((320, 256), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        photo = ImageTk.PhotoImage(image)
        labelImage2.configure(image=photo)
        labelImage2.image = photo
        
    def getResponse(self, parent, controller, variables):
        for variable in variables:
            print(variable.get())
            variable.set("")
        variables[3].set("Yes")
        variables[4].set(datetime.datetime.now().strftime("%m/%d/%Y"))
        variables[5].set(datetime.datetime.now().strftime("%H:%M"))

app = App()
app.mainloop()