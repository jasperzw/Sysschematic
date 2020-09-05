import matlab.engine

#this function boots up matlab and peforms the network identifiability function
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
