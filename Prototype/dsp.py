import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Define parameters
duration = 5  # Duration of the recording in seconds
fs = 44100  # Sample rate
buffer_size = 1024  # Number of audio samples to read in each iteration

# Function to run audio visualization
def run_audio_visualization():
    # Initialize an empty array for audio data
    audio_data = np.zeros(buffer_size)

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

    # Callback function to update audio data
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        nonlocal audio_data
        audio_data = indata[:, 0]  # Get the first channel

    # Create an audio stream
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=buffer_size)

    # Animation function
    def update(frame):
        line.set_ydata(audio_data)
        return line,

    # Start the audio stream and animation
    with stream:
        ani = FuncAnimation(fig, update, blit=True)
        plt.show()