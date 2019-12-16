import numpy as np
import scipy.interpolate

import matplotlib.pyplot as plt

# Dirac delta function response, no change
channel_response = np.array([0, 0, 0, 1, 0, 0, 0])
#channel_response = np.array([1, 0, 0.3+0.3j])


# How do I sync this across two files?
# figure it out later
pilot_value = 1 + 1j

# 15dB seems to be around the minimum for error-free transmission
snr_db = 70

def sim(in_data):
    """
    Simulate effects of communication channel.

    Convolves the channel response, and adds random noise to the signal.
    """

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
    """
    Estimate channel effects by some cool properties.

    Since the effects of the channel medium is a convolution of the transmitted signal,
    we can abuse this for some easy math.

    We take the time domain input signal and turn that into a frequency domain signal.
    If we had a perfect channel, this frequency domain signal would exactly equal the signal
    transmitted. But it doesn't. However, we are in the frequency domain, which means
    convolution turns into multiplication, and to find the effect of the channel on each
    subcarrier, we can simply use division.
    
    Unfortunately, we don't know what the original data was, so we use "pilot" subchannels, which transmit
    known information. We can use this to get estimates for each of the pilot carriers, and finally, we can interpolate
    these values to get an estimate for everything.

    There are a few issues with this method:
    1: It is very estimate-ey. We have to interpolate from a subset of the carriers.
    2: It is quite inefficient. We are sending useless information on every symbol.

    I think a better solution is to send a known symbol (or a set of known symbols)
    at the beginnning of each transmission instead. This means we get a full channel estimate
    every time. This also has the advantage of being able to synchronise the symbols. Since I
    will be implementing some sort of protocol anyways, I think this will be a good idea. As well,
    we move slow enough that the channel will not likely change significantly over a single packet.

    Actually maybe not? Looked at a paper, check the drive.
    """

    carrier_symbol = in_data[0]

    H_est = 0
    H = np.ndarray((len(carrier_symbol)), dtype=np.csingle)
    # Obtain estimate for each sub carrier
    for i in range(len(carrier_symbol)):
        H[i] = carrier_symbol[i] / np.csingle(1 + 1j)
        
    print(H)

    # Exact channel response
    H_exact = np.fft.fft(channel_response, 64)

    plt.plot(range(64), np.real(H), "b-")
    plt.plot(range(64), np.real(H_exact), "r")
    plt.show(block=True)

    plt.plot(range(64), np.imag(H), "b-")
    plt.plot(range(64), np.imag(H_exact), "r")
    plt.show(block=True)

    return H


def equalize(in_data, H_est):
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.csingle)

    for i in range(len(in_data)):
        out_data[i] = in_data[i] / H_est

    return out_data
