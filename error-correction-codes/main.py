#import math
#import matlab
#import matlab.engine
#eng = matlab.engine.start_matlab()

test_string  = "110010"
m = []              # initialize empty bit array

# loop through each character of the binary string and append to bit array
for char in test_string:
    m.append(int(char))

# BCH

# todo - figure out how to find t automatically
def BCHEncode(m):
    t = 3 # for now this is default
    k = len(m)
    print(t)
    # Calculate the smallest m such that 2^a >= k + t + 1
    a = math.ceil(math.log2(k + t + 1))
    # Calculate n = 2^a - 1
    n = 2**a - 1
    c = eng.bch_encode(matlab.double(m),matlab.double(n),matlab.double(k))
    return (c[0],n,k)

def BCHDecode(code,n,k):
    decoded, cnumerr, ccode = eng.bch_decode(matlab.double(code),matlab.double(n),matlab.double(k),nargout=3)
    print(decoded)
    print(cnumerr)
    print(ccode)

# Reed Solomon Code
# m = bits per symbol
def RSEncode(msg):
    m = 3#Apparenty default
    n = matlab.double(2**m -1)
    k = matlab.double(len(msg))
    code = eng.rs_encode(matlab.double(msg),matlab.double(m),n,k)
    return code[0]

def RSDecode(code,k):
    m = 3#Apparenty default
    n = matlab.double(2**m -1)
    decoded, cnumerr, ccode = eng.rs_decode(matlab.double(code),matlab.double(m),n,k,nargout = 3)
    print(decoded[0])
    print(cnumerr)
    print(ccode[0])

# RSDecode(RSEncode(m,3),3,len(m)\

def Conv213_Encode(msg):
    coded = eng.conv213_encode(matlab.int16(msg))
    print(coded[0])
    return coded[0]

def Conv213_Decode(code,n):
    decoded = eng.conv213_decode(matlab.int16(code),matlab.double(n)) 
    ans = [int(x) for x in decoded[0]]
    print(ans)
    return ans

# Conv213_Decode(Conv213_Encode(m),len(m))