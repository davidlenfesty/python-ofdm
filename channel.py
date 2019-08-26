import numpy as np
import scipy.interpolate

import matplotlib.pyplot as plt

channel_response = np.array([-1 - 1j, 0, 0, 1, 0, 0, -1 - 1j])

# How do I sync this across two files?
# figure it out later
pilot_value = 1 + 1j

# 15dB seems to be around the minimum for error-free transmission
snr_db = 15

def sim(in_data):
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.csingle)

    # noise stuff is straight copied from the DSP illustrations article
    for i in range(len(in_data)):
        convolved = np.convolve(channel_response, in_data[i], mode='same')

        signal_power = np.mean(abs(convolved**2))
        noise_power = signal_power * 10**(-snr_db/10)

        noise = np.sqrt(noise_power / 2) * (np.random.randn(*convolved.shape) + 1j*np.random.randn(*convolved.shape))

        out_data[i] = convolved + noise

    return out_data

# Again, most of this is stolen from the guide
# this sort of stuff I had no idea about before I read the guide
def estimate(in_data, pilots=0):

    all_carriers = np.arange(len(in_data[0]))


    if pilots > 0:
        pilot_carriers = all_carriers[::(len(all_carriers)) // pilots]
        pilot_carriers = np.delete(pilot_carriers, 0)

        # start averaging
        H_est = 0

        for i in range(len(in_data)):
            H_est_pilots = in_data[i][pilot_carriers] / pilot_value


            H_est_abs = scipy.interpolate.interp1d(pilot_carriers, abs(H_est_pilots), kind='linear', fill_value='extrapolate')(all_carriers)
            H_est_phase = scipy.interpolate.interp1d(pilot_carriers, np.angle(H_est_pilots), kind='linear', fill_value='extrapolate')(all_carriers)
            H_est += H_est_abs * np.exp(1j*H_est_phase)

            print(H_est_abs)

        H_est = H_est / len(in_data)

        return H_est

    else:
        return 1

def equalize(in_data, H_est):
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.csingle)

    for i in range(len(in_data)):
        out_data[i] = in_data[i] / H_est

    return out_data
