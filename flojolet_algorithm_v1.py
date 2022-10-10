import math, mmh3, random
from tqdm import tqdm
import matplotlib.pyplot as plt

class FM:
    def __init__(self, domain_size):

        self.domain_size = domain_size
        self.n_bits = math.ceil(math.log2(domain_size))
        self.seed = random.randint(0,9999999)
        self.mask = (1<< self.n_bits) -1
        self.r=0

    def put(self, item):
        h = mmh3.hash(item,self.seed) & self.mask
        tmp=0
        r=0
        if h==0: return
        while h & (1<<tmp) == 0: tmp+=1
        r = max(r,tmp)
        return r


fm = FM(1000000)

##-----------------version1 --------------------------------------
tset = set()
x=[]
y=[]
max_size= 0
for i in range(10000):
    fm_size = 0
    item = str(random.randint(0,100000))
    fm_size = fm.put(item)
    max_size = max(max_size,fm_size)
    tset.add(item)
    x.append(len(tset))
    y.append(2**max_size)
    print("version 1 예측 :",2**max_size,'실제 :',len(tset))
plt.scatter(x,y)
plt.plot(x,x,color = "red")
plt.show()
##---------------------------------------------------------------