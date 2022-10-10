import random
from matplotlib import pyplot as plt

class Bucket:
    def __init__(self, start,end):
        self.start = start
        self.end = end
    def __repr__(self):
        return f"({self.start},{self.end})"

class DGIM:
    def __init__(self):
        self.bucket_tower = [[]]
        self.ts = 0

    def put(self, bit):
        if bit == 1:
            self.bucket_tower[0].insert(0,Bucket(self.ts,self.ts))

            layer = 0
            while len(self.bucket_tower[layer]) > 2:
                if len(self.bucket_tower) <= layer+1:
                    self.bucket_tower.append([])
                b1 = self.bucket_tower[layer].pop()
                b2 = self.bucket_tower[layer].pop()
                b1.end =b2.end

                self.bucket_tower[layer+1].insert(0,b1)
                layer+=1
        self.ts +=1

    def count(self, k):
        s = self.ts - k
        cnt = 0
        for layer, buckets in enumerate(self.bucket_tower):
            for bucket in buckets:
                if s <= bucket.start:
                    cnt += (1 << layer) # 2**layer
                elif s <= bucket.end:
                    cnt+= (1 << layer) * (bucket.end -s +1) // (bucket.end -bucket.start+1)
                    return cnt
                else:
                    return cnt
        return cnt

n = [random.randint(0,15) for i in range(10000)]

dgim_1 = DGIM()
dgim_2 = DGIM()
dgim_4 = DGIM()
dgim_8 = DGIM()

n8=[]
n4=[]
n2=[]
n1=[]

for i in n: ####정수 13를 이진수로 표현하면 1101 이다. n8배열에 4번째비트인 1을 넣고
            #### n4 배열에 3번째비트인 1을 넣고,  n2배열에 2번째비트인 0을 넣고, n1배열에 1번째비트인 1을 넣어준다.
    n8.append(int(format(i,'04b')[0]))
    n4.append(int(format(i,'04b')[1]))
    n2.append(int(format(i,'04b')[2]))
    n1.append(int(format(i,'04b')[3]))

for b in n8:
    dgim_8.put(b)
for b in n4:
    dgim_4.put(b)
for b in n2:
    dgim_2.put(b)
for b in n1:
    dgim_1.put(b)
dgim_result = []
real_result = []

for k in range(1,2001):
    first = 8*dgim_8.count(k)+ 4*dgim_4.count(k)+2*dgim_2.count(k)+1*dgim_1.count(k)
    dgim_result.append(first)
    real_result.append(sum(n[-k:]))
    print("k =",k,", 첫번째 방법 합 :", first,", 실제 합 : ",sum(n[-k:]))

plt.plot([i for i in range(1,2001)],real_result,'black')
plt.plot([i for i in range(1,2001)],dgim_result,'r')
plt.show()