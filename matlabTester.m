f = @(x,y) 2*x^2+y^2-2*x*y + 4*y;

V = [1;2]
W = [4;4]
a = 0.9


first = a*V+(1-a)*W
left = f(first(1),first(2))
right = a*f(V(1),V(2))+(1-a)*f(W(1),W(2))