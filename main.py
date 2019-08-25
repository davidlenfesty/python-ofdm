#!/usr/bin/env python3.7

import numpy as np
import matplotlib.pyplot as plt

from channel import channel_sim

from serpar import parallelise, serialise

import qam

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
    



