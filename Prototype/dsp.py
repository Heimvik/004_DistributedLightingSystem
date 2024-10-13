import numpy as np
import sounddevice as sd
import time
import threading

# Parameters
fs = 44100  # Original sampling rate
downsample_factor = 4  # Factor by which to downsample
buffer_size = 1024  # Size of the audio buffer

# New downsampled sampling rate
downsampled_fs = fs // downsample_factor

# Function to run FFT visualization
def run_fft_visualization():
    # Create a figure for the plot
    freqs = np.fft.rfftfreq(buffer_size, d=1/fs)  # Frequency axis

    # Callback function to update the FFT printout
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)

        # Downsample the incoming audio data by taking every 4th sample
        downsampled_data = indata[::downsample_factor]

        # Compute the FFT for the downsampled audio data
        fft_data = np.fft.fft(downsampled_data[:, 0], n=buffer_size // downsample_factor)
        magnitude = np.abs(fft_data[:(buffer_size // (2 * downsample_factor))])  # Take only the positive frequencies

        # Create new frequency axis for downsampled signal
        downsampled_freqs = np.fft.rfftfreq(buffer_size // downsample_factor, d=1/downsampled_fs)

        # Define the logarithmic frequency bins starting from 30 Hz
        start_freq = 30  # Starting frequency
        max_freq = downsampled_fs / 2  # New Nyquist frequency
        log_bins = np.logspace(np.log10(start_freq), np.log10(max_freq), 16).astype(int)

        # Filter out invalid frequency indices that exceed the FFT size
        log_bins = [i for i in log_bins if i < len(magnitude)]

        # Get magnitudes for the selected logarithmic frequency bins
        bin_magnitudes = magnitude[log_bins]
        bin_frequencies = downsampled_freqs[log_bins]

        # Print the frequencies and their corresponding magnitudes
        print("\r", end='')  # Carriage return to overwrite the line
        for freq, mag in zip(bin_frequencies, bin_magnitudes):
            print(f"{freq:<20.2f}", end=' ')
        print()  # Newline for the next row

    # Create an audio stream
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=buffer_size)

    # Start the audio stream
    with stream:
        print("Listening... Press Ctrl+C to stop.")
        while True:
            time.sleep(1)  # Keep the stream alive