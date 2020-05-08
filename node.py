def removeNodeCall(draw,master,number_of_nodes,btnStore,lineStore,lineNumber):

    node = 0
    #removing last node
    #check if their is atleast 1 node
    if(number_of_nodes>0):
        #update the number of nodes
        for x in range(number_of_nodes):
            if(btnStore[x]!=0):
                #check the colors the find the specific transfer
                if(btnStore[x][1].cget('bg')=="lime"):
                    #print(b_view[x])
                    #print(b_view)
                    #print(x)
                    node = btnStore[x][1]
                    #delete it from the canvas and set it to 0 in btnStore
                    draw.delete(btnStore[x][0])
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
                if(lineStore[x][3] ==  node):
                    print("x: ",x," is deleted")
                    draw.delete(lineStore[x][0])
                    lineStore[x]=0
    
    return number_of_nodes, btnStore, lineStore, lineNumber