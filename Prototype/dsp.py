import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

## Define parameters
fs = 44100  # Sample rate
buffer_size = 1024  # Number of audio samples to read in each iteration
num_buffers = 50  # Number of buffers to keep for the spectrogram

# Global variable to keep track of FFT computation times
fft_times = []

# Function to print average computation time every 5 seconds
def print_average_time():
    while True:
        time.sleep(5)  # Wait for 5 seconds
        if fft_times:
            average_time = sum(fft_times) / len(fft_times)
            print(f"Average FFT computation time: {average_time:.6f} seconds")
            fft_times.clear()  # Clear the list for the next interval

# Function to run audio visualization
def run_audio_visualization(audio_data):
    # Create a figure for the plot
    fig, ax = plt.subplots()
    x = np.linspace(0, buffer_size / fs, buffer_size)  # Time axis
    line, = ax.plot(x, audio_data, color='blue')
    ax.set_ylim(-1, 1)  # Set y-axis limits for amplitude
    ax.set_xlim(0, buffer_size / fs)  # Set x-axis limits for time
    ax.set_title('Real-Time Audio Waveform')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')
    ax.grid()

    # Animation function
    def update(frame):
        line.set_ydata(audio_data[0])  # Access the first element to get the audio data
        return line,

    # Animation
    ani = FuncAnimation(fig, update, blit=True)

    plt.show()  # Move plt.show() to the main thread

# Function to run spectrogram visualization
def run_spectrogram_visualization():
    # Initialize an empty array to store audio data for the spectrogram
    audio_buffers = np.zeros((num_buffers, buffer_size))

    # Create a figure for the spectrogram
    fig, ax = plt.subplots()
    ax.set_title('Real-Time Audio Spectrogram')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Frequency [Hz]')
    extent = (0, num_buffers * (buffer_size / fs), 0, fs / 2)
    im = ax.imshow(np.zeros((fs // 2, num_buffers)), aspect='auto', extent=extent, origin='lower', cmap='inferno')

    # Callback function to update audio buffers for the spectrogram
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        audio_buffers[:-1] = audio_buffers[1:]  # Shift buffers
        audio_buffers[-1] = indata[:, 0]  # Add new data to the last buffer

        # Compute the FFT for the current buffer
        start_time = time.time()  # Start time for FFT computation
        fft_data = np.fft.fft(audio_buffers[-1])
        magnitude = np.abs(fft_data[:buffer_size // 2])  # Take only the positive frequencies
        fft_time = time.time() - start_time  # Compute elapsed time
        fft_times.append(fft_time)  # Store computation time

        # Update the spectrogram data
        im.set_array(np.roll(im.get_array(), -1, axis=1))  # Shift the spectrogram left
        im.get_array()[:, -1] = magnitude  # Add new magnitude data to the right

    # Create an audio stream
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=buffer_size)

    # Start the audio stream
    with stream:
        plt.colorbar(im, ax=ax)
        plt.show()