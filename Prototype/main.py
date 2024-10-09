from dsp import initAudioProcessing

def main():
    dspThread = initAudioProcessing()
    dspThread.join()


if __name__ == "__main__":
    main()