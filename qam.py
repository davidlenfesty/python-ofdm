import numpy as np
from scipy.spatial.distance import euclidean

pilot_value = 1 + 1j

qam_mapping_table = {
    0 : 1 + 1j,
    1 : -1 + 1j,
    2 : -1 - 1j,
    3 : 1 - 1j
}

qam_demapping_table = { x : y for y, x in qam_mapping_table.items() }

def modulate(in_data, pilots=0):
    """
    Modulates into 4-QAM encoding, might change that number later.

    This turns input data into a "constellation" of complex numbers,
    ready to be fed into an IFFT. This constellation could also be used
    directly with an IQ modulator.

    Parameters:
    in_data -  m X n array, m symbols to run on
    pilots (optional) - number of pilot signals to intersperse into carriers

    Output:
    data 
    """

    num_data_carriers = len(in_data[0])

    all_carriers = np.arange(num_data_carriers + pilots, dtype=int)

    if pilots > 0:
        pilot_carriers = all_carriers[::(num_data_carriers + pilots)//pilots]
        pilot_carriers = np.delete(pilot_carriers, 0) # not sure how to not have this line
        data_carriers = np.delete(all_carriers, pilot_carriers)
        print(pilot_carriers)
    else:
        data_carriers = all_carriers


    #initialise output array with additional pilot carriers as well
    out_data = np.ndarray((len(in_data), num_data_carriers + pilots), dtype=np.csingle)

    for i in range(len(in_data)):
        data_index = 0
        for carrier_index in data_carriers:
            out_data[i][carrier_index] = qam_mapping_table[in_data[i][data_index]]
            data_index += 1

        if pilots > 0:
            for j in pilot_carriers:
                # Value for pilot carriers
                out_data[i][j] = pilot_value


    return out_data

def demodulate(in_data, pilots=0):
    """
    Demodulates incoming signal.
    """

    all_carriers = np.arange(len(in_data[0]), dtype=int)

    if pilots > 0:
        pilot_carriers = all_carriers[::(len(all_carriers)) // pilots]
        pilot_carriers = np.delete(pilot_carriers, 0) # not sure how to not have this line
        data_carriers = np.delete(all_carriers, pilot_carriers)
    else:
        data_carriers = all_carriers

    out_data = np.ndarray((len(in_data), len(data_carriers)), dtype=np.uint8)

    # Just pull the constellation array data out
    constellation = [ x for x in qam_demapping_table.keys() ]

    for i in range(len(in_data)):
        data_index = 0
        for carrier_index in data_carriers:
            distances = np.ndarray((len(constellation)), dtype=np.single)

            # Here we have to map to the closest constellation point,
            # because floating point error
            for k in range(len(constellation)):
                distances[k] = euclidean(in_data[i][carrier_index], constellation[k])

            # output is the index of the constellation, essentially
            # this may have to change if I want to generalise
            out_data[i][data_index] = np.argmin(distances)
            data_index += 1

    return out_data
