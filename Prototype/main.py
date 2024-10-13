from dsp import run_audio_visualization,print_performance
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
    visualization_thread = threading.Thread(target=run_audio_visualization)
    visualization_thread.start()

    performance_thread = threading.Thread(target=print_performance)
    performance_thread.daemon = True  # Daemon thread will exit when the main program exits
    performance_thread.start()

    # Optional: Wait for both threads to finish (if needed)
    librespot_thread.join()
    visualization_thread.join()


if __name__ == "__main__":
    main()