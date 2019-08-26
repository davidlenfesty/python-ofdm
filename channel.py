import numpy as np

channel_response = np.array([0, 0, 0, 1, 0, 0, 0])

def sim(in_data):
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.csingle)

    for i in range(len(in_data)):
        convolved = np.convolve(channel_response, in_data[i], mode='same')
        out_data[i] = convolved

    return out_data


