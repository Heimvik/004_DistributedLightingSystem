
from dsp import run_audio_visualization, run_fft_visualization
import subprocess
import threading

def run_librespot():
    command = ['./librespot/target/release/librespot', '--name', 'PLserver', '--device', 'default']
    subprocess.run(command)

def main():
    # Start the librespot command in a separate thread
    librespot_thread = threading.Thread(target=run_librespot)
    librespot_thread.start()

    # Start the audio visualization in another separate thread
    #visualization_thread = threading.Thread(target=run_spectrogram_visualization)
    #visualization_thread.start()

    run_fft_visualization()

    # Optional: Wait for both threads to finish (if needed)
    librespot_thread.join()
    #visualization_thread.join()


if __name__ == "__main__":
    main()