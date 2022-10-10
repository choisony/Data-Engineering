import math, mmh3, random
from tqdm import tqdm
import matplotlib.pyplot as plt

class FM:
    def __init__(self, domain_size):
        self.bitarray = 0
        self.domain_size = domain_size
        self.n_bits = math.ceil(math.log2(domain_size))
        self.seed = random.randint(0,9999999)
        self.mask = (1<< self.n_bits) -1

    def put(self, item):
        h = mmh3.hash(item,self.seed) & self.mask
        r=0
        if h==0: return
        while h & (1<<r) == 0: r+=1
        self.bitarray |= (1<<r)

    def size(self):
        R = 0
        while(self.bitarray & (1<<R) != 0):R+=1
        return 2**R / 0.77351

fm1 = FM(1000000)
fm2 = FM(1000000)
fm3 = FM(1000000)
fm4 = FM(1000000)
fm5 = FM(1000000)
fm6 = FM(1000000)
fm7 = FM(1000000)
fm8 = FM(1000000)
fm9 = FM(1000000)
fm10 = FM(1000000)
fm11 = FM(1000000)
fm12 = FM(1000000)
fm13 = FM(1000000)
fm14 = FM(1000000)
fm15 = FM(1000000)

##-----------------version2, with 5 group--------------------------------------
x_2=[]
y_2=[]
tset_2= set()
for i in range(20000):
    item = str(random.randint(0,100000))
    g1 = []
    g2 = []
    g3 = []
    g4 = []
    g5 = []
    fm1.put(item)
    fm2.put(item)
    fm3.put(item)  ## 1 group
    fm4.put(item)
    fm5.put(item)
    fm6.put(item)  ## 2 group
    fm7.put(item)
    fm8.put(item)
    fm9.put(item)  ## 3 group
    fm10.put(item)
    fm11.put(item)
    fm12.put(item)  ## 4 group
    fm13.put(item)
    fm14.put(item)
    fm15.put(item)  ## 5 group
    g1.append(fm1.size())
    g1.append(fm2.size())
    g1.append(fm3.size())
    g1.sort()
    center_1 = g1[1]
    g2.append(fm4.size())
    g2.append(fm5.size())
    g2.append(fm6.size())
    g2.sort()
    center_2 = g2[1]
    g3.append(fm7.size())
    g3.append(fm8.size())
    g3.append(fm9.size())
    g3.sort()
    center_3 = g3[1]
    g4.append(fm10.size())
    g4.append(fm11.size())
    g4.append(fm12.size())
    g4.sort()
    center_4 = g4[1]
    g5.append(fm13.size())
    g5.append(fm14.size())
    g5.append(fm15.size())
    g5.sort()
    center_5 = g5[1]
    center_avg_2 = math.ceil((center_1+center_2+center_3+center_4+center_5)/5)
    tset_2.add(item)
    x_2.append(len(tset_2))
    y_2.append(center_avg_2)
    print("version 2 with 5 group 예측 :",center_avg_2,'실제 :',len(tset_2))
plt.scatter(x_2,y_2)
plt.plot(x_2,x_2,color = "red")
plt.show()
##---------------------------------------------------------------
