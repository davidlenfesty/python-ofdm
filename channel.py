import numpy as np
import scipy.interpolate

import matplotlib.pyplot as plt

# Dirac delta function response, no change
#channel_response = np.array([0, 0, 0, 1, 0, 0, 0])
channel_response = np.array([1, 0, 0.3+0.3j])


# How do I sync this across two files?
# figure it out later
pilot_value = 5 + 5j

# 15dB seems to be around the minimum for error-free transmission
snr_db = 300

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

    all_carriers = np.arange(len(in_data[0]))

    if pilots > 0:
        pilot_carriers = all_carriers[::(len(all_carriers)) // pilots]
        pilot_carriers = np.delete(pilot_carriers, 0)

        print(pilot_carriers)

        # start averaging
        #H_est = 0

        # for i in range(len(in_data)):
        #     # Obtain channel response at pilot carriers
        #     H_est_pilots = in_data[i][pilot_carriers] / pilot_value


        #     # Interpolate estimates based on what we get from the few pilot values
        #     H_est_abs = scipy.interpolate.interp1d(pilot_carriers, abs(H_est_pilots), kind='linear', fill_value='extrapolate')(all_carriers)
        #     H_est_phase = scipy.interpolate.interp1d(pilot_carriers, np.angle(H_est_pilots), kind='linear', fill_value='extrapolate')(all_carriers)

        #     # Take angular form and turn into rectangular form
        #     H_est += H_est_abs * np.exp(1j*H_est_phase)

        H_est_pilots = np.ndarray((len(pilot_carriers)), dtype=np.csingle)

        j = 0
        # Obtain channel response at pilot carriers
        for i in pilot_carriers:
            H_est_pilots[j] = in_data[0][i] / pilot_value
            print("Value: " + str(in_data[0][i]))
            print("Pilot estimate: " + str(H_est_pilots[j]))
            j += 1


        # Interpolate estimates based on what we get from the few pilot values
        H_est_abs = scipy.interpolate.interp1d(pilot_carriers, abs(H_est_pilots), kind='linear', fill_value='extrapolate')(all_carriers)
        H_est_phase = scipy.interpolate.interp1d(pilot_carriers, np.angle(H_est_pilots), kind='linear', fill_value='extrapolate')(all_carriers)

        # Take angular form and turn into rectangular form
        H_est = H_est_abs * np.exp(1j*H_est_phase)

        # for an average channel estimate
        # H_est = H_est / len(in_data)

        # Exact channel response
        H_exact = np.fft.fft(channel_response, len(in_data[0]))

        plt.plot(all_carriers, np.real(H_exact), "b")
        plt.plot(all_carriers, np.real(H_est), "r")
        plt.plot(pilot_carriers, np.real(H_est_pilots), "go")
        plt.show(block=True)

        plt.plot(all_carriers, np.imag(H_exact), "b")
        plt.plot(all_carriers, np.imag(H_est), "r")
        plt.plot(pilot_carriers, np.imag(H_est_pilots), "go")
        plt.show(block=True)

        print(H_est_pilots)
        print(H_exact[pilot_carriers])

        return H_est


    else:
        return -1

def equalize(in_data, H_est):
    out_data = np.ndarray((len(in_data), len(in_data[0])), dtype=np.csingle)

    for i in range(len(in_data)):
        out_data[i] = in_data[i] / H_est

    return out_data
