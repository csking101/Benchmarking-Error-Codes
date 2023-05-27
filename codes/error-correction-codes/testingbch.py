import matlab
import matlab.engine

eng = matlab.engine.start_matlab()


def pad_binary_list(binary_string, n):
    padded_string = binary_string.zfill(n)
    return [int(x) for x in padded_string]

def BCHEncode(m):
    l = len(m)
    n = 2**12 -1
    possible_k = eng.bchnumerr(matlab.double(n))
    mini = 2**12 - 1
    for t in possible_k:
        pk = t[1]
        if pk >=l and pk-l < mini:
            k = pk
            mini = pk - l
    string_m = "".join([str(x) for x in m])
    k = int(k)
    new_m = pad_binary_list(string_m,k)
    print(m, new_m)
    c = eng.bch_encode(matlab.double(new_m),matlab.double(n),matlab.double(k))
    return (c[0],n,k)

print(BCHEncode([1,0,1,1,0,0,1,1]))
