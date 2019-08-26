import numpy as np

channel_response = np.array([0, 0, 0, 1, 0, 0, 0])

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


