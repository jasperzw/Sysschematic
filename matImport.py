import scipy.io as sio
import math
import networkx as nx
import numpy as np

def  readFile(fileLocation):
    mat = sio.loadmat(fileLocation)
    NG = mat['netw']['adjacencyG'][0][0]
    NR = mat['netw']['adjacencyR'][0][0]
    NH = mat['netw']['adjacencyH'][0][0]

    print("adjacency matrix of NG: \n",NG,"")
    print("adjacency matrix of NR: \n",NR,"")
    print("adjacency matrix of NH: \n",NH,"")

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
