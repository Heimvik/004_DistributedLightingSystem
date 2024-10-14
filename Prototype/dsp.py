import numpy as np
import sounddevice as sd
import time
#from visuals import init_bars,load_led_bars_config,set_brightness_and_color

## Define parameters
fs = 44100  # Sample rate
buffer_size = 1024  # Number of audio samples to read in each iteration
num_buffers = 50  # Number of buffers to keep for the spectrogram
downsample_factor = 4  # Factor by which to downsample
downsampled_fs = fs // downsample_factor  # New sample rate after downsampling
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
    #bars = init_bars(load_led_bars_config('visualsConfig.json'))

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

        # New Nyquist frequency after downsampling
        nyquist_frequency = downsampled_fs / 2  

        # Define frequency bins starting from 30 Hz in logarithmic scale
        log_bins = np.array([30, 60, 120, 240, 480, 960, 1920, 3840, 5000])

        # Ensure we only consider frequencies below the Nyquist frequency
        valid_bins = [freq for freq in log_bins if freq < nyquist_frequency]

        # Get the corresponding indices for valid frequency bins
        bin_indices = [np.argmin(np.abs(downsampled_freqs - freq)) for freq in valid_bins]

        # Get magnitudes for the selected frequency bins
        bin_magnitudes = magnitude[bin_indices]

        #TODO: Put in function that takes in the param 
        #if bin_magnitudes[0] > 20:
            #set_brightness_and_color(bars[0], min(((bin_magnitudes[0] / 40) * 255), 255), (0, 0, 255))
        # Print the magnitudes for the selected frequency bins
        print("\r", end='')  # Carriage return to overwrite the line
        for mag in bin_magnitudes:
            print(f"{mag:<20.2f}", end=' ')
        print()  # Newline for the next row

    # Create an audio stream
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, blocksize=buffer_size, device = 7)

    # Start the audio stream
    with stream:
        print("Listening... Press Ctrl+C to stop.")
        while True:
            time.sleep(1)  # Keep the stream alive
