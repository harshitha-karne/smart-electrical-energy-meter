
import numpy as np

def calculate_thd(signal, sampling_frequency, fundamental_frequency=50):

    # Number of samples
    N = len(signal)

    # Perform FFT
    fft_values = np.fft.rfft(signal)

    # Calculate frequency values
    frequencies = np.fft.rfftfreq(
        N,
        d=1/sampling_frequency
    )

    # Calculate amplitude spectrum
    amplitudes = 2 * np.abs(fft_values) / N

    amplitudes[0] /= 2

    if N % 2 == 0:
        amplitudes[-1] /= 2

    # Find fundamental frequency component
    fundamental_index = np.argmin(
        np.abs(frequencies - fundamental_frequency)
    )

    fundamental_amplitude = amplitudes[fundamental_index]

    # Extract harmonic components (2nd to 10th)
    harmonic_amplitudes = []

    for h in range(2, 11):

        harmonic_frequency = h * fundamental_frequency

        index = np.argmin(
            np.abs(frequencies - harmonic_frequency)
        )

        harmonic_amplitudes.append(amplitudes[index])

    harmonic_amplitudes = np.array(harmonic_amplitudes)

    # Calculate THD
    if fundamental_amplitude == 0:
        thd = 0
    else:
        thd = (
            np.sqrt(np.sum(harmonic_amplitudes**2))
            / fundamental_amplitude
        ) * 100

    return thd, frequencies, amplitudes
