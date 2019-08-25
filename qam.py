import numpy as np
from scipy.spatial.distance import euclidean

qam_mapping_table = {
    0 : 1 + 1j,
    1 : -1 + 1j,
    2 : -1 - 1j,
    3 : 1 - 1j
}

qam_demapping_table = { x : y for y, x in qam_mapping_table.items() }

def modulate(in_data):
    """
    Modulates into 4-QAM encoding, might change that number later.

    Parameters:
    in_data -  m X n array, m symbols to run on

    Output:
    data 
    """

    #initialise output array
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.csingle)

    for i in range(len(in_data)):
        for j in range(len(in_data[0])):
            out_data[i][j] = qam_mapping_table[in_data[i][j]]

    return out_data

def demodulate(n, in_data):
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.uint8)

    # Just pull the constellation array data out
    constellation = { x for x in qam_demapping_table.keys() }

    for i in range(len(in_data)):
        for j in range(len(in_data[0])):
            distances = np.ndarray((len(constellation)), dtype=np.single)

            # Here we have to map to the closest constellation point,
            # because floating point error
            for k in range(len(constellation)):
                distances[k] = euclidean(in_data[i][j], constellation[i][j])

            # output is the index of the constellation, essentially
            # this may have to change if I want to generalise
            out_data[i][j] = np.argmin(distances)

    return out_data
