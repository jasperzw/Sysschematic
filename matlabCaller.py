import matlab.engine

def test_identifiability_caller(NG,NR,NH,fixG,fixR,fixH):
    eng = matlab.engine.start_matlab()
    adj = {"G":0,"R":0,"H":0}
    fix = {"G":0,"R":0,"H":0}

    print("NG: ",NG)
    print("--------------------------------------------------------------------------------------")
    print("NR: ",NR)
    print("--------------------------------------------------------------------------------------")
    print("NH: ",NH)

    fixH = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    adj["G"] = matlab.double(NG)
    adj["R"] = matlab.double(NR)
    adj["H"] = matlab.double(NH)

    fix["G"] = matlab.double(fixG)
    fix["R"] = matlab.double(fixR)
    fix["H"] = matlab.double(fixH)

    identifiability, identifiability_nodes, identifiability_modules =  eng.test_identifiability(adj,fix,nargout=3)

    return identifiability, identifiability_nodes, identifiability_modules

def saveToFile():
    eng = matlab.engine.start_matlab()
    print('Matlab engine started')
    #File of interest
    myBadFile='test.mat'
    #Synchronize python/matlab working directory
    eng.cd(os.getcwd(),nargout=0)
    print(eng.pwd())
    #Read file contents
    VALUES=eng.load(myBadFile,nargout=1)
