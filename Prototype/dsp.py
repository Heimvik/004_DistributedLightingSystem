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

# Function to run FFT visualization
def run_fft_visualization():
    # Create a figure for the plot
    fig, ax = plt.subplots()
    freqs = np.fft.rfftfreq(buffer_size, d=1/fs)  # Frequency axis
    line, = ax.plot(freqs, np.zeros(len(freqs)), color='blue')
    ax.set_ylim(0, 1)  # Set y-axis limits for magnitude
    ax.set_xlim(0, fs / 2)  # Set x-axis limits for frequency
    ax.set_title('Real-Time Audio FFT')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Magnitude')
    ax.grid()

    # Callback function to update the FFT plot
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)

        # Compute the FFT for the incoming audio data
        fft_data = np.fft.fft(indata[:, 0])
        magnitude = np.abs(fft_data[:buffer_size // 2])  # Take only the positive frequencies

        # Update the FFT plot
        line.set_ydata(magnitude)  # Update the line with the new FFT data
        fig.canvas.draw()  # Redraw the figure
        fig.canvas.flush_events()  # Ensure that the events are processed

    # Create an audio stream
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=buffer_size)

    # Start the audio stream
    with stream:
        plt.show()  # Show the plot