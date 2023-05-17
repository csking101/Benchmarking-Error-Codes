#import matlab
#import matlab.engine
#import numpy as np
#eng = matlab.engine.start_matlab()


def ImpulseNoise(binary_data,p):
    noisy_data = eng.impulse_noise(matlab.single(binary_data),matlab.double(p))
    noisy_data  = np.asarray(noisy_data)
    noisy_data = noisy_data.flatten().astype(int)
    print(noisy_data)

def RayleighFading(binary_data):
    noisy_data = eng.rayleigh(matlab.single(binary_data))
    noisy_data  = np.asarray(noisy_data)
    noisy_data = noisy_data.flatten().astype(int)
    print(noisy_data)

def RicianFading(binary_data):
    noisy_data = eng.rician(matlab.single(binary_data))
    noisy_data  = np.asarray(noisy_data)
    noisy_data = noisy_data.flatten().astype(int)
    print(noisy_data)
# RicianFading([0 for _ in range(100)])\

def AWGN(binary_data,snr):
    noisy_data = eng.awgn_noise(matlab.single(binary_data),matlab.double(snr))
    noisy_data  = np.asarray(noisy_data)
    noisy_data = noisy_data.flatten().astype(int)
    print(noisy_data)
