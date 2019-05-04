import itertools
import numpy as np
import matplotlib.pyplot as plt

def split_capacity(BEC_capacity):
    # refer to arikan's paper for this.
    good_channel_capacity = 2*BEC_capacity - BEC_capacity**2
    bad_channel_capacity = BEC_capacity**2
    return [good_channel_capacity, bad_channel_capacity]


def polarize(N, bec_cap=0.5):
    '''
        This function generates all the W_{N} channel capacities.
    '''
    num_channels = N
    i = 0 # to track the number of iterations.
    capacities = [[bec_cap],]

    while i != num_channels:
        curr_channel = capacities[-1] # last element because, these will be further polarized.
        sub_cap = []
        for j in curr_channel: # polarize each of them now.
            good_bad = split_capacity(j)
            sub_cap.append(good_bad[0])
            sub_cap.append(good_bad[1])
        i+=1
        capacities.append(sub_cap)

    keys = list(range(len(capacities[-1])+1)) # generate indexes for channels.
    return dict(zip(keys, capacities[-1])) # zip the key-vals and return them.

def reliability_sequence(N, bec_cap=0.5):
    capacities = polarize(N, bec_cap) # generate the capacities
    rel = sorted(capacities.items(), key=lambda x: x[1]) # sort them from bad to good.
    seq = []
    for i in rel:
        seq.append(i[0]+1) # because indexing began from 0.
    return seq[-1:-len(seq)-1:-1] # return them from good to bad.

def matthew_effect_bad():
    n = np.arange(1, 10)
    x = np.arange(1, 11)
    C1 = []
    C2 = []

    for i in n:
        p = np.arange(0, 1, 0.1)
        sub_list = []
        for j in p:
            sub_list.append(min(polarize(i, j)))
        #C2.append(max(polarize(i, 0.9)))
        C1.append(sub_list)
    loc = 1
    for l in C1:
        plt.plot(x, l, label='N={}'.format(loc), marker='o')
        loc += 1
    plt.legend()
    plt.ylabel('Bad Channel Capacity')
    plt.xlabel('Transition Probability of BEC')
    plt.grid()
    plt.show()

def matthew_effect_good():
    n = np.arange(1, 10)
    x = np.arange(1, 11)
    C1 = []
    C2 = []

    for i in n:
        p = np.arange(0, 1, 0.1)
        sub_list = []
        for j in p:
            sub_list.append(max(polarize(i, j)))
        #C2.append(max(polarize(i, 0.9)))
        C1.append(sub_list)
    loc = 1
    for l in C1:
        plt.plot(x, l, label='N={}'.format(loc), marker='o')
        loc += 1
    plt.legend()
    plt.ylabel('Good Channel Capacity')
    plt.xlabel('Transition Probability of BEC')
    plt.grid()
    plt.show()
