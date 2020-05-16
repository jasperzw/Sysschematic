clear all
close all
load('ibm32.mat') %change to matrix you want must be a struct
s = Problem;
values = s.A;
length = 32; %depends on matrix
NG = zeros(length,length);
for x=1:length
    for y=1:length
            NG(x,y)=values(x,y);
            if(NG(x,y)>0)
                NG(x,y)=1;
            end
    end
end
NR = eye(length);
NH = eye(length);
netw = struct;
netw.adjacencyG = logical(NG);
netw.adjacencyR = logical(NR);
netw.adjacencyH = logical(NH);
save('ibm32_unweighed','netw') %Change X into the name of the matrix
