#from tkinter import *
#from var import outputNumber, outputStore

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
                img1Btn.image.text = str(m)

        outputStore.append(save)
        outputNumber = outputNumber + 1


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
