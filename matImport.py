import scipy.io as sio
import math
from node import addNode

def  readFile(fileLocation):
    mat = sio.loadmat(fileLocation)
    NG = mat['netw']['adjacencyG'][0][0]
    NR = mat['netw']['adjacencyR'][0][0]
    NH = mat['netw']['adjacencyH'][0][0]

    print("adjacency matrix of NG: \n",NG,"")
    print("adjacency matrix of NR: \n",NR,"")
    print("adjacency matrix of NH: \n",NH,"")

    return NG, NR, NH

def plotMatrix(mat,draw,master,start, lineNumber,lineStore,connect):
    connect = []
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

    set = [lineNumber,lineStore,connect]
    return set
