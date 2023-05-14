def encode(data):
    # Convert input data to MATLAB array
    data = matlab.double(data)

    # Call MATLAB function for Hamming code encoding
    encoded = eng.encode(data,7,4,'hamming/binary')

    # Convert output to Python list
    encoded = list(encoded)

    return encoded

def decode(encoded):
    # Convert input data to MATLAB array
    encoded = matlab.double(encoded)

    # Call MATLAB function for Hamming code decoding
    decoded = eng.decode(encoded,7,4,'hamming/binary')

    # Convert output to Python list
    decoded = list(decoded)

    return decoded