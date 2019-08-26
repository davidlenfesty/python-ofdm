#!/usr/bin/env python3.7

"""
Shitty OFDM simulator designed to make it so I understand OFDM.
Hopefully eventually this modem design makes it onto an fpga.

TODO:
    Add comments for functions
    Explain what the main function is doing
    Add more errors, like a shifted signal
    Add support for 16-QAM, 64-QAM, etc...
    Add channel estimation via pilot carriers
    Add some sort of payload support, i.e. be able to drop the padding at the end

"""

import numpy as np
import matplotlib.pyplot as plt

import channel
import qam

from serpar import parallelise, serialise

def cp_add(in_data, prefix_len):
    out_data = np.ndarray((len(in_data), len(in_data[0]) + prefix_len), dtype=np.csingle)

    for i in range(len(in_data)):
        cp = in_data[i][-prefix_len:]
        out_data[i] = np.hstack([cp, in_data[i]])

    return out_data

def cp_remove(in_data, prefix_len):
    out_data = np.ndarray((len(in_data), len(in_data[0]) - prefix_len), dtype=np.csingle)

    for i in range(len(in_data)):
        out_data[i] = in_data[i][prefix_len:]

    return out_data




if __name__ == '__main__':
    with open('data.txt', 'r') as file:
        data = file.read()

    bytes = bytearray(data, 'utf8')

    parallel = parallelise(64, bytes)

    modulated = qam.modulate(parallel)

    ofdm_time = np.fft.ifft(modulated)

    tx = cp_add(ofdm_time, 4)

    rx = channel.sim(tx)

    # Put the channel simulator stuff here

    ofdm_cp_removed = cp_remove(rx, 4)

    to_decode = np.fft.fft(ofdm_cp_removed)

    to_serialise = qam.demodulate(to_decode)

    data = serialise(64, to_serialise)

    print(data)
