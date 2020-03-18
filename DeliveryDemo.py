# Importing tkinter module
from tkinter import *
from exampleLib import *

#setting global variables
#global declare is unnecessary since they are declared in the upper script outside any function
number_of_nodes = 0
b = []
b_view = []

#variable which indicates if a click means a module add
clickOperation=0
#A simple function to draw circles in a canvas
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


#initializes the main menu. you have to pass the mainmenu frame and the canvas so that it could pass the canvas id when clearing it
def initMainMenu(frame, canvas):

    #column 0
    Button(frame, text="load .mat file", height = 1, width=20).grid(row=0, padx=2, pady=2)
    Button(frame, text="export .mat file", height = 1, width=20).grid(row=1, padx=2, pady=2)
    Button(frame, text="load example network", command= lambda: draw_example(draw,-10, -150,master), height = 1, width=20).grid(row=2, padx=2, pady=2)

    #column 1
    Button(frame, text="Options", height = 1, width=20).grid(row=0, column=1, padx=2, pady=2)
    Button(frame, text="Go to global view", height = 1, width=20).grid(row=1, column=1, padx=2, pady=2)
    Button(frame, text="Clear window", command= lambda: clearWindow(canvas), height = 1, width=20).grid(row=2, column=1, padx=2, pady=2)

#same as main menu initializes the submenu
def initSubMenu(frame):
    Label(frame, text="currently selected:", bg="gray").pack()
    Button(frame, text="Add node", command=addButton, height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="Remove node", command= lambda: removeNode(draw,-10,-150, master),  height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="View internals", height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="Make known", height = 1, width=20).pack(padx=2, pady=2)

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

def removeNode(w,x,y,master):
        global number_of_nodes
        global b
        global b_view
        #removing last node
        if(number_of_nodes>0):
            #update the number of nodes
            for x in range(number_of_nodes):
                if(b[x].cget('bg')=="lime"):
                    print(b_view[x])
                    print(b_view)
                    print(x)
                    w.delete(b_view[x])
                    b_view.pop(x)
                    print(number_of_nodes)
                    print(b_view)
                    number_of_nodes = number_of_nodes - 1

def addButton():
    global clickOperation
    clickOperation = 1


def clickEvent(event):
    global clickOperation
    if(clickOperation==1):
        addNode(event.widget, event.x, event.y, master)
        clickOperation=0;


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


# canvas aanmaken en even een proef of concept hardcode op het scherm
#w = Canvas(master, width=1000, height=600)
#w.pack()
#initialize_display(w,master)


# label widget
# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
mainloop()
