# Importing tkinter module
from tkinter import *
from exampleLib import *
from matImport import readFile
from tkinter.filedialog import askopenfilename
import math
from Scrollwindow import *



"""
initializing all global components
The structure used for both btnStore and outputStore is as follows [windowsId, WidgetObject, x, y]
windowId is the canvas id generated by create window and widgetObject is the object you can edit to change color and such
the noise store has an extra entry which comes down to [windowsId, WidgetObject, x, y, outputObject] where output Object is the object of the output on which the noise is applied
tempStore follows [widgetId, objectId1, objectId2] object 1 en object 2 is the objects between which the line is connected
widgetId is what you call to remove it from the canvas in draw.delete(widgetId)
"""
number_of_nodes = 0
btnStore = []
lineStore = [[]]
lineNumber = 0
outputStore = []
noiseStore = []
connect = []
noiseNumber = 0
outputNumber = 0
#global declare is unnecessary since they are declared in the upper script outside any function
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
    Button(frame, text="add noise", command= lambda: addNoise(master, draw), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="remove noise", command= lambda: removeNoise(master, draw), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="Toggle noise", command= lambda: addWidget(2), height = 1, width=20).pack(padx=2, pady=2)
    Button(frame, text="connect Transfer/module", command= lambda: connectCall(draw,master), height = 1, width=20).pack(padx=2, pady=2)

# Load mat will move everything in from the specific mat file.
def loadMat(draw,master):
    global connect
    global lineNumber
    global lineStore
    filename = askopenfilename()
    NG, NR, NH = readFile(filename)
    lotMatrix(NG,draw,master,0)
    print(connect)
    #plotMatrix(NR,draw,master,1)
    #plotMatrix(NH,draw,master,2)

def plotMatrix(mat,draw,master,start):
    global lineNumber
    global lineStore
    global connect
    connect = []

    #below function will read through the mat file and try to find how many modules their are
    for x in range(len(mat)):
        stat = 0
        index = 0
        arrowModule = 0
        for value in mat[x]:
            if value != 0:
                stat = 1
            index = index + 1
        if stat == 1:
            #plot each function in a circle
            step = (2*math.pi)/index
            xc = math.cos(step*x)*50+100 + start*200
            yc = math.sin(step*x)*50+100
            #print("x: ",x," xc: ",xc," yc:", yc)
            addNode(draw, xc, yc,master)
            #connect each part
        for value in range(len(mat[x])):
            if (mat[x,value] == 1):
                add = 1;
                if(len(connect)!=0):
                    for var_x in range(len(connect)):
                        if(connect[var_x]==str(x)+str(value)):
                            add = 0
                if(add==1):
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



"""
Below we have the subsection of:

-------------------------------------------------------- nodes --------------------------------------------------------

Each function uses the global variables to store the nodes and to make changes
"""

def selectNode(node):
    global btnStore
    global number_of_nodes

    #simpely edit the node its color based on the node object given in the argument
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

        #perform initial node
        if(number_of_nodes==0):
            btn = Button(master, text = "G"+str(number_of_nodes), command = lambda: selectNode(0) , bg = "cyan")
            save = [w.create_window(x, y, window=btn),btn,x,y]
            #append it on th end
            btnStore.append(save)
            number_of_nodes = number_of_nodes + 1
            print("start initial node")

        else:
            #first search if a entry is zero because then a node has been removed their and we can insert a new one
            for m in range(number_of_nodes-1):
                if(btnStore[m]==0):
                    node = m
                    btn = Button(master, text = "G"+str(node), command = lambda: selectNode(node) , bg = "cyan")
                    save = [w.create_window(x, y, window=btn),btn,x,y]
                    btnStore[m] = save
                    print("added node in existing place")

            #if no space is free and it is not the initial node append a new one on the end.
            if(number_of_nodes!=0 and node == 0):
                temp = number_of_nodes
                btn = Button(master, text = "G"+str(number_of_nodes), command = lambda: selectNode(temp) , bg = "cyan")
                save = [w.create_window(x, y, window=btn),btn,x,y]
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
        #check if their is atleast 1 node
        if(number_of_nodes>0):
            #update the number of nodes
            for x in range(number_of_nodes-1):
                if(btnStore[x]!=0):
                    #check the colors the find the specific transfer
                    if(btnStore[x][1].cget('bg')=="lime"):
                        #print(b_view[x])
                        #print(b_view)
                        #print(x)
                        node = x
                        #delete it from the canvas and set it to 0 in btnStore
                        w.delete(btnStore[x][0])
                        btnStore[x] = 0
                        if(x==number_of_nodes-1):
                            number_of_nodes = number_of_nodes - 1
                        #print(number_of_nodes)
                        #print(b_view)

            #search if we can find it in lineStore and remove it
            print("starting deleting lines at node=",node,"")
            for x in range(lineNumber):
                print("x: ",x," lineStore:",lineStore[x],"")
                if(lineStore[x]!=0):
                    if(lineStore[x][1]==node or lineStore[x][2] == node):
                        print("x: ",x," is deleted")
                        w.delete(lineStore[x][0])
                        lineStore[x]=0

"""
below are the functions regarding

-------------------------------------------------------- noise --------------------------------------------------------
"""

def toggleNoise(noise):
    global noiseStore
    global noiseNumber
    #switch color base on stat variable bound to the noise.
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


def addNoise(master, draw):
    global outputStore
    global outputNumber
    global noiseNumber
    global noiseStore

    switch = 0
    node = 0
    #find output which is selected and save it to node
    for x in range(outputNumber):
        print(outputStore[x])
        if(outputStore[x]!=0):
            if(outputStore[x][1].stat == 2):
                node = outputStore[x]

    #move the x y to left above the center of the output
    x = node[2] - 30
    y = node[3] - 50

    #creating noise button
    noiseImg = PhotoImage(file="data/noise.png")
    noise = Button(master, image = noiseImg, highlightthickness = 0, bd = 0)
    noise.configure(command = lambda: toggleNoise(noise))
    noise.image = noiseImg
    noise.stat = 1
    save = [draw.create_window(x,y, window=noise),noise,x,y,node[1]]

    #store noise in a open spot
    if(node!=0):
        for x in range(noiseNumber):
            if(noiseStore[x]==0 and switch==0):
                noiseStore.insert(x,save)
                switch = 1

        #if no open space left append it on the end
        if(switch==0):
            noiseStore.append(save)
            noiseNumber = noiseNumber + 1
            print("noise added! number: ",noise)

def removeNoise(master, draw):
    global noiseStore
    global noiseNumber
    global outputStore
    global outputNumber

    node = 0

    print("trying to remove the noise")

    #find selected output
    for x in range(outputNumber):
        if(outputStore[x]!=0):
            if(outputStore[x][1].stat == 2):
                node = outputStore[x]
                print("found output: ",node)

    #search for noise entry which has the selected output
    for x in range(noiseNumber):
        print("scanning: ",noiseStore[x])
        if(noiseStore[x]!=0):
            if(noiseStore[x][4] == node[1]):
                print("removing noise")
                #remove it
                draw.delete(noiseStore[x][0])
                noiseStore[x] = 0
                if(x == noiseNumber):
                    noiseNumber = noiseNumber - 1

"""
Below are the functions for

-------------------------------------------------------- output --------------------------------------------------------

tada
"""
def addOutput(draw, x, y, master):
        global outputStore
        global outputNumber
        #create output
        switch = 0
        node = 0
        img1 = PhotoImage(file="data/outputS.png")
        img1Btn = Button(master, image=img1, highlightthickness = 0, bd = 0)
        nmb = Label(master, text="0", bg="white")
        img1Btn.configure(command = lambda: selectOutput(img1Btn))
        img1Btn.image = img1
        img1Btn.stat = 1
        img1Btn["border"] = "0"


        save = [draw.create_window(x, y, window=img1Btn),img1Btn,x,y,draw.create_window(x+10,y+5,window=nmb),nmb]

        #earch if their is a empty entry.
        for m in range(outputNumber):
            if(outputStore[m]==0):
                node=m
                nmb.configure(text=str(m))
                outputStore[m] = save
                img1Btn.image.text = str(m)
                switch = 1

                #initial output
        if(outputNumber==0):
            outputStore.append(save)
            outputNumber = outputNumber + 1
            switch = 1

        #append if no empty entry
        if(switch==0):
            nmb.configure(text=str(outputNumber))
            outputStore.append(save)
            outputNumber = outputNumber + 1


def removeOutput(draw,master):
    global outputStore
    global outputNumber
    #search for output and set it to 0
    for x in range(outputNumber):
        if(outputStore[x]!=0):
            if(outputStore[x][1].stat == 2):
                draw.delete(outputStore[x][0])
                outputStore[x] = 0

def selectOutput(id):
    #each output has a stat variable which indicates state. stat == 1 is not selected, stat == 2 is selected
    #work in progress image swap werkt nog niet
    nmb = 0
    #finding corresponding label
    for x in range(outputNumber):
        if(outputStore[x]!=0):
            if(outputStore[x][1]==id):
                nmb=outputStore[x][5]


    if(id.stat==1):
        imgGreen = PhotoImage(file="data/outputGreenS.png")
        id.image = imgGreen
        id.stat = 2
        nmb.configure(bg="limegreen")
        id.configure(image=imgGreen)
        print("setting output green")
    else:
        imgWhite = PhotoImage(file="data/outputS.png")
        id.image=imgWhite
        id.stat = 1
        nmb.configure(bg="white")
        id.configure(image=imgWhite)
        print("setting output white")


"""
below are the remaining functions

-------------------------------------------------------- Remaining --------------------------------------------------------
"""
def clearWindow(canvas):
    #remove everythin and set all global to 0
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


#select nodes
def connectCall(draw,master):
    global number_of_nodes
    global btnStore
    global lineStore
    global lineNumber
    node1 = 0
    node2 = 0
    node3 = 0

    #serach first for selected outputs
    for x in range(outputNumber):
        if(outputStore[x][1].stat==2):
            if(outputStore[x][1]!=node1 and node1==0):
                node1 = outputStore[x]
            elif(node2!=outputStore[x][1]):
                node2 = outputStore[x]

    #check if the node is not the same or not 0.
    if((node1==node2) or (node1 == 0 or node2 == 0)):
        print("error occured with node selection")

    else:
        temp = 0
        for x in range(lineNumber):
            if(node1[1]==lineStore[x][1] and node2[1]==lineStore[x][2]):
                temp = x+1
        #make sure that the connection is not made already
        #else make the connection
        if(temp==0):
            x_transfer = (node2[2] + node1[2])/2
            y_transfer = (node1[3] + node2[3])/2
            addNode(draw,x_transfer,y_transfer,master)
            for x in range(number_of_nodes):
                if(btnStore[x]!=0):
                    if(btnStore[x][2==x_transfer] and btnStore[x][3]==y_transfer):
                        node3 = btnStore[x]
            tempStore = [draw.create_line(node1[2], node1[3], node2[2], node2[3]), node1[1], node2[1]]
            lineStore.insert(lineNumber,tempStore)
            lineNumber = lineNumber+1
            selectOutput(node1[1])
            selectOutput(node2[1])

def addWidget(input):
    #set the clickOperation variable
    global clickOperation
    clickOperation = input


def clickEvent(event):
    #on button press perform an action based on click clickOperation
    global clickOperation
    x = draw.canvasx(event.x)
    y = draw.canvasy(event.y)
    if(clickOperation==1):
        addNode(event.widget, x, y, master)
        clickOperation=0

    if(clickOperation==2):
        addOutput(event.widget, x, y, master)
        clickOperation=0

"""
Below you will find the basic setup of the grid

-------------------------------------------------------- Grid interface setup and initialization --------------------------------------------------------
"""
# creating Tk window
master = Tk()
master.configure(background="gray")
master.title("Delivery Demo")
#set initial size
master.geometry("1000x500")

#create a grid which can reize with the resizing of the box
Grid.rowconfigure(master, 0, weight=1)
Grid.columnconfigure(master, 0, weight=1)
masterFrame = Frame(master)
masterFrame.grid(row=0, column=0, sticky=N+S+E+W)
Grid.rowconfigure(masterFrame, 0, weight=1)
Grid.rowconfigure(masterFrame, 1, weight=100)
Grid.columnconfigure(masterFrame, 0, weight=100)
Grid.columnconfigure(masterFrame, 1, weight=1)

#seperating the menu in different frames which will hold all the components so that it is easier to use .grid for button placemant
#main menu is for the upper buttons, canvas is for draw, subMenu is for the component selection
mainMenu = Frame(masterFrame, bg="gray")
canvas = Frame(masterFrame, bg="white")
subMenu = Frame(masterFrame, bg="gray")

#set each frame in the grid
mainMenu.grid(row=0,sticky=N+S+E+W)
canvas.grid(row=1, sticky=N+S+E+W)
subMenu.grid(row=0, column=1, rowspan=2, sticky=N+S+E+W)

#create a canvas called draw in the canvas frame
draw = Canvas(canvas, bg="white")
draw.pack(fill="both", expand=True)

#bind functions to events
initMainMenu(mainMenu, draw)
initSubMenu(subMenu)

#set the draw canvas with the scroll and pan option
unit = Zoom_Advanced(draw)
#bind button Release to the clickevent
unit.canvas.bind("<ButtonRelease-1>",clickEvent)
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
# canvas aanmaken en even een proef of concept hardcode op het scherm
#w = Canvas(master, width=1000, height=600)
#w.pack()
#initialize_display(w,master)


# label widget
# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
mainloop()
