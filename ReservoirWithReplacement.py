import random
from matplotlib import pyplot as plt

class ReservoirWithReplacement:
    def __init__(self, k):
        self.sampled = [[0] for i in range(k)] ## k개만큼 배열 만들어줌
        self.k = k
        self.cnt  = 0

    def put(self, item): ##item 은 복원추출이므로 (0~999)에서 매번 랜덤으로 추출할거임
        if self.cnt <self.k:
            self.sampled[self.cnt][0] = item
        else:
            r = random.randint(0, self.cnt)
            if r <self.k:
                self.sampled[r][0] = item
        self.cnt+=1

count_replacement = [0]*1000
time_replacement = 0
for _ in range(10000):
    r = ReservoirWithReplacement(100)
    for i in range(1000):  #### 0~999의 숫자를 랜덤으로 복원추출해주는것(1000번 반복)
        replacement_item = random.randint(0,999)
        r.put(replacement_item)
    for j in r.sampled:
        count_replacement[j[0]]+=1
    time_replacement +=1
    print(time_replacement,"번째 시행")

print("Count_replacement 배열:",count_replacement)
plt.plot([i for i in range(1000)],count_replacement)
plt.show()
