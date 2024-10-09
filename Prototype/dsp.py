import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import ctypes
import time

# Load the GPU FFT shared library
gpuFft = ctypes.CDLL('./gpuFft/gpuFftInterface.so')

FORMAT = pyaudio.paInt16
CHANNELS = 1  # Future 2 channel?
RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()

deviceIndex = None  # Check if correct, none is apperently default
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=device_index)

fig, ax = plt.subplots()
x = np.arange(0, CHUNK // 2) 
line, = ax.plot(x, np.random.rand(CHUNK // 2))
plt.show(block=False)

try:
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)

        # Make data compatible with c types
        input_ctypes = audio_data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        output_data = np.zeros(CHUNK, dtype=np.float32)
        output_ctypes = output_data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        gpuFft.run_gpu_fft(input_ctypes, CHUNK, output_ctypes)

        # Update the plot with the FFT result
        line.set_ydata(np.abs(output_data[:CHUNK // 2]))
        ax.relim()
        ax.autoscale_view(True, True, True)
        fig.canvas.draw()
        fig.canvas.flush_events()
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
