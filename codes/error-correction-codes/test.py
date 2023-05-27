import random
import matlab
import matlab.engine
import numpy as np

eng = matlab.engine.start_matlab()

def get_minimum_m(k):
    m = 1
    while True:
        if 2**m - m - 1 >= k:
            return (2**m-1, 2**m - m - 1)
        m += 1

def pad_binary_list(binary_string, n):
    padded_string = binary_string.zfill(n)
    return [int(x) for x in padded_string]

def hamming_encode(data,k):
    # Convert input data to MATLAB array
    n,new_k = get_minimum_m(k)
    padded_data = pad_binary_list(data,new_k)
    encoded = eng.encode(matlab.single(padded_data),matlab.single(n),matlab.single(new_k),'hamming/binary')

    encoded = np.asarray(encoded).astype(int).flatten().tolist()

    return encoded

def hamming_decode(encoded,k):
    # Convert input data to MATLAB array
    n,new_k = get_minimum_m(k)
    encoded = matlab.double(encoded)
    # Call MATLAB function for Hamming code decoding
    decoded = eng.decode(encoded,n,new_k,'hamming/binary')

    # Convert output to Python list
    decoded = np.asarray(decoded).astype(int).flatten().tolist()

    return decoded[-k:]


print(hamming_decode(hamming_encode("10101",5),5))