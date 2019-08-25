#!/usr/bin/env python3.7

import numpy as np
import matplotlib.pyplot as plt

from channel import channel_sim

from serpar import parallelise, serialise



def qam(n, in_data):
    """
    Modulates into 4-QAM encoding, might change that number later.

    Parameters:
    n - number of channels to operate on
    in_data -  m X n array, m symbols to run on

    Output:
    data 
    """

    #initialise output array
    out_data = np.ndarray((len(in_data), n), dtype=np.csingle)

    for i in range(len(in_data)):
        for j in range(n):
            
            #4-QAM is nice
            out_data[i][j] = 1 + 1j

            # Just rotate 90 degrees for every number and you've got your encoding
            for k in range(in_data[i][j]):
                out_data[i][j] = out_data[i][j] * (1j)

    return out_data

def cyclic_prefix(n, in_data, prefix_len):
    out_data = np.ndarray((len(in_data), n + prefix_len), dtype=np.csingle)





if __name__ == '__main__':
    with open('data.txt', 'r') as file:
        data = file.read()

    bytes = bytearray(data, 'utf8')

    parallel = parallelise(16, bytes)

    modulated = qam(16, parallel)

    tx = np.fft.ifft(modulated)

    rx = channel_sim(tx)
    
    plt.plot(tx[0], 'r')
    plt.plot(rx[0], 'b')
    plt.show()

    print(channel_sim(pre_modulated))



