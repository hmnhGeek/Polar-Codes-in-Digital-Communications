import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc

def Q(x):
    return 0.5*erfc(x*(2**(-0.5)))

ebnodb = np.arange(0.1, 12, 0.01)
ebno = [10**(i*0.1) for i in ebnodb]
ebno = np.array(ebno)
y = np.log(Q(np.sqrt(2*ebno)))

plt.plot(ebnodb, y)
plt.xlabel("Eb/N0 (in dB)")
plt.ylabel("log(BER)")
plt.grid()
plt.show()
