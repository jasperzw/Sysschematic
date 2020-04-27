# Importing tkinter module
from tkinter import *
from exampleLib import *
from matImport import *
from tkinter.filedialog import askopenfilename
import math

#setting global variables
#global declare is unnecessary since they are declared in the upper script outside any function
number_of_nodes = 0
btnStore = []
lineStore = [[]]
lineNumber = 0
outputStore = []
noiseStore = []
noiseNumber = 0
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
    Button(frame, text="add noise", command= lambda: addNoise(), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="remove noise", command= lambda: removeNoise(), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="Toggle noise", command= lambda: addWidget(2), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="connect Transfer/module", command= lambda: connect(draw,master), height = 1, width=20).pack(padx=2, pady=2)

def plotMatrix(mat,draw,master,start):
    global lineNumber
    global lineStore
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

        for value in mat[x]:
            if value != 0:
                step = (2*math.pi)/index
                xc = math.cos(step*x)*50+100 + start*200
                yc = math.sin(step*x)*50+100

                xe = math.cos(step*arrowModule)*50+100 + start*200
                ye = math.sin(step*arrowModule)*50+100
                print("start: ",start,"x: ",x," arrowModule: ",arrowModule)
                #draw.create_line(xc, yc, xe, ye)
                tempStore = [draw.create_line(xc, yc, xe, ye), x, arrowModule]
                lineStore.insert(lineNumber,tempStore)
                lineNumber = lineNumber+1
            arrowModule = arrowModule + 1


def loadMat(draw,master):
    filename = askopenfilename()
    NG, NR, NH = readFile(filename)
    plotMatrix(NG,draw,master,0)
    plotMatrix(NR,draw,master,1)
    plotMatrix(NH,draw,master,2)


def clearWindow(canvas):
    global number_of_nodes
    global outputNumber
    global btnStore
    global outputStore
    global noiseStore
    global noiseNumber
    canvas.delete("all")
    number_of_nodes = 0
    outputNumber = 0
    btnStore = []
    outputStore = []
    noiseStore = []
    noiseNumber = 0

def toggleNoise(noise):
    global noiseStore
    global noiseNumber
    if(noise.stat==1):
        noiseImgKnown = PhotoImage(file="data/noiseKnown.png")
        noise.image = noiseImgKnown
        noise.configure(image=noiseImgKnown)
        noise.stat=2
    else:
        noiseImg = PhotoImage(file="data/noise.png")
        noise.image = noiseImg
        noise.configure(image=noiseImg)
        noise.stat=1
    

def addNoise():
    global outputStore
    global outputNumber
    global noiseNumber
    global noiseStore

    switch = 0
    node = 0
    for x in range(outputNumber):
        if(outputStore[x]!=0):
            if(outputStore[x][1].stat == 2):
                node = outputStore[x]
    
    x = node[2] - 30
    y = node[3] - 50
    noiseImg = PhotoImage(file="data/noise.png")
    noise = Button(master, image = noiseImg, highlightthickness = 0, bd = 0)
    noise.configure(command = lambda: toggleNoise(noise))
    noise.image = noiseImg
    noise.stat = 1
    save = [draw.create_window(x,y, window=noise),noise,x,y,node[1]]

    if(node!=0):
        for x in range(noiseNumber):
            if(noiseStore[x]==0 and switch==0):
                noiseStore.insert(x,save)
                switch = 1
        
        if(switch==0):  
            noiseStore.append(save)
            noiseNumber = noiseNumber + 1
            print("noise added! number: ",noise)
    
def removeNoise():
    global noiseStore
    global noiseNumber
    global outputStore
    global outputNumber
    
    node = 0

    print("trying to remove the noise")

    for x in range(outputNumber):
        if(outputStore[x]!=0):
            if(outputStore[x][1].stat == 2):
                node = outputStore[x]
                print("found output: ",node)
    
    for x in range(noiseNumber):
        print("scanning: ",noiseStore[x])
        if(noiseStore[x]!=0):
            if(noiseStore[x][4] == node[1]):
                print("removing noise")
                draw.delete(noiseStore[x][0])
                noiseStore[x] = 0
                if(x == noiseNumber):
                    noiseNumber = noiseNumber - 1



#select nodes
def selectNode(node):
    global btnStore
    global number_of_nodes

    print("the node which is to be selected", node)
    if(btnStore[node][1]["bg"]=="cyan"):
        btnStore[node][1]["bg"]="lime" 
    else:
        btnStore[node][1]["bg"]="cyan"

# adding a node
def addNode(w,x,y,master):
        global number_of_nodes
        global btnStore
        node = 0
        #creating node x
        
        if(number_of_nodes==0):
            btn = Button(master, text = "G"+str(number_of_nodes), command = lambda: selectNode(0) , bg = "cyan")
            save = [draw.create_window(x, y, window=btn),btn,x,y]
            btnStore.append(save)
            number_of_nodes = number_of_nodes + 1
            print("start initial node")

        else:
            for m in range(number_of_nodes-1):
                if(btnStore[m]==0):
                    node = m
                    btn = Button(master, text = "G"+str(node), command = lambda: selectNode(node) , bg = "cyan")
                    save = [draw.create_window(x, y, window=btn),btn,x,y]
                    btnStore[m] = save
                    print("added node in existing place")
            
            if(number_of_nodes!=0 and node == 0):
                temp = number_of_nodes
                btn = Button(master, text = "G"+str(number_of_nodes), command = lambda: selectNode(temp) , bg = "cyan")
                save = [draw.create_window(x, y, window=btn),btn,x,y]
                btnStore.append(save)
                number_of_nodes = number_of_nodes + 1
                print("appended node to back of list")
        
        print(btnStore)

def removeNode(w, master):
        global number_of_nodes
        global btnStore
        global lineStore
        global lineNumber

        node = 0
        #removing last node
        if(number_of_nodes>0):
            #update the number of nodes
            for x in range(number_of_nodes-1):
                if(btnStore[x]!=0):
                    if(btnStore[x][1].cget('bg')=="lime"):
                        #print(b_view[x])
                        #print(b_view)
                        #print(x)
                        node = x
                        w.delete(btnStore[x][0])
                        btnStore[x] = 0
                        if(x==number_of_nodes-1):
                            number_of_nodes = number_of_nodes - 1
                        #print(number_of_nodes)
                        #print(b_view)


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
        img1 = PhotoImage(file="data/outputS.png")
        img1Btn = Button(master, image=img1, highlightthickness = 0, bd = 0)
        img1Btn.configure(command = lambda: selectOutput(img1Btn,draw,master))
        img1Btn.image = img1
        img1Btn.stat = 1
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
    transfer = 0
    for x in range(outputNumber):
        if(outputStore[x][1].stat==2):
            if(node1!=outputStore[x][1]):
                node1 = outputStore[x]
            else:
                node2 = outputStore[x]
    
    if(node2==0):
        for x in range(number_of_nodes):
            if(btnStore[x][1]["bg"] == "lime"):
                node2 = btnStore[x]
                transfer = 1


    print(node1)
    print(node2)

    if((node1==node2) or (node1 == 0 or node2 == 0)):
        print("error occured with node selection")
    else:
        
        tempStore = [draw.create_line(node1[2], node1[3], node2[2], node2[3]), node1[1], node2[1]]
        lineStore.insert(lineNumber,tempStore)
        lineNumber = lineNumber+1
        selectOutput(node1[1],draw,master)
        if(transfer==0):
            selectOutput(node2[1],draw,master)
        else:
            node2[1]["bg"] = "cyan"


def removeOutput(draw,master):
    global outputStore
    global outputNumber
    for x in range(outputNumber):
        if(outputStore[x]!=0):
            if(outputStore[x][1].stat == 2):
                draw.delete(outputStore[x][0])
                outputStore[x] = 0

def selectOutput(id,draw,master):
    #work in progress image swap werkt nog niet
    if(id.stat==1):
        imgGreen = PhotoImage(file="data/outputGreenS.png")
        id.image = imgGreen
        id.stat = 2
        id.configure(image=imgGreen)
        print("setting output green")
    else:
        imgWhite = PhotoImage(file="data/outputS.png")
        id.image=imgWhite
        id.stat = 1
        id.configure(image=imgWhite)
        print("setting output white")
    #if(id["highlightthickness"]==0):
    #    id.configure(highlightthickness=3)
    #    print("enabled id:",id["highlightthickness"])
    #else:
    #    id.configure(highlightthickness=0)


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
master.geometry("1000x500")

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
