import math
from scipy.special import erfc
import random
import numpy as np
import matplotlib.pyplot as plt

def GaussianPDF(x):
    return (1/math.sqrt(2*math.pi))*math.e**((-x**2)/2)

def dbtoratio(db_val):
    return 10**(db_val*0.1)

def AWGN_Noise_Variance(ebnodb, R):
    return math.sqrt(1/(2*R*dbtoratio(ebnodb)))

def BER(ebono):
    return 0.5*erfc(math.sqrt(ebono))

def intersect(arr1, arr2):
    l=[]
    for i in range(len(arr1)):
        if arr1[i] == arr2[i]:
            l.append(0)
        else:
            l.append(1)

    return l

if __name__ == '__main__':
    EbNodB = 10.5
    R = 1 # for uncoded BPSK

    N = 1000 # no of bits of message per block
    Nerrs = 0
    Nblocks = 10000
    
    for j in range(Nblocks):
        msg = []
        for i in range(N):
            msg.append(random.choice([0, 1]))

        # generate a BPSK
        s = [1-2*i for i in msg]

        # generate the signal in the channel.
        sigma = math.sqrt(1/(2*R*dbtoratio(EbNodB)))
        r = np.array(s) + sigma*np.random.normal(0, 1, N)

        # message cap
        msg_cap = []

        for i in r:
            if i < 0:
                msg_cap.append(1)
            else:
                msg_cap.append(0)

        msg_cap = np.array(msg_cap)
        Nerrs = Nerrs + sum(intersect(msg_cap, msg))

    BER_sim = Nerrs/N
    BER_sim /= Nblocks
    print("Theoretical BER = {}".format(BER(dbtoratio(EbNodB))))
    print("Simulation based BER = {}".format(BER_sim))
    print("Number of errors = {}".format(Nerrs))
    print("Total transmissions = {}".format(N*Nblocks))
        
