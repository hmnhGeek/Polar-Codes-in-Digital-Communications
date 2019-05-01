import numpy as np
import random
import matplotlib.pyplot as plt

# reliability sequence for 5G N=1024
Q = np.array([1, 2, 3, 5, 9, 4, 6, 10, 7, 11, 13, 8, 12, 14, 15, 16])-1

def encode(N, K, Q):
    if N >= K:
        n = np.log(N)/np.log(2)
        n = int(n)

        msg = np.random.choice([0, 1], K)
        #msg = [1, 1, 0, 1, 1, 0, 0, 1]
        U = np.array([0]*N)

        temp = Q[N-K::]
        for i in range(len(msg)):
            U[temp[i]] = msg[i]
            
        G2 = np.matrix([[1,0], [1, 1]])
        GN = G2

        for i in range(n-1):
            GN = np.kron(G2, GN)

        C = (U.dot(GN))%2
        C = C.tolist()[0]
        return msg, C
    else:
        return -1

def AWGN(message, ebnodb, R):
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

    GinvN = np.linalg.inv(GN)
    C = np.matrix(C)

    D = C.dot(GinvN) % 2
    D = D.tolist()[0]
    D = [int(i) for i  in D]
    temp = Q[N-K::]

    msg = []
    for i in temp:
        msg.append(D[i])

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
        if message[i] != m_cap[i]:
            errors += 1

    return errors*K**(-1)


def simulate1():
    lengths = np.arange(1, 17, 1)
    BER_final = []
    ebnodb = np.arange(0, 12, 0.01)

    for k in lengths:
        
        BER = []
        for i in ebnodb:
            BER.append(calcBER(16, int(k), i))

        BER_final.append(np.average(BER))

    #BER_final = np.log10(BER_final)

    plt.stem(lengths, BER_final)
    plt.xlabel("Message length (in bits)")
    plt.ylabel("log(BER)")
    plt.grid()
    plt.show()

def simulate2():
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

simulate2()
