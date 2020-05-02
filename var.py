# declare is unnecessary since they are declared in the upper script outside any function
def init():
    global number_of_nodes
    global btnStore
    global lineStore
    global lineNumber
    global outputStore
    global noiseStore
    global connect
    global noiseNumber
    global outputNumber

    number_of_nodes = 0
    btnStore = []
    lineStore = [[]]
    lineNumber = 0
    outputStore = []
    noiseStore = []
    connect = []
    noiseNumber = 0
    outputNumber = 0
