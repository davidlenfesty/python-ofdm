#!/usr/bin/env python3

"""
Shitty OFDM simulator designed to make it so I understand OFDM.
Hopefully eventually this modem design makes it onto an fpga.

TODO:
    Change channel estimation to pre-amble symbols
    Add comments for functions
    Add more errors, like a shifted signal
    Add support for 16-QAM, 64-QAM, etc...
    Add some sort of payload support, i.e. be able to drop the padding at the end

I don't believe this architecture will work too well for an FPGA, right now it's kind of hacky,
and obviously there are parallelisation improvements on an FPGA, so this will likely have to be redone.

Right now though it's just proof of concept to see if I can get a reliable signal to work.

"""

import numpy as np
import matplotlib.pyplot as plt
plt.ion()

import channel
import qam

from serpar import parallelise, serialise

def cp_add(in_data, prefix_len):
    """
    Adds a cyclic prefix to an array of symbols, with a specified length.

    This changes the linear convolution of the data into a circular convolution,
    allowing easier equalization.
    As well, it helps remove inter-symbol interference.
    """

    out_data = np.ndarray((len(in_data), len(in_data[0]) + prefix_len), dtype=np.csingle)

    for i in range(len(in_data)):
        cp = in_data[i][-prefix_len:]
        out_data[i] = np.hstack([cp, in_data[i]])

    return out_data

def cp_remove(in_data, prefix_len):
    """
    Removes cyclic prefix from retrieved data. Naively assumes that data is correctly aligned.
    """

    out_data = np.ndarray((len(in_data), len(in_data[0]) - prefix_len), dtype=np.csingle)

    for i in range(len(in_data)):
        out_data[i] = in_data[i][prefix_len:]

    return out_data




if __name__ == '__main__':
    with open('data.txt', 'r') as file:
        data = file.read()

    bytes = bytearray(data, 'utf8')

    # Turn data into a parallelised form, able to be QAM-modulated
    parallel = parallelise(64, bytes)

    # modulate data with a QAM scheme
    modulated = qam.modulate(parallel, pilots=20)

    # Run IFFT to get a time-domain signal to send
    ofdm_time = np.fft.ifft(modulated)

    # Add cyclic prefix to each symbol
    tx = cp_add(ofdm_time, 16)

    # Simulate effects of a multipath channel
    rx = channel.sim(tx)

    # Remove cyclic prefix from incoming symbols
    ofdm_cp_removed = cp_remove(rx, 16)

    # Bring symbols back into frequency domain to get carrier channels
    to_equalize = np.fft.fft(ofdm_cp_removed)

    # Find an estimate for channel effect
    H_est = channel.estimate(to_equalize, pilots=20)

    # Equalise based on estimated channel
    to_decode = channel.equalize(to_equalize, H_est)

    # Demodulate symbol into output data
    to_serialise = qam.demodulate(to_decode, pilots=20)

    # Turn data back into string
    data = serialise(64, to_serialise)
    print(data)
