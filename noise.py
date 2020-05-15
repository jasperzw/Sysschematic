from tkinter import *

def addNoiseNodeCall(draw, x, y, master, noiseNodeNumber, noiseNodeStore, img1Btn):
    #create output
    switch = 0
    node = 0
    img1 = PhotoImage(file="data/excitation.png")

    nmb = Label(master, text="1", bg="yellow")
    img1Btn.configure(image=img1)
    img1Btn.image = img1
    img1Btn.stat = 1
    img1Btn.nmb = 0
    img1Btn.order = 0
    img1Btn["border"] = "0"


    save = [draw.create_window(x, y, window=img1Btn),img1Btn,x,y,draw.create_window(x+10,y+5,window=nmb),nmb]

    #earch if their is a empty entry.
    for m in range(noiseNodeNumber):
        if(noiseNodeStore[m]==0):
            node=m
            nmb.configure(text=str(m+1))
            save[1].nmb = m
            noiseNodeStore[m] = save
            img1Btn.image.text = str(m+1)
            switch = 1

            #initial output
    if(noiseNodeNumber==0):
        noiseNodeStore.append(save)
        noiseNodeNumber = noiseNodeNumber + 1
        switch = 1

    #append if no empty entry
    if(switch==0):
        nmb.configure(text=str(noiseNodeNumber+1))
        save[1].nmb=noiseNodeNumber
        noiseNodeStore.append(save)
        noiseNodeNumber = noiseNodeNumber + 1

    return noiseNodeNumber, noiseNodeStore

def selectNoiseNodeCall(draw, master, noiseNodeNumber, noiseNodeStore, currentAmountOutputSelected, id):
        #each output has a stat variable which indicates state. stat == 1 is not selected, stat == 2 is selected
        #work in progress image swap werkt nog niet
        nmb = 0
        print("current working object ",id)
        #finding corresponding label
        for x in range(noiseNodeNumber):
            if(noiseNodeStore[x]!=0):
                if(noiseNodeStore[x][1]==id):
                    nmb = noiseNodeStore[x][5]


        if(id.stat==1):
            imgGreen = PhotoImage(file="data/excitationKnown.png")
            id.image = imgGreen
            id.stat = 2
            id.order = currentAmountOutputSelected
            currentAmountOutputSelected = currentAmountOutputSelected + 1
            nmb.configure(bg="green")
            id.configure(image=imgGreen)
            print("setting output green")
        else:
            imgWhite = PhotoImage(file="data/excitation.png")
            id.image=imgWhite
            id.stat = 1
            id.order = 0
            currentAmountOutputSelected = currentAmountOutputSelected - 1
            nmb.configure(bg="yellow")
            id.configure(image=imgWhite)
            print("setting output white")

        return currentAmountOutputSelected

def removeNoiseNodeCall(noiseNodeStore, noiseNodeNumber, lineStore, lineNumber, draw):
    #search for output and set it to 0

    for x in range(noiseNodeNumber):
        if(noiseNodeStore[x]!=0):
            if(noiseNodeStore[x][1].stat == 2):
                for i in range(lineNumber):
                    print("i: ",i," lineStore:",lineStore[i],"")
                    if(lineStore[i]!=0):
                        if(lineStore[i][1]==noiseNodeStore[x][1] or lineStore[i][2]==noiseNodeStore[x][1]):
                            print("i: ",i," is deleted")
                            lineStore[i][3]["bg"]="lime"
                            draw.delete(lineStore[i][0])
                            #removeNode(draw, master)
                            lineStore[i]=0
                draw.delete(noiseNodeStore[x][4])
                draw.delete(noiseNodeStore[x][0])
                noiseNodeStore[x] = 0
    return noiseNodeStore, lineStore
