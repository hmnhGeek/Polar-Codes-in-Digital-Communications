import matplotlib.pyplot as plt
from scipy.special import erfc
import numpy as np
import random

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

def run(val):
    ebnodb = val
    R = 1 
    ebno = decibel_to_number(ebnodb)
    variance_of_noise = noise_variance(ebno, R)
    N = 1000 # number of bits of message per block
    blocks = 100
    err = 0

    for j in range(blocks):
        msg = ''
        for i in range(N):
            msg += str(random.choice([0, 1]))

        s = [1-2*int(i) for i in msg]
        r = np.array(s) + np.random.normal(0, variance_of_noise, N)
        
        m_cap = ''
        for i in r:
            if i <=0:
                m_cap += '1'
            else:
                m_cap += '0'
         
        for i in range(len(msg)):
            if msg[i] != m_cap[i]:
                err += 1
    BER_sim = err*(N*blocks)**(-1)
    return BER_sim
    
simulation = np.vectorize(run)

x = np.arange(0.5, 12, 0.5)
y = simulation(x)
yth = TheoreticalBER(x, 1)
plt.plot(x, y, label="Simulation", marker='*')
plt.plot(x, yth, label="Theoretical", marker='o')
plt.legend()
plt.grid()
plt.xlabel(r"$\frac{E_{b}}{N_{o}}$ in dB")
plt.ylabel("BER")
plt.show()
