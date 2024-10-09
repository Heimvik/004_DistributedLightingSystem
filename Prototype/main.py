from dsp import runDspThread
from visuals import runVisualsThread

# Starting of the librespot server has to be done first: ./librespot/target/release/librespot --name "PLserver" &

def main():
    dspThread = runDspThread()
    visualsThread = runVisualsThread()
    
    dspThread.join()
    visualsThread.join()


if __name__ == "__main__":
    main()