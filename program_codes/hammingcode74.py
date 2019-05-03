import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc
import random

'''
    This script generates the BER vs. Eb/N0 plot for hamming code.
'''

codewords = {'0000':'0000000',
             '0001':'0001011',
             '0010':'0010110',
             '0101':'0101100',
             '1011':'1011000',
             '0110':'0110001',
             '1100':'1100010',
             '1000':'1000101',
             '0100':'0100111',
             '1001':'1001110',
             '0011':'0011101',
             '0111':'0111010',
             '1110':'1110100',
             '1101':'1101001',
             '1010':'1010011',
             '1111':'1111111'
             }

inv_code = dict(zip(codewords.values(), codewords.keys()))

def Q(x):
    return 0.5*erfc(x*2**(-0.5))

def voltage(bin_stream, high, low):
    s = []
    for i in bin_stream:
        if i == 1:
            s.append(high)
        else:
            s.append(low)
    return np.array(s)

def noise_variance(ebno, R):
    return (2*R*ebno)**(-0.5)

noise_variance = np.vectorize(noise_variance)

def count(num):
    c = 0
    for i in num:
        if i == '1':
            c += 1
    return c

def hard_decision(vector):
    r = ''
    for i in vector:
        r += str(i)

    distance = 1000
    cap_val = 0000
    for i in inv_code:
        val = int(i, 2)^int(r, 2)
        val = np.binary_repr(val, 8)
        if count(val) < distance:
            distance = count(val)
            cap_val = i
    return cap_val

def calc_ber(decision, message):
    message = [str(i) for i in message]
    message = ''.join(message)
    val = int(message, 2)^int(decision, 2)
    val = np.binary_repr(val, 8)
    val = count(val)
    return val*len(decision)**(-1)

def find_voltage(sequence):
    l = []
    for i in sequence:
        if i == '0':
            l.append(1)
        else:
            l.append(-1)
    return np.array(l)

def soft_decision(vector):
    distance = -1000.0
    cap_val = 0
    for i in inv_code:
        v = find_voltage(i)
        vector = np.array(vector)
        dotproduct = np.dot(v, vector)
        if dotproduct > distance:
            distance = dotproduct
            cap_val = i
    return cap_val

def hamming(ebnodb):
    R = 4.0/7.0
    ebno = 10**(ebnodb*0.1)
    variance = noise_variance(ebno, R)
    sigma = np.sqrt(1/(2*R*ebno))

    k, n = 4, 7

    msg = []
    for i in range(k):
        msg.append(random.choice([0,1]))

    msg.append((msg[0]+msg[1]+msg[2])%2)
    msg.append((msg[1]+msg[2]+msg[3])%2)
    msg.append((msg[0]+msg[1]+msg[3])%2)

    voltages = voltage(msg, -1, 1)
    noise = np.random.normal(0, variance, n)

    r = voltages + noise
    r_cap = []
    for i in r:
        if i <= 0:
            r_cap.append(1)
        else:
            r_cap.append(0)

    # hard decision
    d1 = hard_decision(r_cap)
    ber1 = calc_ber(d1, msg)

    # soft decision
    d2 = soft_decision(r)
    ber2 = calc_ber(d2, msg)

    return ber1, ber2

h = np.vectorize(hamming)

def plot():
    ebnodb = np.arange(0, 2, 0.01)
    y1, y2 = h(ebnodb)

    plt.stem(ebnodb, y1, 'b', markerfmt='bo', label ="Hard Decision")
    plt.stem(ebnodb, y2, 'g', markerfmt='go', label = 'Soft Decision')
    plt.legend()
    plt.grid()
    plt.xlabel("Eb/No in dB")
    plt.ylabel("BER (linear scale)")
    plt.show()
plot()
