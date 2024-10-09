import subprocess
import os

def setup_loopback_device():
    os.system("pactl load-module module-null-sink sink_name=loopback")
    os.system("pactl load-module module-loopback sink=loopback")

def run_librespot():
    subprocess.Popen(["librespot", "--name", "MyPi"])

if __name__ == "__main__":
    setup_loopback_device()
    run_librespot()