import numpy as np

channel_response = np.array([1, 0, 1 - 1j])

def sim(in_data):
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.csingle)

    for i in range(len(in_data)):
        convolved = np.convolve(channel_response, in_data[i])



