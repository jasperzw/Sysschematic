#import test_identifiability
import matlab.engine
eng = matlab.engine.start_matlab()
adj = {"G":0,"H":0,"R":0}
adj["G"] = matlab.double([[1,0,0],[0,1,0],[0,0,1]])
adj["H"] = matlab.double([[1,0,0],[0,1,0],[0,0,1]])
adj["R"] = matlab.double([[1,0,0],[0,1,0],[0,0,1]])
#fixed = 0
#adj, fix = eng.testTable(nargout=2)
a,b,d = eng.test_identifiability(adj,adj,nargout=3)
#print(adj)
print(a,b,d)
