import scipy.io as sio
import math
import networkx as nx
import numpy as np
import copy

def  readFile(fileLocation):
    mat = sio.loadmat(fileLocation)
    NG = mat['netw']['adjacencyG'][0][0]
    NR = mat['netw']['adjacencyR'][0][0]
    NH = mat['netw']['adjacencyH'][0][0]

    print("adjacency matrix of NG: \n",NG,"")
    print("adjacency matrix of NR: \n",NR,"")
    print("adjacency matrix of NH: \n",NH,"")

    return NG, NR, NH

def toAdjacencyMatrixCall(draw,master,overlay,storeNG,storeNH,storeNR,lineStore,lineNumber,outputStore,outputNumber,excitationStore,excitationNumber,noiseNodeStore,noiseNodeNumber,KnownNodes,noiseNumber):
    NG = []
    NR = []
    NH = []
    KnownNodes = []
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
        KnownNodes.append(0)
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
                        for a in range(outputNumber):
                            if(outputStore[a]!=0):
                                nodeA = outputStore[a][1]
                                if(nodeA==nodeB):
                                    print(x)
                                    print(nodeB.nmb)
                                    NG[x][nodeB.nmb-1] = 1

            if(currentOutput.stat==3):
                KnownNodes[x]=1

            if(overlay==1):
                print("noisenodeNumber")
                print(noiseNodeNumber)
                for y in range(lineNumber):
                    if(lineStore[y]!=0):
                        if(lineStore[y][2]==currentOutput):
                            nodeB = lineStore[y][1]
                            for a in range(noiseNodeNumber):
                                if(noiseNodeStore[a]!=0):
                                    if(nodeB == noiseNodeStore[a][1]):
                                        NH[x][nodeB.nmb-1] = 1
                NR = storeNR
            else:
                NH = storeNH
                NR = storeNR

    if(len(NH)==0):
        NH = []
        for x in range(outputNumber):
            new = []
            for y in range(outputNumber):
                if(x==y):
                    new.append(1)
                else:
                    new.append(0)
            NH.append(new)
    if(len(NR)==0):
        NR = []
        for x in range(outputNumber):
            new = []
            for y in range(outputNumber):
                if(x==y):
                    new.append(1)
                else:
                    new.append(0)
            NR.append(new)
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
    print("KnownNodes is generated as following:")
    print(KnownNodes)

    return NG, NR, NH, outputNumber, outputStore, KnownNodes

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
        pos = nx.kamada_kawai_layout(plot, scale=setScale, center=(500,500))
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

    test = nx.shortest_path(plot,source=0)
    print("shortest find path: ",test)
    return pos

def graphShortestPath(NG,nodeSearchList):

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
    path = nx.shortest_path(plot,source=nodeSearchList[0][1].nmb-1,target=nodeSearchList[1][1].nmb-1)

    return path


def graphDisjointPath(NG, group1, group2, operation):

    nmbOutputs = len(NG)
    nmbOutputs2 = len(NG[0])

    #operation depicts if the minimum disconnected set should be located (operation==0) or the disjoint path (operation==1)

    #below function will read through the mat file and try to find how many modules their are

    #using the network functions create a direction graph (nodes with a connection with a direction so connection 1 to 2 has a direction and is not the same as 2 to 1)
    plot = nx.DiGraph()
    plot.add_nodes_from(range(nmbOutputs))

    for x in range(nmbOutputs):
        for y in range(nmbOutputs2):
            if(NG[x][y]==1):
                plot.add_edge(y,x)

    plot.add_node(nmbOutputs)
    plot.add_node(nmbOutputs+1)
    for x in group1:
        plot.add_edge(nmbOutputs,x[1].nmb-1)

    for x in group2:
        plot.add_edge(x[1].nmb-1,nmbOutputs+1)

    if(operation):
        result = list(nx.node_disjoint_paths(plot,nmbOutputs,nmbOutputs+1))
    else:
        result = list(nx.minimum_node_cut(plot,nmbOutputs, nmbOutputs+1))

    return result

def treeAllocation(treeStore):
    amountTree = len(treeStore)
    mergeMatrix = []
    for x in range(amountTree):
        new = []
        for y in range(amountTree):
            if y == x:
                new.append(0)
            else:
                new.append(2)
        mergeMatrix.append(new)


    #here the difficult shit happens
    #take a pseudo tree
    masterTree = 0
    for unit in treeStore:
        #print("create merge matrix for row pseudo tree:",unit)
        #take in line in that tree
        for line in unit[3]:
            #print("checking at:",line[0])
            #print("checking line:",line,"in:",unit[2])
            #check if a node it connects to belongs in that tree
            if line[2] not in unit[2] or line[2]!=unit[1]:
                #print(line[2].nmb,"not in unit[2] or unit[1]")
                #if it does not check which tree it connects
                slaveTree = 0
                for targetUnit in treeStore:
                    if targetUnit!=unit:
                        #loop through all tree
                        #check if a node is in this tree and mark it
                        #print("scanning in: ",targetUnit)
                        #print("check line from:",line[1].nmb,"to",line[2].nmb,"with",targetUnit[1].nmb,"while working tree",unit[0],masterTree,slaveTree)
                        if line[2] == targetUnit[1] or line[2] in targetUnit[2]:
                            #now we will check if it is mergable
                            mergeMatrix[masterTree][slaveTree] = checkMerge(unit,targetUnit)
                    slaveTree += 1
        masterTree += 1

    print("found mergeMatrix:")
    for x in mergeMatrix:
        print(x)

    return mergeMatrix

def mergeTree(masterTree, slaveTree):
    tempUnit = []
    tempUnit.append(masterTree[0])
    tempUnit.append(masterTree[1])
    tempUnit.append([])
    tempUnit.append([])
    tempUnit.append([])
    for x in masterTree[2]:
        tempUnit[2].append(x)

    for x in masterTree[3]:
        tempUnit[3].append(x)

    check_root = 0
    tempUnit[3].extend(slaveTree[3])

    for line in tempUnit[3]:
        if line[2] == slaveTree[1] and line[1] == masterTree[1]:
            check_root += 1
        if line[1] == slaveTree[1] and line[2] == masterTree[1]:
            check_root += 1

    if check_root == 2:
        tempUnit[4].extend(slaveTree[1])
    tempUnit[2].append(slaveTree[1])
    tempUnit[2].extend(slaveTree[2])


    return tempUnit

def checkMerge(unit,targetUnit):
    tempUnit = mergeTree(unit, targetUnit)

    #now check if correct tree
    #print("checking tree:",unit[0],"as head merge with",targetUnit[0])
    out = checkIfTree(tempUnit)
    return out

def checkIfTree(tempUnit):
    #check if no line go to the same node (this means a node has 2 inputs or more)
    for firstLine in tempUnit[3]:
        for secondLine in tempUnit[3]:
            if firstLine[2] == secondLine[2] and firstLine != secondLine:
                #print("tree not mergable because of multiple input")
                return 0
    #check root node
    totalNode = [tempUnit[1]]
    totalNode.extend(tempUnit[2])
    seenNodes = [tempUnit[1]]
    currentNode = [tempUnit[1]]
    nextNode = []
    while(currentNode!=[]):
        for node in currentNode:
            for line in tempUnit[3]:
                if line[1] == node:
                    if line[2] not in seenNodes:
                        nextNode.append(line[2])
                        seenNodes.append(line[2])
        currentNode = nextNode
        nextNode = []


    for checkNode in seenNodes:
        if checkNode not in totalNode:
            #print("tree not mergable because of no direct line from root")
            return 0
        else:
            #print("tree is totally mergable")
            return 1
