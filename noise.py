#from tkinter import *
#from var import outputNumber, outputStore, noiseStore, noiseNumber

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


def addNoise(master, draw):
    global outputStore
    global outputNumber
    global noiseNumber
    global noiseStore

    switch = 0
    node = 0
    for x in range(outputNumber):
        print(outputStore[x])
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

def removeNoise(master, draw):
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
