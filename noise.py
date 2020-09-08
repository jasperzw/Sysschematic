from tkinter import *


def addNoiseNodeCall(draw, x, y, master, noiseNodeNumber, noiseNodeStore, img1Btn,unit,nodeSize):
    #create output
    switch = 0
    node = 0
    size = nodeSize
    #set img1btn as object so that we can add .widget containing the circle id.
    img1Btn.widget = draw.create_circle(x,y,size*unit.currentZoom, fill="yellow", tags="nodes")
    img1Btn.nmb =1
    img1Btn.stat = 1
    img1Btn.zoom = size*unit.currentZoom
    textSize = round((size/2)*unit.currentZoom)
    if(textSize<1):
        textSize = 1

    img1Btn.nodeMode = []

    for i in range(5):
        img1Btn.nodeMode.append(IntVar())
    #use same save technique so that all the functions remain functional
    save = [img1Btn.widget,img1Btn,x,y]

    #earch if their is a empty entry.
    for m in range(noiseNodeNumber):
        if(noiseNodeStore[m]==0):
            node=m
            nmb = draw.create_text(x, y, text="e"+str(m+1),width=0, font=("Courier", textSize),tags="wNotation")
            save.append(nmb)
            save[1].nmb = m
            noiseNodeStore[m] = save
            switch = 1

            #initial output
    if(noiseNodeNumber==0):
        nmb = draw.create_text(x, y, text="e"+str(1),width=0, font=("Courier", textSize),tags="wNotation")
        save.append(nmb)
        noiseNodeStore.append(save)
        noiseNodeNumber = noiseNodeNumber + 1
        switch = 1

    #append if no empty entry
    if(switch==0):
        save[1].nmb=noiseNodeNumber+1
        nmb = draw.create_text(x, y, text="e"+str(noiseNodeNumber+1),width=0, font=("Courier", textSize),tags="wNotation")
        save.append(nmb)
        noiseNodeStore.append(save)
        noiseNodeNumber = noiseNodeNumber + 1

    return noiseNodeNumber, noiseNodeStore

def selectNoiseNodeCall(draw, master, noiseNodeNumber, noiseNodeStore, currentAmountOutputSelected, id,lineNumber,lineStore):
        #each output has a stat variable which indicates state. stat == 1 is not selected, stat == 2 is selected
        #work in progress image swap werkt nog niet
        if(id[1].stat==1):
            id[1].order = currentAmountOutputSelected
            currentAmountOutputSelected = currentAmountOutputSelected + 1
            id[1].stat = 2
            draw.itemconfig(id[0],fill="green")
            #print("buttond found!")
            for a in range(lineNumber):
                if(lineStore[a]!=0):
                    if (id[1]==lineStore[a][1] or id[1]==lineStore[a][2]):
                        draw.itemconfig(lineStore[a][0], fill="red")
        else:
            id[1].order = 0
            currentAmountOutputSelected = currentAmountOutputSelected - 1
            id[1].stat = 1
            draw.itemconfig(id[0],fill="yellow")
            print("buttond found!")
            for a in range(lineNumber):
                if(lineStore[a]!=0):
                    if (id[1]==lineStore[a][1] or id[1]==lineStore[a][2]):
                        draw.itemconfig(lineStore[a][0], fill="black")

        return currentAmountOutputSelected

def removeNoiseNodeCall(noiseNodeStore, noiseNodeNumber, lineStore, lineNumber, draw):
    #search for output and set it to 0

    for x in range(noiseNodeNumber):
        if(noiseNodeStore[x]!=0):
            if(noiseNodeStore[x][1].stat == 2):
                for i in range(lineNumber):
                    #print("i: ",i," lineStore:",lineStore[i],"")
                    if(lineStore[i]!=0):
                        if(lineStore[i][1]==noiseNodeStore[x][1] or lineStore[i][2]==noiseNodeStore[x][1]):
                            #print("i: ",i," is deleted")
                            lineStore[i][1].stat == 2
                            draw.delete(lineStore[i][0])
                            lineStore[i]=0
                draw.delete(noiseNodeStore[x][4])
                draw.delete(noiseNodeStore[x][0])
                noiseNodeStore[x] = 0
    return noiseNodeStore, lineStore, noiseNodeNumber
