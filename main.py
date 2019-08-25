#!/usr/bin/env python3.7

import numpy as np
import matplotlib.pyplot as plt
from math import floor, ceil

from channel import channel_sim

def parralelise(n, in_data):
    """
    Parameters:
    n - number of channels
    in_data - input data, array of 

    Output:
    array of OFDM symbols, each symbol
    """

    data_len = len(in_data)

    # Find number of OFDM symbols
    # Multiplied by four here because we have 2 bits per QAM symbol/channel/whatever
    # so 8 / 2 = 4
    symbols = float(data_len * 4 / n)
    
    # Check if we have to pad last symbol
    if symbols.is_integer():
        symbols = int(symbols)
    else:
        symbols = ceil(symbols)


    # Initialise output array
    out_data = np.ndarray(shape=(int(symbols), n), dtype=int)

    # Just a way to keep track of where I am in the byte array
    # I bet there's a more "python-y" way to do this but whatever
    byte_index = 0
    bit_index = 0

    # Will have to be revamped if I want to do more than 4-QAM modulation
    for i in range(symbols):
        for j in range(n):
            #  if we have exhausted data, pad with zeroes
            if i == symbols - 1 and byte_index == data_len:
                for k in range(j, n):
                    out_data[i][k] = 0

                break

            # Isolate the correct bits
            out_data[i][j] = (in_data[byte_index] >> (bit_index * 2)) & 0b11

            bit_index += 1

            if bit_index == 4:
                byte_index += 1
                bit_index = 0


    return out_data




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

    parallel = parralelise(16, bytes)

    modulated = qam(16, parallel)

    tx = np.fft.ifft(modulated)

    rx = channel_sim(tx)
    
    plt.plot(tx[0], 'r')
    plt.plot(rx[0], 'b')
    plt.show()

    print(channel_sim(pre_modulated))



