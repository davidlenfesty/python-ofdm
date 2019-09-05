# the naming is terrible but eh
import numpy as np
from math import floor, ceil

def parallelise(n, in_data):
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

def serialise(n, in_data):
    out_data = bytearray()

    # Will need to be changed to deal with more QAM schemes
    bytes_per_symbol = int(n / 4)

    for i in range(len(in_data)):
        for j in range(bytes_per_symbol):
            new_byte = np.uint8(0)

            for k in range(4):
                #try:
                new_byte |= in_data[i][(j*4) + k] << (k * 2)
                #except:
                 #   print(i)

            out_data.append(new_byte)

    return out_data

