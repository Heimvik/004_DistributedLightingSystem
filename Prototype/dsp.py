import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import threading

# PyAudio configuration
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 2  # Stereo audio
RATE = 44100  # Sample rate (44.1 kHz)
CHUNK = 1024  # Number of samples per chunk (small enough for real-time processing)
LOOPBACK_DEVICE_NAME = 'loopback.monitor'

# Function to perform FFT and plot it
def process_audio_data(data):
    audioData = np.frombuffer(data, dtype=np.int16)
    
    fftResult = np.fft.fft(audioData[::2])  # Use every second sample for left channel
    fftMagnitude = np.abs(fftResult)[:CHUNK // 2]  # Take magnitude of FFT and limit to half

    fftMagnitude = fftMagnitude / np.max(fftMagnitude)

    print("\033[H\033[J")  # ANSI escape code to clear the terminal screen

    for i, value in enumerate(fftMagnitude):
        bar = "#" * int(value * 50)  # Scale the bar length by 50 for visualization
        print(f"{i:03d}: {bar}")

# Function to read from the loopback stream
def audio_stream_reader():
    p = pyaudio.PyAudio()

    loopbackDeviceIndices = []
    for i in range(p.get_device_count()):
        deviceInfo = p.get_device_info_by_index(i)
        if LOOPBACK_DEVICE_NAME in deviceInfo['name']:
            loopbackDeviceIndices.append(i)

    print("Available loopback devices:", loopbackDeviceIndices)

    loopbackDeviceIndex = None
    for i in range(p.get_device_count()):
        deviceInfo = p.get_device_info_by_index(i)
        if LOOPBACK_DEVICE_NAME in deviceInfo['name']:
            loopbackDeviceIndex = i
            break
    
    if loopbackDeviceIndex is None:
        raise RuntimeError(f"Loopback device named '{LOOPBACK_DEVICE_NAME}' not found.")
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=loopbackDeviceIndex,
                    frames_per_buffer=CHUNK)

    print(f"Reading audio from {LOOPBACK_DEVICE_NAME}...")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            process_audio_data(data)

    except KeyboardInterrupt:
        print("\nStopping audio stream...")
        stream.stop_stream()
        stream.close()
        p.terminate()

def initAudioProcessing():
    streamThread = threading.Thread(target=audio_stream_reader)
    streamThread.start()
    return streamThread
