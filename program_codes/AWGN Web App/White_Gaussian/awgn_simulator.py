import matplotlib.pyplot as plt
from scipy.special import erfc
import numpy as np
import random
import textwrap3
import os

# this is a Q function.
def Q(x):
    return 0.5*erfc(x*2**(-0.5))

def decibel_to_number(db_val):
    return 10**(db_val*0.1)

def noise_variance(eboverno, R):
    return (2*R*eboverno)**(-0.5)

def Bit_Error_Rate(eboverno, R):
    return Q(noise_variance(eboverno, R)**(-1))

TheoreticalBER = np.vectorize(Bit_Error_Rate)
db_to_num = np.vectorize(decibel_to_number)

def plot_graph():
    x_scale = np.arange(0, 12, 0.001)
    x = db_to_num(x_scale)
    y_scale = TheoreticalBER(x, 1)

    plt.plot(x_scale, y_scale)
    plt.show()

# Uncoded BPSK hence R=1.

def convert_ascii(message):
    """
        This function converts a message stream to binary numbers with each character represented
        by 8 bit ASCII code.
    """
    string = ''

    for i in message:
        string += np.binary_repr(ord(i), 8)

    return string

def convert_back(value):
    """
        This function converts a given 8 bit ASCII to its equivalent character.
    """
    value = textwrap3.wrap(value, 8)
    alphabets = []
    for i in value:
        alphabets.append(chr(int(i, 2)))
    return ''.join(alphabets)

def init_simulator(ebvsno, rate, msg):
    plt.cla()
    msg = convert_ascii(msg)
    ebnodb = ebvsno
    R = rate
    ebno = decibel_to_number(ebnodb)
    variance_of_noise = noise_variance(ebno, R)
    N = len(msg) # number of bits of message per block
    err = 0

    s = [1-2*int(i) for i in msg] # converts 0 to 1 and 1 to -1.
    n = np.random.normal(0, variance_of_noise, N)
    r = np.array(s) + n # add AWGN to message s.
    
    m_cap = ''
    for i in r:
        if i <=0:
            m_cap += '1'
        else:
            m_cap += '0'

    # m_cap is the recieved message in 1 and 0 form.
     
    for i in range(len(msg)):
        if msg[i] != m_cap[i]:
            err += 1
    # err stores the flipped number of bits.
    
    BER_sim = err*N**(-1)
    received = convert_back(m_cap)
    noise_graph = plt.plot(n)

    cwd = os.getcwd()
    os.chdir('static')
    plt.savefig('noise.png')
    os.chdir(cwd)

    return BER_sim, received, Bit_Error_Rate(ebno, R)
    
simulation = np.vectorize(init_simulator)


