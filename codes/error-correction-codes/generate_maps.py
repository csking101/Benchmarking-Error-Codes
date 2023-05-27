import matlab
import matlab.engine
import pickle

eng = matlab.engine.start_matlab()

def get_minimum_m(k):
    m = 1
    while True:
        if 2**m - m - 1 >= k:
            return (2**m-1, 2**m - m - 1)
        m += 1

hammingDict = {}
for k in range(4,1800):
    n,new_k = get_minimum_m(k)
    print(k,n,new_k)
    hammingDict[k] = (n,new_k)

with open('valid_code_length_hamming.pkl','wb') as f:
    pickle.dump(hammingDict,f)

bch_dict = {}
for m in range(13,3,-1):
    n = 2**m - 1
    possible_k = eng.bchnumerr(matlab.double(n))
    for r in range(4,1800):
        if(r > possible_k[0][1]):
            break
        mini = n
        for t in possible_k:
            pk = t[1]
            if pk >= r and pk-r < n:
                k = pk
                mini = pk - r
        k = int(k)
        if(mini !=n):
            bch_dict[r] = (n,k)
            print(r,n,k)


with open('valid_code_length_bch.pkl','wb') as f:
    pickle.dump(bch_dict,f)