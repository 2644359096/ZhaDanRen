import torch
x1 = torch.rand(4, 3)
x2= torch.ones(4,3,dtype=torch.long)
x3 = torch.tensor([333,444])
x4=x1+x2

y1=x1.view(12)
y2=x1.view(-1,4)
print(x1)
print(x2)
print(x3)
print(x4)
print(y1.size(),y2.size(),'\n',y1,'\n',y2)