import pipeline

import matlab.engine
eng = matlab.engine.start_matlab()

def hamming_encode(data):
    # Convert input data to MATLAB array
    data = matlab.double(data)

    # Call MATLAB function for Hamming code encoding
    encoded = eng.encode(data,7,4,'hamming/binary')

    # Convert output to Python list
    encoded = list(encoded)

    return encoded

def hamming_decode(encoded):
    # Convert input data to MATLAB array
    encoded = matlab.double(encoded)

    # Call MATLAB function for Hamming code decoding
    decoded = eng.decode(encoded,7,4,'hamming/binary')

    # Convert output to Python list
    decoded = list(decoded)

    return decoded

from pipeline import ErrorCode

class HammingCode(ErrorCode):
    def __init__(self):
        super().__init__()

    def encode(self,data):
        data = matlab.double(data)
        encoded = eng.encode(data,7,4,'hamming/binary')
        encoded = list(encoded)
        return encoded
    
    def decode(self,encoded):
        encoded = matlab.double(encoded)
        decoded = eng.decode(encoded,7,4,'hamming/binary')
        decoded = list(decoded)
        return decoded

hc = HammingCode()

def simple_noise(encoded):
    encoded[0] = 1
    return encoded

hamming_benchmark = pipeline.Benchmark(hc,noises=[simple_noise])

print(hamming_benchmark.message_batches[0].messages)
print(hamming_benchmark.noisy_batches[0][0].messages)
print(len(hamming_benchmark.message_batches))
print(len(hamming_benchmark.noisy_batches))
print(len(hamming_benchmark.noisy_batches[0]))

eng.quit()