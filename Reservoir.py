import random
from matplotlib import pyplot as plt

class Reservoir:
    def __init__(self, k):
        self.sampled = []
        self.k = k
        self.cnt  = 0

    def put(self, item):
        if self.cnt <self.k:
            self.sampled.append(item)
        else:
            r = random.randint(0, self.cnt)
            if r <self.k:
                self.sampled[r] = item
        self.cnt+=1

count= [0]*1000
time =0
for _ in range(10000):
    r = Reservoir(100)
    for i in range(1000):
        r.put(i)
    for i in r.sampled:
        count[i] +=1
    time+=1

    print(time,"번째 시행")

plt.plot([i for i in range(1000)],count)
print("Count 배열: ",count) ##0~999가 몇번 추출되었는지 count 해준 배열
plt.show()