import random
import matlab
import matlab.engine
import numpy as np

eng = matlab.engine.start_matlab()
MESSAGES = []

def generate_messages(no_messages: int = 30,max_length: int = 50):
    for _ in range(no_messages):
        MESSAGES.append([random.randint(0,1) for __ in range(4,random.randint(4,max_length))])

def pad_binary(binary_string, n):
    padded_string = binary_string.zfill(n)
    return padded_string

def pad_message():
    global MESSAGES
    MESSAGES = [pad_binary(message,64) for message in MESSAGES]

def print_messages():
    for message in MESSAGES:
        print(message,len(message))
    print()

def hamming_encode(data,n,k):
    # Convert input data to MATLAB array
    data = matlab.double(data)

    # Call MATLAB function for Hamming code encoding
    encoded = eng.encode(data,n,k,'hamming/binary')

    # Convert output to Python list
    encoded = np.asarray(encoded).astype(int).flatten().tolist()

    return encoded

def hamming_decode(encoded,n,k):
    # Convert input data to MATLAB array
    encoded = matlab.double(encoded)

    # Call MATLAB function for Hamming code decoding
    decoded = eng.decode(encoded,n,k,'hamming/binary')

    # Convert output to Python list
    decoded = np.asarray(decoded).astype(int).flatten().tolist()

    return decoded

def RayleighFading(binary_data):
    noisy_data = eng.rayleigh(matlab.single(binary_data))
    noisy_data  = np.asarray(noisy_data)
    noisy_data = noisy_data.flatten().astype(int)
    return noisy_data.tolist()

if __name__ == "__main__":
    for m in range(3,12):
        n = 2**m - 1
        k = n - m
        message = [random.randint(0,1) for _ in range(k)]
        # print(f'Message = {message}')
        # encode
        encoded = hamming_encode(message,n,k)
        # print(f'Encoded = {encoded}')
        # modulation and apply noise function
        recieved_data = RayleighFading(encoded)
        # print(f'Recieved = {recieved_data}')
        # print(eng.biterr(matlab.single(encoded), matlab.single(recieved_data)))
        # decoding
        decoded = hamming_decode(recieved_data,n,k)
        # print(f'Decoded = {decoded}')
        print(eng.biterr(matlab.single(message), matlab.single(decoded)))

# print(calculate_n(11))