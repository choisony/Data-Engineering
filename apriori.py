from itertools import combinations

def make_candidate(freq_itemsets, k):
    candidates = set()
    for itemset1 in freq_itemsets:
        for itemset2 in freq_itemsets:
            union = itemset1 | itemset2
            if len(union) ==k:
                for item in union:
                    if union - {item} not in freq_itemsets:
                        break
                else:
                    candidates.add(union)
    return candidates

def filter(candidates, k, s):
    itemsets_cnt_k = {}
    with open ("groceries.csv","r")as f:
        for line in f:
            basket = line.strip().split(",")
            for comb in combinations(basket,k):
                comb = frozenset(comb)
                if comb in candidates:
                    if comb not in itemsets_cnt_k:
                        itemsets_cnt_k[comb] = 0
                    itemsets_cnt_k[comb] +=1
    freq_itemsets = set(itemset for itemset, cnt in itemsets_cnt_k.items() if cnt>= s)
    return freq_itemsets

######################## S 설정
s= 150

# item 개수 구하기
item_cnt = {}
with open ("groceries.csv","r")as f:
    for line in f:
        basket = line.strip().split(",")
        for item in basket:
            if item not in item_cnt:
                item_cnt[item] =0
            item_cnt[item] +=1

## L1
freq_itemsets = set(frozenset([item]) for item, cnt in item_cnt.items() if cnt>= s)
freq_itemsets_all = freq_itemsets.copy()

k=2
while len(freq_itemsets)>0:
    candidates = make_candidate(freq_itemsets,k)
    freq_itemsets = filter(candidates,k,s)
    freq_itemsets_all |= freq_itemsets
    k+=1


########--Mining Association Rule--########
######무언가를 살때 무언가를 같이 산다 라는것을 알려면 일단 2개이상 산 경우를 봐야한다.

###### 우선 아이템 각각에 접근할 수 있는 배열을 만들어줍니다
freq_itemsets_one = []
for fi in freq_itemsets_all:
    if len(fi)==1:
        for i in fi:
            freq_itemsets_one.append(i)

def assotiation(items,c):
    for i in items:
        conf = 0
        for j in items:
            sup_i_j = 0
            sup_i = 0
            if i!=j:
                ## 아이템 셋에서 support(i)와 support(i | j) 를 계산해줍니다.
                for x in freq_itemsets_all:
                    if i in x:
                        sup_i +=1
                        if j in x:
                            sup_i_j +=1
            if sup_i !=0:
                conf = sup_i_j / sup_i
            if conf >= c:
                print(i,"가 있으면",round(conf*100,1),"% 확률로",j,"가 있다")
    return "end"

print(assotiation(freq_itemsets_one,0.25))