# Importing tkinter module
from tkinter import *
from exampleLib import *
from matImport import *
from tkinter.filedialog import askopenfilename
import math

#setting global variables
#global declare is unnecessary since they are declared in the upper script outside any function
number_of_nodes = 0
b = []
b_view = []
lineStore = [[]]
lineNumber = 0
outputStore = []
outputNumber = 0

#variable which indicates if a click means a module add
clickOperation=0
#A simple function to draw circles in a canvas
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


#initializes the main menu. you have to pass the mainmenu frame and the canvas so that it could pass the canvas id when clearing it
def initMainMenu(frame, canvas):

    #column 0
    Button(frame, text="load .mat file", command= lambda: loadMat(draw, master), height = 1, width=20).grid(row=0, padx=2, pady=2)
    Button(frame, text="export .mat file", height = 1, width=20).grid(row=1, padx=2, pady=2)
    Button(frame, text="load example network", command= lambda: draw_example(draw,-10, -150,master), height = 1, width=20).grid(row=2, padx=2, pady=2)

    #column 1
    Button(frame, text="Options", height = 1, width=20).grid(row=0, column=1, padx=2, pady=2)
    Button(frame, text="Go to global view", height = 1, width=20).grid(row=1, column=1, padx=2, pady=2)
    Button(frame, text="Clear window", command= lambda: clearWindow(canvas), height = 1, width=20).grid(row=2, column=1, padx=2, pady=2)

#same as main menu initializes the submenu
def initSubMenu(frame):
    Label(frame, text="currently selected:", bg="gray").pack()
    Button(frame, text="Add transfer", command= lambda: addWidget(1), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="Remove transfer", command= lambda: removeNode(draw, master),  height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="add output", command= lambda: addWidget(2), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="remove output", command= lambda: removeOutput(draw, master), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="connect Transfer/module", command= lambda: connect(draw,master), height = 1, width=20).pack(padx=2, pady=2)


def plotMatrix(mat,draw,master,start):
    global lineNumber
    global lineStore
    global connect
    connect = []
    for x in range(len(mat)):
        stat = 0
        index = 0
        arrowModule = 0
        for value in mat[x]:
            if value != 0:
                stat = 1
            index = index + 1
        if stat == 1:
            step = (2*math.pi)/index
            xc = math.cos(step*x)*50+100 + start*200
            yc = math.sin(step*x)*50+100
            #print("x: ",x," xc: ",xc," yc:", yc)
            addNode(draw, xc, yc,master)
        for value in range(len(mat[x])):
            if (mat[x,value] == 1):
                add = 1;
                if(len(connect)!=0):
                    for var_x in range(len(connect)):
                        if(connect[var_x]==str(value)+str(x)):
                            add = 0
                        if(connect[var_x]==str(x)+str(value)):
                            add = 0
                if(add==1):
                    if(x>value):
                        connect.append(str(value)+str(x))
                        connect.sort()
                    else:
                        connect.append(str(x)+str(value))
                        connect.sort()
                    step = (2*math.pi)/index
                    xc = math.cos(step*x)*50+100 + start*200
                    yc = math.sin(step*x)*50+100

                    xe = math.cos(step*value)*50+100 + start*200
                    ye = math.sin(step*value)*50+100
                    arrowModule = value
                    print("start: ",start,"x: ",x," arrowModule: ",arrowModule)
            #draw.create_line(xc, yc, xe, ye)
                    delta_x = 0.5*(xe-xc)
                    delta_y = 0.5*(ye-yc)
                    tempStore_0 = [draw.create_line(xc, yc, xe, ye), x, arrowModule]
                    lineStore.insert(lineNumber,tempStore_0)
                    lineNumber = lineNumber+1


def loadMat(draw,master):
    global connect
    filename = askopenfilename()
    NG, NR, NH = readFile(filename)
    plotMatrix(NG,draw,master,0)
    #plotMatrix(NR,draw,master,1)
    #plotMatrix(NH,draw,master,2)


def clearWindow(canvas):
    global number_of_nodes
    global b
    global b_view
    canvas.delete("all")
    number_of_nodes = 0
    b = []
    b_view = []

#deselct nodes
def deselectNode(node, w, master, x, y):
    global b
    global b_view
    w.delete(b_view[node])
    b.pop(node)
    b_view.pop(node)
    b.insert(node, Button(master, text = "G"+str(node), command = lambda: selectNode(node, w, master, x, y), bg = "cyan"))
    b_view.insert(node, w.create_window(x, y, window=b[node]))

#select nodes
def selectNode(node, w, master, x, y):
    global b
    global b_view
    w.delete(b_view[node])
    b.pop(node)
    b_view.pop(node)
    b.insert(node, Button(master, text = "G"+str(node), command = lambda: deselectNode(node, w, master, x, y), bg = "lime"))
    b_view.insert(node, w.create_window(x, y, window=b[node]))
# adding a node
def addNode(w,x,y,master):
        global number_of_nodes
        global b
        global b_view
        f = number_of_nodes
        #creating node x
        if(b.count == number_of_nodes):
            b.extend()
            b_view.extend()
        b.insert(number_of_nodes, Button(master, text = "G"+str(number_of_nodes), command = lambda: selectNode(f,w, master, x, y), bg = "cyan"))
        b_view.insert(number_of_nodes, w.create_window(x, y, window=b[number_of_nodes]))
        #update the number of nodes
        number_of_nodes = number_of_nodes + 1

def removeNode(w, master):
        global number_of_nodes
        global b
        global b_view
        global lineStore
        global lineNumber

        node = 0
        #removing last node
        if(number_of_nodes>0):
            #update the number of nodes
            for x in range(number_of_nodes):
                if(b[x].cget('bg')=="lime"):
                    #print(b_view[x])
                    #print(b_view)
                    #print(x)
                    node = x
                    w.delete(b_view[x])
                    b_view.pop(x)
                    #print(number_of_nodes)
                    #print(b_view)
                    number_of_nodes = number_of_nodes - 1

            print("starting deleting lines at node=",node,"")
            for x in range(lineNumber):
                print("x: ",x," lineStore:",lineStore[x],"")
                if(lineStore[x]!=0):
                    if(lineStore[x][1]==node or lineStore[x][2] == node):
                        print("x: ",x," is deleted")
                        w.delete(lineStore[x][0])
                        lineStore[x]=0

def addOutput(draw, x, y, master):
        global outputStore
        global outputNumber
        node = 0
        img1 = PhotoImage(file="data/output.png")
        img1Btn = Button(master, image=img1, highlightthickness = 0, bd = 0)
        img1Btn.configure(command = lambda: selectOutput(img1Btn,draw,master))
        img1Btn.image = img1
        img1Btn["border"] = "0"
        save = [draw.create_window(x, y, window=img1Btn),img1Btn,x,y]
        if(outputNumber==0):
            outputStore.append(save)
            outputNumber = outputNumber + 1

        for m in range(outputNumber):
            if(outputStore[m]==0):
                node=m
                outputStore[m] = save

        outputStore.append(save)
        outputNumber = outputNumber + 1

def connect(draw,master):
    global lineStore
    global lineNumber
    node1 = 0
    node2 = 0
    switch = 0
    for x in range(outputNumber):
        if(outputStore[x][1]["highlightthickness"]==3):
            if(switch==0):
                node1 = outputStore[x]
                switch = 1
            else:
                node2 = outputStore[x]

    print(node1)
    print(node2)

    if((node1==node2) or (node1 == 0 or node2 == 0)):
        print("error occured with node selection")
    else:

        tempStore = [draw.create_line(node1[2], node1[3], node2[2], node2[3]), node1[1], node2[1]]
        lineStore.insert(lineNumber,tempStore)
        lineNumber = lineNumber+1
        node1[1].configure(highlightthickness=0)
        node2[1].configure(highlightthickness=0)


def removeOutput(draw,master):
    global outputStore
    global outputNumber
    for x in range(outputNumber):
        if(outputStore[x]!=0):
            if(outputStore[x][1]["highlightthickness"]==3):
                draw.delete(outputStore[x][0])
                outputStore[x] = 0

def selectOutput(id,draw,master):
    #imgGreen =  PhotoImage(file="data/outputGreen.png")
    #id.configure(image=imgGreen)
    if(id["highlightthickness"]==0):
        id.configure(highlightthickness=3)
        print("enabled id:",id["highlightthickness"])
    else:
        id.configure(highlightthickness=0)


def addWidget(input):
    global clickOperation
    clickOperation = input


def clickEvent(event):
    global clickOperation
    if(clickOperation==1):
        addNode(event.widget, event.x, event.y, master)
        clickOperation=0

    if(clickOperation==2):
        addOutput(event.widget, event.x, event.y, master)
        clickOperation=0

# creating Tk window
master = Tk()
master.configure(background="gray")
master.title("Delivery Demo")

#everything below is to make the screen resizable
Grid.rowconfigure(master, 0, weight=1)
Grid.columnconfigure(master, 0, weight=1)
masterFrame = Frame(master)
masterFrame.grid(row=0, column=0, sticky=N+S+E+W)
Grid.rowconfigure(masterFrame, 0, weight=1)
Grid.rowconfigure(masterFrame, 1, weight=100)
Grid.columnconfigure(masterFrame, 0, weight=100)
Grid.columnconfigure(masterFrame, 1, weight=1)

#seperating the menu in different frames which will hold all the components so that it is easier to use .grid for button placemant
mainMenu = Frame(masterFrame, bg="gray")
canvas = Frame(masterFrame, bg="white")
subMenu = Frame(masterFrame, bg="gray")

#alligning the grid
mainMenu.grid(row=0,sticky=N+S+E+W)
canvas.grid(row=1, sticky=N+S+E+W)
subMenu.grid(row=0, column=1, rowspan=2, sticky=N+S+E+W)

draw = Canvas(canvas, bg="white")
draw.pack(fill="both", expand=True)

#bind functions to events
draw.bind("<Button-1>", clickEvent)
initMainMenu(mainMenu, draw)
initSubMenu(subMenu)

#creating scrollbars for x and y
#scrollbar_y = Scrollbar(canvas, orient="vertical",command=draw.yview)
#scrollbar_x = Scrollbar(canvas, orient="horizontal",command=draw.xview)
#scrollable_frame = canvas
#scrollable_frame.bind("<Configure>", lambda e: draw.configure(scrollregion=draw.bbox("all")))
#draw.configure(yscrollcommand=scrollbar_y.set)
#draw.configure(xscrollcommand=scrollbar_x.set)
#scrollbar_y.pack(side="right", fill="y")
#scrollbar_x.pack(side="bottom", fill="x")


#####
class AutoScrollbar(Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise TclError('Cannot use place with this widget')

class Zoom_Advanced(Frame):
    ''' Advanced zoom of the image '''
    def __init__(self, mainframe):
        ''' Initialize the main Frame '''
        Frame.__init__(self, master=mainframe)
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
        self.canvas = draw
        self.canvas.update()  # wait till canvas is created
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('i',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('o',   self.wheel)  # only with Linux, wheel scroll up
        self.imscale = 1; #scale for the image
        self.delta = 1.3  # zoom magnitude
        self.height = 500
        self.width = 500
        # Put image into container rectangle and use it to set proper coordinates to the image
    #    self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        # Plot some optional random rectangles for the test purposes

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
#        bbox = self.canvas.bbox(self.container)  # get image area
#        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
#        else: return  # zoom only inside image area
        scale = 1.0
#         Respond to Windows (event.delta) wheel event
        if event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects

Zoom_Advanced(master)
# canvas aanmaken en even een proef of concept hardcode op het scherm
#w = Canvas(master, width=1000, height=600)
#w.pack()
#initialize_display(w,master)


# label widget
# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
mainloop()
