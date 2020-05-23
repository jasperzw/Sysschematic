import scipy.io as sio
import math
import networkx as nx

def  readFile(fileLocation):
    mat = sio.loadmat(fileLocation)
    NG = mat['netw']['adjacencyG'][0][0]
    NR = mat['netw']['adjacencyR'][0][0]
    NH = mat['netw']['adjacencyH'][0][0]

    print("adjacency matrix of NG: \n",NG,"")
    print("adjacency matrix of NR: \n",NR,"")
    print("adjacency matrix of NH: \n",NH,"")

    return NG, NR, NH

def toAdjecencyMatrixCall(draw,master,overlay,storeNG,storeNH,storeNR,lineStore,lineNumber,outputStore,outputNumber,excitationStore,excitationNumber,noiseNodeStore,noiseNodeNumber):

    NG = []
    NR = []
    NH = []

    #set everything first to zero
    for x in range(outputNumber):
        new = []
        for y in range(outputNumber):
            new.append(0)
        NG.append(new)
        new = []
        for y in range(noiseNodeNumber):
            new.append(0)
        NH.append(new)
        new = []
        for y in range(excitationNumber):
            new.append(0)
        NR.append(new)
    #create NG matrix
    #print(noiseNodeStore)
    for x in range(outputNumber):
        if(outputStore[x]!=0):
            currentOutput = outputStore[x][1]
            #check for connections to create NG
            for y in range(lineNumber):
                #print("now scanning for node: ",x," at linestore: ",lineStore[y]," for button: ",currentOutput)
                if(lineStore[y]!=0):
                    if(lineStore[y][2]==currentOutput):
                        #found a lineconnection to currentOutput
                        nodeB = lineStore[y][1]
                        #print(nodeB.nmb)
                        NG[x][nodeB.nmb] = 1


            if(overlay==1):
                for y in range(lineNumber):
                    if(lineStore[y]!=0):
                        if(lineStore[y][2]==currentOutput):
                            nodeB = lineStore[y][1]
                            for a in range(noiseNodeNumber):
                                if(noiseNodeStore[a]!=0):
                                    if(nodeB == noiseNodeStore[a][1]):
                                        print(nodeB.nmb)
                                        NH[x][nodeB.nmb] = 1
            else:
                NH = storeNH

            for y in range(excitationNumber):
                if(excitationStore[y]!=0):
                    if(excitationStore[y][4]==currentOutput):
                        excitation = excitationStore[y][1]
                        nmb = int(excitation.nmb)
                        NR[x][nmb] = 1

    storeNG = NG
    storeNR = NR
    storeNH = NH

    print("NG is generated as following:")
    for value in storeNG:
        print(value)
    print("NR is generated as following:")
    for value in storeNR:
        print(value)
    print("NH is generated as following:")
    for value in storeNH:
        print(value)

    return NG, NR, NH

def generateGraph(NG,NH,NR, typeGraph, setScale, layoutMethod):

    nmbOutputs = len(NG)
    nmbOutputs2 = len(NG[0])
    #below function will read through the mat file and try to find how many modules their are

    #using the network functions create a direction graph (nodes with a connection with a direction so connection 1 to 2 has a direction and is not the same as 2 to 1)
    plot = nx.DiGraph()
    plot.add_nodes_from(range(nmbOutputs))

    for x in range(nmbOutputs):
        for y in range(nmbOutputs2):
            if(NG[x][y]==1):
                plot.add_edge(y,x)

    print("number of nodes: ", plot.number_of_nodes() ," number of edges: ", plot.number_of_edges())

    pos = []

    typeGraph = layoutMethod.get()
    #creating coordinates
    #the below functions can be chosen and generate position for the network and return them
    if(typeGraph=="circular"):
        pos = nx.circular_layout(plot,scale=setScale,center=(500,500))
        print("circular layout")
    if(typeGraph=="kamada_kawai"):
        pos = nx.kamada_kawai_layout(plot, scale=setScale, center=(500,500), dim=2)
        print("kamada_kawai layout")
    if(typeGraph=="spring"):
        pos = nx.spring_layout(plot, scale=setScale, center=(500,500))
        print("spring layout")
    if(typeGraph=="spectral"):
        pos = nx.spectral_layout(plot, scale=setScale, center=(500,500))
        print("spectral layout")
    if(typeGraph=="spiral"):
        pos = nx.spiral_layout(plot, scale=setScale, center=(500,500))
        print("spiral layout")

    return pos
