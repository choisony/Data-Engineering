import math
import mmh3 , random

class BloomFilter:
    def __init__(self, capacity, fp_prob):
        self.capacity = capacity
        self.fp_prob  = fp_prob
        self.bitarray  = 0
        self.n_bits  = math.ceil(-math.log(fp_prob,math.e)* capacity / (math.log(2,math.e)**2))
        self.n_hashs = int(self.n_bits/capacity * math.log(2,math.e))
        self.seeds=[random.randint(0,99999999) for i in range(self.n_hashs)]
        print("비트배열 크기 : ",self.n_bits)
        print("hash function k 개수 :",  self.n_hashs)

    def put(self,item): ##string값 들어온다고 가정
        for i in range(self.n_hashs):
            pos = mmh3.hash(item,self.seeds[i]) % self.n_bits
            self.bitarray |= (1 << pos)

    def test(self,item):
        for i in range(self.n_hashs):
            pos = mmh3.hash(item, self.seeds[i]) % self.n_bits
            if self.bitarray & (1<<pos) == 0:
                return False
        return True


bloom = BloomFilter(15,0.05)

words  = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

for i in words:
    bloom.put(i)


test_words =  ['q','r','s','t','u','v','w','x','y','z','ab','ac','ad','fd','gf',
               'fh','ss','wt','wet','wte','sgd','xcv','hdf','asd','asda','asdlajh','fs','zxc','qtyq','yrr','kgh','vbn','sxxx',
               'sdfs','sdgsd','jgj','kuu','adfqasd','xvxvxv','adasdqwe','zxczxcaksk']
pos = 0
for i in test_words:
    print(i,":",bloom.test(i))
    if bloom.test(i):
        pos+=1


print("false positive 비율 :", pos/len(test_words))  ## false positive 비율