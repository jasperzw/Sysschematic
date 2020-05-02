
#from var import lineNumber, lineStore, number_of_nodes, btnStore
#from tkinter import *

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
            save = [w.create_window(x, y, window=btn),btn,x,y]
            btnStore.append(save)
            number_of_nodes = number_of_nodes + 1
            print("start initial node")

        else:
            for m in range(number_of_nodes-1):
                if(btnStore[m]==0):
                    node = m
                    btn = Button(master, text = "G"+str(node), command = lambda: selectNode(node) , bg = "cyan")
                    save = [w.create_window(x, y, window=btn),btn,x,y]
                    btnStore[m] = save
                    print("added node in existing place")

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

#            draw.delete(lineStore[temp-1][0])
#            lineStore[temp-1]=0
#            removeNode(draw,master)
