import numpy as np
from pyfinite import ffield

def gf_mul(x, y, field):
    """
    Multiply two elements in the Galois Field of characteristic 2.
    """
    if x == 0 or y == 0:
        return 0
    else:
        return field.exp[(field.log[x] + field.log[y]) % (field.modulus - 1)]

def gf_poly_mul(p1, p2, field):
    """
    Multiply two polynomials in the Galois Field of characteristic 2.
    """
    m = len(p1)
    n = len(p2)
    result = np.zeros(m + n - 1, dtype=int)
    for i in range(m):
        for j in range(n):
            result[i+j] ^= gf_mul(p1[i], p2[j], field)
    return result.tolist()

def gf_poly_div(dividend, divisor, field):
    """
    Divide two polynomials in the Galois Field of characteristic 2.
    """
    dividend = np.array(dividend, dtype=int)
    divisor = np.array(divisor, dtype=int)
    remainder = np.copy(dividend)
    quotient = np.zeros(len(dividend) - len(divisor) + 1, dtype=int)
    for i in range(len(dividend) - len(divisor), -1, -1):
        quotient[i] = remainder[i + len(divisor) - 1]
        if quotient[i] != 0:
            remainder[i:i + len(divisor)] ^= gf_poly_mul(divisor, [quotient[i]], field)
    return quotient.tolist(), remainder.tolist()

def gf_poly_eval(poly, x, field):
    """
    Evaluate a polynomial over a finite field at x.
    """
    y = 0
    power = 1
    for coeff in poly:
        y ^= gf_mul(coeff, power, field)
        power = gf_mul(power, x, field)
    return y


def bch_encode(data, t):
    """
    Encode binary data using a BCH code with t-error correction capability.
    """
    n = 2**t - 1
    k = n - t
    field = ffield.FField(t)
    gen = [1]  # generator polynomial
    # calculate generator polynomial using roots of unity
    for i in range(1, 2*t):
        root = field.exp[i]
        gen = gf_poly_mul(gen, [1, root], field)
        if len(gen) > t:
            gen, _ = gf_poly_div(gen, [1, field.exp[t]], field)
    # pad data with zeros
    data = data + [0] * (k - len(data))
    # calculate parity check symbols using generator polynomial
    _, remainder = gf_poly_div(data + [0] * t, gen, field)
    parity = remainder[-t:]
    # return codeword
    return data + parity

def bch_decode(codeword, t):
    """
    Decode binary data using a BCH code with t-error correction capability.
    """
    n = 2**t - 1
    k = n - t
    field = ffield.FField(t)
    gen = [1]  # generator polynomial
    # calculate generator polynomial using roots of unity
    for i in range(1, 2*t):
        root = field.exp[i]
        gen = gf_poly_mul(gen, [1, root], field)
        if len(gen) > t:
            gen, _ = gf_poly_div(gen, [1, field.exp[t]], field)
    # calculate syndrome
    syndrome = np.zeros(t, dtype=int)
    for i in range(t):
        s = 0
        for j in range(n):
            s ^= gf_mul(codeword[j], field.exp[i*j], field)
        syndrome[i] = s
    if sum(syndrome) == 0:
        # no errors detected, return original message
        return codeword[:k]
    else:
        # find error locator polynomial and error evaluator polynomial
        sigma, omega = [1], [0]
        for i in range(1, t+1):
            s = 0
            for j in range(i):
                s ^= gf_mul(sigma[j], syndrome[i-j-1], field)
            sigma.append(s)
            if 2*i <= t:
                s = 0
                for j in range(i):
                    s ^= gf_mul(sigma[j], codeword[i-j-1], field)
                omega.append(s)
        # find error positions and correct errors
        error_positions = []
        for i in range(n):
            if gf_poly_eval(sigma, field.exp[(i+1) % field.modulus], field) == 0:
                error_positions.append(i)
        if len(error_positions) <= t:
            for i in error_positions:
                codeword[i] ^= 1
            # correct errors and return original message
            return codeword[:k]
        else:
            raise Exception("Too many errors to correct.")

print(bch_encode('01010010', 2))

