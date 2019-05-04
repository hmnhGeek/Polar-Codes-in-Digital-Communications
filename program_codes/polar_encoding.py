import numpy as np
import random
import matplotlib.pyplot as plt

'''
    This script also generates BER plot for polar codes but in log scale.
    simulate1() is used to find BER based on message length. simulate2() is
    used to generate BER plot vs Eb/N0.
'''

# reliability sequence for 5G N=16
Q = np.array([1, 2, 3, 5, 9, 4, 6, 10, 7, 11, 13, 8, 12, 14, 15, 16])-1

def encode(N, K, Q):
    if N >= K:
        n = np.log(N)/np.log(2)
        n = int(n)

        # generate a random message of K bits.
        msg = np.random.choice([0, 1], K)
        U = np.array([0]*N)

        temp = Q[N-K::] # according to reliability sequence, generate a sublist of optimum channels.
        for i in range(len(msg)):
            U[temp[i]] = msg[i] # store message bits in U according to the index of the optimum channels, as given by reliability seq.
            
        G2 = np.matrix([[1,0], [1, 1]])
        GN = G2

        # generate a generator matrix using kronecker product.
        for i in range(n-1):
            GN = np.kron(G2, GN)

        C = (U.dot(GN))%2 # modulo 2 product of U with the generator matrix.
        C = C.tolist()[0] # C contains the polar coded stream
        return msg, C
    else:
        return -1

def AWGN(message, ebnodb, R):
    """ This function simulates AWGN noise. """
    ebno = 10**(ebnodb*0.1)
    M = []
    for i in message:
        if i == 0:
            M.append(1)
        else:
            M.append(-1)
    
    noise_var = (2*R*ebno)**(-0.5)

    r = np.array(M) + np.random.normal(0, noise_var, len(message))
    return r.tolist()

def hard_decision(r):
    dec = []

    for i in r:
        if i <= 0:
            dec.append(1)
        else:
            dec.append(0)

    return dec

def decode(C, Q, N, K):
    n = int(np.log(N)/np.log(2))
    G2 = np.matrix([[1,0], [1, 1]])
    GN = G2

    for i in range(n-1):
        GN = np.kron(G2, GN)

    GinvN = np.linalg.inv(GN) # generate the inverse of the generator matrix so that we can retrieve the message back.
    C = np.matrix(C)

    D = C.dot(GinvN) % 2 # modulo 2 multiplication
    D = D.tolist()[0]
    D = [int(i) for i  in D]
    temp = Q[N-K::] # index of the message starts after N-K bits in the Q because we encoded it in that way.

    msg = []
    for i in temp:
        msg.append(D[i]) # append bits to msg according to the index given by temp.
    return msg

def calcBER(N, K, ebnodb):
    message, codeword = encode(N, K, Q)

    # pass through AWGN
    r = AWGN(codeword, ebnodb, K*N**(-1))

    # make decision
    C = hard_decision(r)

    # find the actual message
    m_cap = decode(C, Q, N, K)
    errors = 0

    for i in range(len(message)):
        if message[i] != m_cap[i]: # find the flipped bits.
            errors += 1

    return errors*K**(-1)


def simulate1():
    """ This function simulates BER. """
    lengths = np.arange(1, 17, 1)
    BER_final = []
    ebnodb = np.arange(0, 12, 0.01)

    for k in lengths:
        
        BER = []
        for i in ebnodb:
            BER.append(calcBER(16, int(k), i))

        BER_final.append(np.average(BER))

    plt.stem(lengths, BER_final)
    plt.xlabel("Message length (in bits)")
    plt.ylabel("log(BER)")
    plt.grid()
    plt.show()

def simulate2():
    """ This function simulates BER on log graph """
    lengths = np.arange(1, 16, 4)
    BER_final = []
    ebnodb = np.arange(0, 12, 0.01)

    for k in lengths:
        
        BER = []
        for i in ebnodb:
            BER.append(calcBER(16, int(k), i))

        plt.plot(ebnodb, np.log10(BER), label="BER plot for K = {}".format(k))

    plt.xlabel("Eb/No in dB")
    plt.ylabel("BER in Log Scale")
    plt.grid()
    plt.legend()
    plt.show()


def monte_carlo(ebnodb, N, K, iterations=250):
    """ This function generates the histogram of BER's obtained for a particular Eb/No """

    l = [] # empty list to store BERs
    for i in range(iterations):
        l.append(calcBER(N, K, ebnodb))

    plt.hist(l, bins=np.arange(0, 1, 0.01))
    plt.xlabel("BER")
    plt.ylabel("Frequency")
    plt.show()
