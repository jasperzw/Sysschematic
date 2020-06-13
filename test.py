import matlab.engine
eng = matlab.engine.start_matlab()
x = 4.0
y = 8.0

#fixed = 0
adj, fix = eng.testTable(nargout=2)
a,b,d = eng.test_identifiability(adj,fix,nargout=3)
print(adj)
print(a,b,d)