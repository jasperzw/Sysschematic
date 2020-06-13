<<<<<<< HEAD
import test_identifiability
=======
<<<<<<< HEAD
import matlab.engine
eng = matlab.engine.start_matlab()
x = 4.0
y = 8.0

#fixed = 0
adj, fix = eng.testTable(nargout=2)
a,b,d = eng.test_identifiability(adj,fix,nargout=3)
print(adj)
print(a,b,d)
=======
from oct2py import octave
>>>>>>> 1f7721edcf9d466254a7b3e6b83bba26623414e7
>>>>>>> a2808539c840dc764f22a983c35c2c777ef4a92b
